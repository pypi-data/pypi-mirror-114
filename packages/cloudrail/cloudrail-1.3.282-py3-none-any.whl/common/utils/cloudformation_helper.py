from typing import Dict, Set
from cfn_tools import load_json, load_yaml, ODict, dump_json
from common.api.dtos.account_config_dto import AccountConfigDTO
from common.api.dtos.cloud_provider_dto import CloudProviderDTO
from common.api.dtos.supported_services_response_dto import SupportedSectionDTO
from common.constants import IacType
from common.utils.file_utils import read_file, raise_file_format_mismatch
from common.utils.string_utils import StringUtils

# pylint: disable=R1710


class CloudformationHelper:

    EXTRA_PARAMETERS_KEY: str = 'cr_extra_params'

    @staticmethod
    def validate_required_cfn_template_parameters(cfn_template_file: str, cfn_template_parameters: dict):
        cfn_template_content: dict = {}
        if cfn_template_file.endswith('.json'):
            cfn_template_content = CloudformationHelper.file_to_cfn_json(cfn_template_file)
        elif cfn_template_file.endswith('.yaml'):
            cfn_template_content = CloudformationHelper.file_to_cfn_yaml(cfn_template_file)
        else:
            raise_file_format_mismatch(cfn_template_file)
        template_parameters: dict = cfn_template_content.get('Parameters', {})
        for param_name in template_parameters:
            if param_name not in cfn_template_parameters and 'Default' not in template_parameters[param_name]:
                raise Exception(f'Missing required template parameter "{param_name}"')

    @classmethod
    def update_cfn_template_with_extra_parameters(cls, cfn_template_content: dict, cfn_stack_name: str, iac_type: IacType,
                                                  cloud_provider: CloudProviderDTO, cfn_stack_region: str, account_id: str,
                                                  account_config: AccountConfigDTO = None, cfn_parameters: dict = None):
        cfn_template_content[cls.EXTRA_PARAMETERS_KEY] = {}
        cfn_template_content[cls.EXTRA_PARAMETERS_KEY]['stack_name'] = cfn_stack_name
        cfn_template_content[cls.EXTRA_PARAMETERS_KEY]['iac_type'] = iac_type
        cfn_template_content[cls.EXTRA_PARAMETERS_KEY]['cloud_provider'] = account_config.cloud_provider if account_config \
            else cloud_provider
        cfn_template_content[cls.EXTRA_PARAMETERS_KEY]['region'] = cfn_stack_region
        cfn_template_content[cls.EXTRA_PARAMETERS_KEY]['account_id'] = account_id

        if account_config:
            cfn_template_content[cls.EXTRA_PARAMETERS_KEY]['account_name'] = account_config.name

        if cfn_parameters:
            cfn_template_content[cls.EXTRA_PARAMETERS_KEY].update(cfn_parameters)

    @classmethod
    def create_filtered_cfn_template(cls, cfn_template_file: str,
                                     supported_services: Dict[str, SupportedSectionDTO],
                                     cfn_params: dict = None) -> str:
        cfn_template_dict: dict = cls.load_cfn_template(cfn_template_file)
        cls.handle_include_resources(cfn_template_dict, supported_services)
        # self._handle_hashed_properties() # todo
        cfn_template_dict.update(ODict([[cls.EXTRA_PARAMETERS_KEY, cls.to_odict(cfn_params or {})]]))
        return dump_json(cfn_template_dict)

    @staticmethod
    def handle_include_resources(cfn_template_dict: dict, supported_services: Dict[str, SupportedSectionDTO]) -> None:
        if supported_services:
            properties_to_include: Dict[str, Set[str]] = {}
            common_properties = supported_services.get('common', {})
            for resource_name, properties in supported_services.items():
                properties_to_include[resource_name] = set(properties.known_fields.pass_values)
                properties_to_include[resource_name].update(common_properties.known_fields.pass_values)
            del properties_to_include['common']

            for resource in cfn_template_dict.get('Resources').values():
                resource_type: str = resource['Type']
                properties: dict = resource.get('Properties', ODict())
                for property_name in properties.copy():
                    if property_name.lower() not in properties_to_include.get(resource_type, {}):
                        del properties[property_name]

    @classmethod
    def load_cfn_template(cls, cfn_template_file: str) -> dict:
        if cfn_template_file.endswith('.json'):
            return cls.file_to_cfn_json(cfn_template_file)
        elif cfn_template_file.endswith('.yaml'):
            return cls.file_to_cfn_yaml(cfn_template_file)
        else:
            cls.raise_invalid_cfn_template_file()

    @classmethod
    def cfn_template_str_to_dict(cls, cfn_template_content: str) -> dict:
        if StringUtils.is_json(cfn_template_content):
            return load_json(cfn_template_content)
        elif StringUtils.is_yaml(cfn_template_content):
            return load_yaml(cfn_template_content)
        else:
            cls.raise_invalid_cfn_template_file()

    @staticmethod
    def file_to_cfn_json(file_path: str) -> dict:
        try:
            return load_json(read_file(file_path))
        except Exception as ex:
            message = f'Error while reading CloudFormation template JSON file {file_path}. {ex}'
            raise Exception(message)

    @staticmethod
    def file_to_cfn_yaml(file_path: str) -> dict:
        try:
            return load_yaml(read_file(file_path))
        except Exception as ex:
            message = f'error while reading CloudFormation template yaml file {file_path}. {ex}'
            raise Exception(message)

    @staticmethod
    def to_odict(ordinary_dict: dict) -> ODict:
        return ODict([[key, val] for key, val in ordinary_dict.items()])

    @staticmethod
    def raise_invalid_cfn_template_file():
        raise Exception('Invalid CloudFormation template file format')
