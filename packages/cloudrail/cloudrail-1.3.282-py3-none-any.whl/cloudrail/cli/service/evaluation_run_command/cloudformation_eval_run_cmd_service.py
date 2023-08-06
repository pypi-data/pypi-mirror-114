import json
import os
import re
from dataclasses import dataclass

import click
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.data import JsonLexer

from cloudrail.cli.commands_utils import echo_error, exit_with_code
from cloudrail.cli.exit_codes import ExitCode
from cloudrail.cli.service.cloudrail_cli_service import CloudrailCliService
from cloudrail.cli.service.command_service import CommandParameters
from cloudrail.cli.service.evaluation_run_command.evaluation_run_command_service import EvaluationRunCommandService, BaseRunCommandParameters
from cloudrail.cli.service.generate_cloudformation_template_service import GenerateCloudformationTemplateService
from cloudrail.cli.service.service_response import ServiceResponse
from common.api.dtos.account_config_dto import AccountConfigDTO
from common.constants import IacType
from common.utils.cloudformation_helper import CloudformationHelper
from common.utils.file_utils import file_to_json


@dataclass
class CloudformationRunCommandParameters(BaseRunCommandParameters):
    iac_type: IacType = IacType.CLOUDFORMATION
    cfn_template_file: str = None
    cfn_filtered_template_file: str = None
    cfn_params: str = None
    cfn_params_file: str = None
    cfn_stack_name: str = None
    cfn_stack_region: str = None


