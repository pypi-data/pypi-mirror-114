from ..types import Adapter, TypeDef, native_adapter
from ..undefined import undefined
from ..validationResult import ValidationResult

type_name = 'boolean'


def from_string(string: str):
    if string.lower() == 'false':
        return False
    elif string.lower() == 'true':
        return True
    elif not string:
        return undefined
    else:
        raise ValueError(f'{string} cannot be converted into a boolean.')


str_adapter = Adapter(from_=from_string, to=str)


adapters = dict(
    string=str_adapter,
    json=native_adapter,
    yaml=native_adapter,
    toml=native_adapter,
)


def validator(value, path):
    return ValidationResult(True)


attributes = []

type_def = TypeDef(
    type_name,
    bool,
    adapters,
    validator,
    attributes,
)
