from dataclasses import dataclass
from typing import List

from dataclasses_json import DataClassJsonMixin

from common.api.dtos.rule_info_dto import RuleSeverityDTO, RuleTypeDTO, SecurityLayerDTO, ResourceTypeDTO


@dataclass
class RuleTaskDTO(DataClassJsonMixin):
    rule_id: str
    rule_name: str
    description: str
    rule_type: RuleTypeDTO
    security_layer: SecurityLayerDTO
    resource_types: List[ResourceTypeDTO]
    severity: RuleSeverityDTO
    logic: str
    iac_remediation_steps: str
    console_remediation_steps: str
    last_validation: str
    account_config_ids: List[str]
