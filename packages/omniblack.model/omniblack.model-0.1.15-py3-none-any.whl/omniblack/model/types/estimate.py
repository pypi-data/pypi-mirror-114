from sys import float_info

from ..field import UiString
from ..localization import TXT
from ..types import Adapter, TypeDef, native_adapter
from ..validationResult import ErrorTypes, ValidationMessage, ValidationResult

adapters = dict(
    string=Adapter(from_=float, to=str),
    json=native_adapter,
    yaml=native_adapter,
    toml=native_adapter,
)


def validator(value, path, min=-float_info.max, max=float_info.max):
    messages = []

    if value > max:
        messages.append(ValidationMessage(
            ErrorTypes.constraint_error,
            TXT('${path} must not be greater than ${max}.', locals()),
            path,
        ))
    elif value < min:
        messages.append(ValidationMessage(
            ErrorTypes.constraint_error,
            TXT('${path} must not be less than ${min}.', locals()),
            path,
        ))

    return ValidationResult(not messages, messages)


attributes = [
    dict(
        name='min',
        display=UiString('Minimum'),
        desc=UiString('The minimum value allowed for this field.'),
        type='integer',
        assumed=-float_info.max,
    ),
    dict(
        name='max',
        display=UiString('Maximum'),
        desc=UiString('The maximum value allowed for this field.'),
        type='integer',
        assumed=float_info.max,
    ),
]


type_def = TypeDef(
    'estimate',
    float,
    adapters=adapters,
    validator=validator,
    attributes=attributes,
)
