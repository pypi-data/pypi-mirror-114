from ..field import UiString
from ..localization import TXT
from ..types import Adapter, TypeDef
from ..validationResult import ErrorTypes, ValidationMessage, ValidationResult

type_name = 'integer'

str_adapter = Adapter(from_=int, to=str)

adapters = dict(string=str_adapter)


def validator(value, path, min=None, max=None):
    messages = []
    if max is not None and value > max:
        messages.append(ValidationMessage(
            ErrorTypes.constraint_error,
            TXT('${value} must not be greater than ${max}.', locals()),
            path,
        ))

    elif min is not None and value < min:
        messages.append(ValidationMessage(
            ErrorTypes.constraint_error,
            TXT('${value} must not be less than ${min}.', locals()),
            path,
        ))

    return ValidationResult(not messages, messages)


attributes = [
    dict(
        name='min',
        display=UiString('Minimum'),
        desc=UiString('The minimum value allowed for this field.'),
        type='integer',
    ),
    dict(
        name='max',
        display=UiString('Maximum'),
        desc=UiString('The maximum value allowed for this field.'),
        type='integer',
    ),
]


type_def = TypeDef(
    type_name,
    int,
    adapters=adapters,
    validator=validator,
    attributes=attributes,
)
