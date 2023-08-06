from dataclasses import dataclass
from typing import Optional
import click
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.data import JsonLexer
from pygments.styles.monokai import MonokaiStyle

from cloudrail.cli.api_client.external_api_client import ExternalApiClient
from cloudrail.cli.commands_utils import echo_error, validate_origin, validate_input_paths, exit_with_code
from cloudrail.cli.error_messages import generate_convert_terraform_plan_to_json_failure_message, \
    generate_process_plan_json_failure_message, generate_simple_message
from cloudrail.cli.exit_codes import ExitCode
from cloudrail.cli.service.cloudrail_cli_service import CloudrailCliService
from cloudrail.cli.service.command_service import CommandParameters
from cloudrail.cli.service.evaluation_run_command.evaluation_run_command_service import EvaluationRunCommandService, BaseRunCommandParameters
from cloudrail.cli.terraform_service.terraform_context_service import TerraformContextService
from common.api.dtos.account_config_dto import AccountConfigDTO
from common.api.dtos.cloud_provider_dto import CloudProviderDTO
from common.constants import IacType
from common.exceptions import UnsupportedCloudProviderException


@dataclass
class GenerateFilteredPlanCommandParameters(CommandParameters):
    directory: str = None
    tf_plan: str = None
    output_file: str = None
    api_key: str = None
    notty: bool = None
    cloud_provider: Optional[CloudProviderDTO] = None
    base_dir: str = None


@dataclass
class TerraformRunCommandParameters(BaseRunCommandParameters):
    directory: str = None
    tf_plan: str = None
    filtered_plan: str = None
    base_dir: str = None