class CloudformationEvalRunCmdService(EvaluationRunCommandService):
    def __init__(self, cloudrail_service: CloudrailCliService,
                 command_parameters: CommandParameters, command_name: str):
        super().__init__(cloudrail_service=cloudrail_service, command_parameters=command_parameters,
                         command_name=command_name)

    def _validate_input_paths(self) -> None:
        cfn_stack_name: str = self.command_parameters.cfn_stack_name
        cfn_template_file: str = self.command_parameters.cfn_template_file
        cfn_filtered_template_file: str = self.command_parameters.cfn_filtered_template_file
        cfn_params: str = self.command_parameters.cfn_params
        cfn_params_file: str = self.command_parameters.cfn_params_file
        self.command_parameters.cfn_stack_region = os.getenv('AWS_REGION', self.command_parameters.cfn_stack_region)
        cfn_stack_region: str = self.command_parameters.cfn_stack_region

        if not cfn_stack_name:
            if self.command_parameters.no_cloud_account:
                cfn_stack_name = os.path.basename(self.command_parameters.cfn_template_file or self.command_parameters.cfn_filtered_template_file)
                cfn_stack_name = os.path.splitext(cfn_stack_name)[0]
                self.command_parameters.cfn_stack_name = cfn_stack_name
            elif self.is_tty:
                cfn_stack_name = click.prompt('Enter "cfn-stack-name" parameter').strip()
                self.command_parameters.cfn_stack_name = cfn_stack_name

            else:
                echo_error('Must provide "cfn-stack-name" parameter')
                exit_with_code(ExitCode.INVALID_INPUT)

        if not cfn_stack_region:
            if self.is_tty:
                cfn_stack_region = click.prompt('Enter "cfn-stack-region" parameter').strip()
                self.command_parameters.cfn_stack_region = cfn_stack_region
            else:
                echo_error('Must provide "cfn-stack-region" parameter')
                exit_with_code(ExitCode.INVALID_INPUT)

        if cfn_filtered_template_file:
            if not os.path.exists(cfn_filtered_template_file):
                echo_error(f'The CloudFormation filtered template file path you have provided "{cfn_filtered_template_file}" '
                           f'does not point to a specific file.'
                           '\nPlease provide the path directly to the filtered template file you wish to use Cloudrail with.')
                exit_with_code(ExitCode.INVALID_INPUT)
        if cfn_template_file:
            if not os.path.exists(cfn_template_file):
                echo_error(f'The CloudFormation template file path you have provided "{cfn_template_file}" '
                           f'does not point to a specific file.'
                           '\nPlease provide the path directly to the template file you wish to use Cloudrail with.')
                exit_with_code(ExitCode.INVALID_INPUT)

        if cfn_template_file and cfn_filtered_template_file:
            echo_error('Can\'t define both "cfn-template-file" and "cfn-filtered-template-file" parameters]\n'
                       '\nPlease provide only one')
            exit_with_code(ExitCode.INVALID_INPUT)

        if cfn_params and not self._is_cfn_params_format_valid(cfn_params):
            echo_error('Invalid CloudFormation parameters format set in "cfn-params" parameter\n'
                       '\nPlease enter valid format, i.e. myKey1=myValue1,myKey2=myValue2...')
            exit_with_code(ExitCode.INVALID_INPUT)

        if cfn_params_file and not os.path.exists(cfn_params_file):
            echo_error(f'The CloudFormation parameters file path you have provided "{cfn_params_file}" '
                       'does not point to a specific file.'
                       '\nPlease provide the path directly to the parameters file you wish to use Cloudrail with.')
            exit_with_code(ExitCode.INVALID_INPUT)

        if not self.command_parameters.cloud_provider:
            self.command_parameters.cloud_provider = 'aws'

        if self.command_parameters.no_cloud_account and not self.command_parameters.cloud_account_id:
            self.command_parameters.cloud_account_id = '000000000000'

        parsed_cfn_params: dict = {}
        if cfn_params:
            parsed_cfn_params = self._to_cfn_params_dict(cfn_params)
        elif cfn_params_file:
            parsed_cfn_params = file_to_json(cfn_params_file).get('Parameters', {})

        try:
            CloudformationHelper \
                .validate_required_cfn_template_parameters(cfn_filtered_template_file or cfn_template_file, parsed_cfn_params)
        except Exception as ex:
            echo_error(str(ex))
            exit_with_code(ExitCode.INVALID_INPUT)

    def _upload_iac_file(self, customer_id: str, account_config: AccountConfigDTO,
                         job_id: str, custom_rules: dict, drift_track: bool):
        cfn_template_content_as_dict: dict = {}
        if self.command_parameters.cfn_template_file:
            filtered_cfn_template: str = self._create_filtered_cfn_template()
            cfn_template_content_as_dict = CloudformationHelper.cfn_template_str_to_dict(filtered_cfn_template)
        elif self.command_parameters.cfn_filtered_template_file:
            cfn_template_content_as_dict = CloudformationHelper.load_cfn_template(self.command_parameters.cfn_filtered_template_file)
        else:
            self.spinner.fail('CloudFormation template isn\'t provided')
            exit_with_code(ExitCode.INVALID_INPUT, self.command_parameters.no_fail_on_service_error)

        cfn_parameters: dict = {}
        if self.command_parameters.cfn_params:
            cfn_parameters.update(self.command_parameters.convert_key_val_params_to_dict(self.command_parameters.cfn_params))

        if self.command_parameters.cfn_params_file:
            params: dict = file_to_json(self.command_parameters.cfn_params_file)
            if 'Parameters' in params:
                cfn_parameters.update(params['Parameters'])
            else:
                echo_error('Invalid CloudFormation parameters json file structure, missing \'Parameters\' key')
                exit_with_code(ExitCode.INVALID_INPUT)

        CloudformationHelper.update_cfn_template_with_extra_parameters(cfn_template_content=cfn_template_content_as_dict,
                                                                       cfn_stack_name=self.command_parameters.cfn_stack_name,
                                                                       iac_type=self.command_parameters.iac_type,
                                                                       cloud_provider=account_config.cloud_provider if account_config
                                                                       else self.command_parameters.cloud_provider,
                                                                       cfn_stack_region=self.command_parameters.cfn_stack_region,
                                                                       account_config=account_config,
                                                                       cfn_parameters=cfn_parameters,
                                                                       account_id=(account_config and account_config.cloud_account_id) or
                                                                                  self.command_parameters.cloud_account_id)

        self._submit_filtered_cfn_template(json.dumps(cfn_template_content_as_dict, indent=4, sort_keys=True), custom_rules, job_id, drift_track)
        self.spinner.succeed('Upload completed')

    def _submit_filtered_cfn_template(self, filtered_cfn_template_as_json_str: str, custom_rules: dict, job_id: str, drift_track: bool):
        if not self.command_parameters.auto_approve:
            if not self.is_tty:
                echo_error('You have chosen to do a full run without interactive login. '
                           'This means Cloudrail CLI cannot show you the filtered cloudformation template prior to uploading to'
                           ' the Cloudrail Service. In such a case you can either:'
                           '\n1. Execute \'cloudrail generate-filtered-cfn-template\' '
                           'first, then provide the file to \'cloudrail run --cfn-filtered-template-file\'.'
                           '\n2. Re-run \'cloudrail run\' with \'--auto-approve\', '
                           'indicating you are approving the upload of the filtered template to Cloudrail Service.')
                exit_with_code(ExitCode.INVALID_INPUT, self.command_parameters.no_fail_on_service_error)
            click.echo(highlight(filtered_cfn_template_as_json_str, JsonLexer(), Terminal256Formatter()))

            approved: bool = click.confirm('OK to upload this CloudFormation template content to Cloudrail'
                                           ' (use \'--auto-approve\' to skip this in the future)?', default=True)
            if not approved:
                self.cloudrail_service.submit_failure('CloudFormation template content not approved for upload', job_id)
                echo_error('Upload not approved. Aborting.')
                exit_with_code(ExitCode.USER_TERMINATION, self.command_parameters.no_fail_on_service_error)

        self.spinner.start('Submitting cloudformation filtered template to the Cloudrail Service...')
        self.call_service(self.cloudrail_service.submit_filtered_plan, (filtered_cfn_template_as_json_str, job_id, custom_rules, drift_track),
                          ExitCode.BACKEND_ERROR, simple_message=True)

    def _create_filtered_cfn_template(self, job_id: str = None, submit_failure: bool = False) -> str:
        self.spinner.start('Starting to generate cloudformation filtered template')
        supported_services_result = self.call_service(function=self.cloudrail_service.list_aws_supported_services,
                                                      parameters=(IacType.CLOUDFORMATION, ),
                                                      exit_code_if_failure=ExitCode.BACKEND_ERROR)
        cfn_filtered_template_response: ServiceResponse = GenerateCloudformationTemplateService.create_filtered_cfn_template(
            cfn_template_file=self.command_parameters.cfn_template_file,
            supported_services=supported_services_result.supported_services)
        if cfn_filtered_template_response.success:
            self.spinner.succeed("CloudFormation filtered template generated successfully")
        else:
            if submit_failure:
                self.cloudrail_service.submit_failure(cfn_filtered_template_response.message, job_id)
            self.spinner.fail(cfn_filtered_template_response.message)
            self._exit_on_failure(ExitCode.CLI_ERROR, job_id)
        return cfn_filtered_template_response.message

    @staticmethod
    def _is_cfn_params_format_valid(cfn_params: str) -> bool:
        if not cfn_params:
            return False
        for key_val in re.split(',', cfn_params):
            if len(re.split('=', key_val)) != 2:
                return False
        return True

    @staticmethod
    def _to_cfn_params_dict(cfn_params: str) -> dict:
        key_val_params: dict = {}
        for key_val in re.split(',', cfn_params):
            key_val_pair = re.split('=', key_val)
            key_val_params[key_val_pair[0]] = key_val_pair[1]
        return key_val_params
