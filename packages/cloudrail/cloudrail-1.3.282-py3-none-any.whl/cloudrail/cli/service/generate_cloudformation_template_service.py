import logging
import os
import sys
from dataclasses import dataclass
from typing import Dict

import click
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.data import JsonLexer
from pygments.styles.algol import AlgolStyle

from cloudrail.cli.commands_utils import exit_with_code, echo_error
from cloudrail.cli.exit_codes import ExitCode
from cloudrail.cli.service.cloudrail_cli_service import CloudrailCliService
from cloudrail.cli.service.command_service import CommandParameters, CommandService
from cloudrail.cli.service.service_response import ServiceResponseFactory, ServiceResponse
from cloudrail.cli.spinner_wrapper import SpinnerWrapper
from common.api.dtos.assessment_job_dto import RunOriginDTO
from common.api.dtos.supported_services_response_dto import SupportedSectionDTO
from common.utils.cloudformation_helper import CloudformationHelper
from common.utils.file_utils import file_to_json, validate_file_exist
from common.utils.string_utils import StringUtils


@dataclass
class GenerateFilteredCloudformationTemplateCommandParameters(CommandParameters):
    cfn_template_file: str = None
    output_file: str = None
    api_key: str = None
    notty: bool = None
    cfn_params: str = None
    cfn_params_file: str = None
    cfn_template_parameters: dict = None

    def validate_inputs(self):
        if not self.cfn_template_parameters:
            self.cfn_template_parameters = {}
        self._file_exist(self.cfn_template_file)
        if self.cfn_params:
            self.cfn_template_parameters.update(self.convert_key_val_params_to_dict(self.cfn_params))
        if self.cfn_params_file:
            self._file_exist(self.cfn_params_file)
            cfn_params_as_dict: dict = file_to_json(self.cfn_params_file).get('Parameters', {})
            self.cfn_template_parameters.update(cfn_params_as_dict)

        self._validate_required_cfn_template_parameters()

    def _validate_required_cfn_template_parameters(self):
        try:
            CloudformationHelper.validate_required_cfn_template_parameters(self.cfn_template_file, self.cfn_template_parameters)
        except Exception as ex:
            echo_error(str(ex))
            exit_with_code(ExitCode.INVALID_INPUT)

    @staticmethod
    def _file_exist(file_path: str):
        try:
            validate_file_exist(file_path)
        except Exception as ex:
            echo_error(str(ex))
            exit_with_code(ExitCode.INVALID_INPUT)


class GenerateCloudformationTemplateService(CommandService):
    def __init__(self, cloudrail_service: CloudrailCliService,
                 command_parameters: GenerateFilteredCloudformationTemplateCommandParameters,
                 command_name: str,
                 supported_services: Dict[str, SupportedSectionDTO] = None):
        self.is_tty = command_parameters.origin != RunOriginDTO.CI and not command_parameters.notty and sys.stdout.isatty()
        super().__init__(cloudrail_service, command_parameters, SpinnerWrapper(show_spinner=self.is_tty), self.is_tty, command_name)
        self._supported_services: Dict[str, SupportedSectionDTO] = supported_services or {}

    def generate_filtered_cfn_template(self):
        """
        Generating filtered CloudFormation template file as it will be send to CloudRail service
        """
        self.command_parameters.validate_inputs()

        if self.command_parameters.api_key:
            self.cloudrail_service.api_key = self.command_parameters.api_key

        self.spinner.start('Starting...')
        response: ServiceResponse = self.create_filtered_cfn_template(self.command_parameters.cfn_template_file,
                                                                      self._supported_services,
                                                                      self.command_parameters.cfn_template_parameters)
        if response.success:
            cfn_template_content: str = response.message
            if self.command_parameters.output_file:
                self._save_result_to_file(cfn_template_content)
            else:
                click.echo(self.pretty_cfn_template(cfn_template_content))
                exit_with_code(ExitCode.OK)
        else:
            self.spinner.fail(response.message)
            exit_with_code(ExitCode.INVALID_INPUT)

    @classmethod
    def create_filtered_cfn_template(cls, cfn_template_file: str,
                                     supported_services: Dict[str, SupportedSectionDTO],
                                     cfn_extra_params: dict = None) -> ServiceResponse:
        try:
            cfn_template_str: str = CloudformationHelper.create_filtered_cfn_template(cfn_template_file=cfn_template_file,
                                                                                      supported_services=supported_services,
                                                                                      cfn_params=cfn_extra_params)
        except Exception as ex:
            msg = f'failed to load CloudFormation template file={cfn_template_file}'
            logging.error(msg=msg, exc_info=ex)
            return ServiceResponseFactory.failed(msg)
        return ServiceResponseFactory.success(message=cfn_template_str)

    def _save_result_to_file(self, result: str) -> None:
        try:
            self.spinner.start(f'Saving results to: {self.command_parameters.output_file}')
            full_path = os.path.join(os.getcwd(), self.command_parameters.output_file)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as writer:
                writer.write(result)
        except Exception as ex:
            logging.exception('could not write result to file', exc_info=ex)
            self.spinner.fail(f'Failed to save filtered CloudFormation template to file: {self.command_parameters.output_file}')
            exit_with_code(ExitCode.INVALID_INPUT)

    @staticmethod
    def pretty_cfn_template(cfn_template_content: str) -> str:
        if StringUtils.is_json(cfn_template_content):
            return highlight(cfn_template_content, JsonLexer(), Terminal256Formatter())
        else:
            return highlight(cfn_template_content, JsonLexer(), Terminal256Formatter(style=AlgolStyle))