class TerraformEvalRunCmdService(EvaluationRunCommandService):
    def __init__(self, cloudrail_service: CloudrailCliService,
                 terraform_environment_service: TerraformContextService,
                 command_parameters: CommandParameters, command_name: str):
        super().__init__(cloudrail_service, command_parameters, command_name)
        self.terraform_environment_service = terraform_environment_service

    def _validate_input_paths(self):
        self.command_parameters.tf_plan, self.command_parameters.directory, self.command_parameters.filtered_plan = \
            validate_input_paths(self.command_parameters.tf_plan,
                                 self.command_parameters.directory,
                                 self.command_parameters.filtered_plan,
                                 self.is_tty)

    def _upload_iac_file(self, customer_id: str, account_config: AccountConfigDTO, job_id: str, custom_rules: dict, drift_track: bool):
        self.spinner.start('Preparing a filtered Terraform plan locally before uploading to Cloudrail Service...')
        if not self.command_parameters.filtered_plan:
            filtered_plan, checkov_result = self._create_filtered_plan(
                customer_id=customer_id,
                base_dir=self.command_parameters.base_dir,
                cloud_provider=(account_config and account_config.cloud_provider) or self.command_parameters.cloud_provider,
                job_id=job_id,
                submit_failure=True)
            self._submit_filtered_plan(filtered_plan, checkov_result, custom_rules, job_id, drift_track)
        else:
            self._submit_existing_filtered_plan(custom_rules, job_id, drift_track)

    def generate_filtered_plan(self):
        """
        Send Terraform out file to Cloudrail service for evaluation. We are getting back
        job_id and checking every X sec if the evaluation is done.
        """
        self.command_parameters.origin = validate_origin(self.command_parameters.origin)
        self.command_parameters.tf_plan, self.command_parameters.directory, unused_filtered_plan = validate_input_paths(
            self.command_parameters.tf_plan,
            self.command_parameters.directory,
            None,
            self.is_tty)

        if self.command_parameters.api_key:
            self.cloudrail_service.api_key = self.command_parameters.api_key

        self.spinner.start('Starting...')
        customer_id = self.call_service(self.cloudrail_service.get_my_customer_data, (), ExitCode.BACKEND_ERROR).id
        filtered_plan, _ = self._create_filtered_plan(customer_id=customer_id,
                                                      cloud_provider=self.command_parameters.cloud_provider,
                                                      base_dir=self.command_parameters.base_dir)
        if self.command_parameters.output_file:
            self._save_result_to_file(str(filtered_plan), self.command_parameters.output_file)
            self.spinner.succeed()
        else:
            click.echo(filtered_plan)
            exit_with_code(ExitCode.OK)

    def _create_filtered_plan(self,
                              customer_id: str,
                              cloud_provider: CloudProviderDTO,
                              base_dir: str,
                              job_id: str = None,
                              submit_failure: bool = False):
        self.spinner.start('Re-running your Terraform plan through a customized \'terraform plan\' to generate needed context data...')
        service_result = self.terraform_environment_service.convert_plan_to_json(self.command_parameters.tf_plan,
                                                                                 self.command_parameters.directory)
        if not service_result.success:
            if submit_failure:
                self.cloudrail_service.submit_failure(service_result.error, job_id)
            self.spinner.fail()
            echo_error(generate_convert_terraform_plan_to_json_failure_message(service_result.error, job_id))
            self._exit_on_failure(ExitCode.CLI_ERROR, job_id)
        self.spinner.start('Filtering and processing Terraform data...')
        cloud_provider = self._calculate_cloud_provider(cloud_provider, service_result.result)
        if cloud_provider == CloudProviderDTO.AMAZON_WEB_SERVICES:
            supported_services_result = self.call_service(function=self.cloudrail_service.list_aws_supported_services,
                                                          parameters=(IacType.TERRAFORM, ),
                                                          exit_code_if_failure=ExitCode.BACKEND_ERROR)
        elif cloud_provider == CloudProviderDTO.AZURE:
            supported_services_result = self.call_service(self.cloudrail_service.list_azure_supported_services, (), ExitCode.BACKEND_ERROR)
        elif cloud_provider == CloudProviderDTO.GCP:
            supported_services_result = self.call_service(self.cloudrail_service.list_gcp_supported_services, (), ExitCode.BACKEND_ERROR)
        else:
            raise UnsupportedCloudProviderException(cloud_provider)

        supported_checkov_services_result = self.call_service(self.cloudrail_service.list_checkov_supported_services, (cloud_provider,),
                                                              ExitCode.BACKEND_ERROR)

        supported_checkov_services = supported_checkov_services_result.supported_checkov_services
        checkov_results = self.terraform_environment_service.run_checkov_checks(self.command_parameters.directory,
                                                                                supported_checkov_services,
                                                                                base_dir)

        if not checkov_results.success:
            echo_error(checkov_results.error)
            self._exit_on_failure(ExitCode.BACKEND_ERROR, job_id)

        service_result = self.terraform_environment_service.process_json_result(service_result.result,
                                                                                supported_services_result.supported_services,
                                                                                checkov_results.result,
                                                                                customer_id,
                                                                                ExternalApiClient.get_cli_handshake_version(),
                                                                                base_dir,
                                                                                cloud_provider)

        if not service_result.success:
            if submit_failure:
                self.cloudrail_service.submit_failure(service_result.error, job_id)
            self.spinner.fail()
            echo_error(generate_process_plan_json_failure_message(service_result.error, job_id))
            self._exit_on_failure(ExitCode.CLI_ERROR, job_id)

        self.spinner.start('Obfuscating IP addresses...')
        self.spinner.succeed()
        return service_result.result, checkov_results.result

    def _submit_filtered_plan(self, filtered_plan, checkov_result, custom_rules, job_id, drift_track):
        if not self.command_parameters.auto_approve:
            if not self.is_tty:
                echo_error('You have chosen to do a full run without interactive login. '
                           'This means Cloudrail CLI cannot show you the filtered plan prior to uploading to the Cloudrail Service. '
                           'In such a case you can either:'
                           '\n1. Execute \'cloudrail generate-filtered-plan\' '
                           'first, then provide the file to \'cloudrail run --filtered-plan\'.'
                           '\n2. Re-run \'cloudrail run\' with \'--auto-approve\', '
                           'indicating you are approving the upload of the filtered plan to Cloudrail Service.')
                exit_with_code(ExitCode.INVALID_INPUT, self.command_parameters.no_fail_on_service_error)
            click.echo(highlight(filtered_plan, JsonLexer(), Terminal256Formatter(style=MonokaiStyle)))
            if checkov_result:
                click.echo('For some non-context-aware rules, '
                           'Cloudrail utilized the Checkov engine and found a few violations.'
                           '\nSuch violations will be marked with the \'CKV_*\' rule ID.\n')
            approved = click.confirm('OK to upload this Terraform data to Cloudrail'
                                     ' (use \'--auto-approve\' to skip this in the future)?', default=True)
            if not approved:
                self.cloudrail_service.submit_failure('terraform data not approved for upload', job_id)
                echo_error('Upload not approved. Aborting.')
                exit_with_code(ExitCode.USER_TERMINATION, self.command_parameters.no_fail_on_service_error)

        self.spinner.start('Submitting Terraform data to the Cloudrail Service...')
        self.call_service(self.cloudrail_service.submit_filtered_plan, (filtered_plan, job_id, custom_rules, drift_track),
                          ExitCode.BACKEND_ERROR, simple_message=True)

    def _submit_existing_filtered_plan(self, custom_rules, job_id: str, drift_track: bool):
        service_result = self.terraform_environment_service.read_terraform_output_file(self.command_parameters.filtered_plan)
        if not service_result.success:
            echo_error(generate_simple_message('Error while reading json file. This is probably due to an '
                                               'outdated Terraform show output generated by Cloudrail CLI container.'
                                               '\nPlease pull the latest version of this container and use \'generated-filtered-plan\' '
                                               'to regenerate the file.', job_id))
            exit_with_code(ExitCode.INVALID_INPUT, self.command_parameters.no_fail_on_service_error)
        self.spinner.start('Submitting Terraform data to the Cloudrail Service...')
        self.call_service(self.cloudrail_service.submit_filtered_plan, (service_result.result, job_id, custom_rules, drift_track),
                          ExitCode.BACKEND_ERROR, simple_message=True)
