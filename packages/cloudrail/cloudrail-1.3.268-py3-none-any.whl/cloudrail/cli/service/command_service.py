import logging
import uuid
from dataclasses import dataclass
from time import sleep
from typing import Optional

import click

from common.constants import IacType
from common.api.dtos.assessment_job_dto import RunOriginDTO
from cloudrail.cli.commands_utils import exit_with_code, offer_to_upload_log_and_exit
from cloudrail.cli.error_messages import generate_simple_message
from cloudrail.cli.exit_codes import ExitCode
from cloudrail.cli.service.cloudrail_cli_service import CloudrailCliService
from cloudrail.cli.service.service_response_status import ResponseStatus
from cloudrail.cli.spinner_wrapper import SpinnerWrapper


@dataclass
class CommandParameters:
    no_fail_on_service_error: bool = None
    upload_log: bool = False
    no_upload_log: bool = False
    origin: RunOriginDTO = RunOriginDTO.WORKSTATION
    iac_type: IacType = IacType.TERRAFORM

    @staticmethod
    def convert_key_val_params_to_dict(key_val_params: str, delimiter=',') -> dict:
        params_dict: dict = {}
        for key_val in key_val_params.split(delimiter):
            key_val = key_val.split('=')
            if len(key_val) == 2:
                params_dict[key_val[0]] = key_val[1]
        return params_dict


class CommandService:
    def __init__(self, cloudrail_service: CloudrailCliService,
                 command_parameters: CommandParameters,
                 spinner: SpinnerWrapper, is_tty: bool, command_name: str):
        self.cloudrail_service = cloudrail_service
        self.command_parameters = command_parameters
        self.spinner = spinner
        self.is_tty = is_tty
        self.command_name: Optional[str] = command_name

    # pylint: disable=R1710
    def call_service(self, function, parameters,
                     exit_code_if_failure: ExitCode,
                     message_if_failure: Optional[str] = None,
                     simple_message: bool = False,
                     offer_to_send_log: bool = True,
                     retry_count: int = 2):
        try:
            service_result = self.try_call_service(retry_count, function, parameters)
            if service_result.status == ResponseStatus.UNAUTHORIZED:
                click.echo(service_result.message)
                exit_with_code(ExitCode.INVALID_INPUT)
            if service_result.status == ResponseStatus.FAILURE:
                message = message_if_failure or service_result.message
                if simple_message:
                    message = generate_simple_message(service_result.message)
                self.spinner.fail()
                click.echo(message)
                if offer_to_send_log:
                    self._exit_on_failure(exit_code_if_failure)
                else:
                    exit_with_code(exit_code_if_failure, self.command_parameters.no_fail_on_service_error)
            return service_result.message
        except Exception:
            logging.exception(f'error while trying to call {function}')
            self._exit_on_failure(exit_code_if_failure)

    def _exit_on_failure(self,
                         exit_code: ExitCode,
                         job_id: Optional[str] = None):
        if not job_id:
            job_id = str(uuid.uuid4())
        offer_to_upload_log_and_exit(self.cloudrail_service, exit_code, self.command_parameters.upload_log,
                                     self.command_parameters.no_upload_log, self.command_parameters.origin,
                                     self.is_tty, job_id, self.command_name, self.command_parameters.no_fail_on_service_error)

    @staticmethod
    def try_call_service(retry_count, function, parameters):
        service_result = function(*parameters)
        while retry_count > 0 and not service_result.success:
            sleep(2)
            retry_count = retry_count - 1
            service_result = function(*parameters)
        return service_result
