from enum import Enum


class IacType(str, Enum):
    TERRAFORM = 'terraform'
    CLOUDFORMATION = 'cloudformation'
