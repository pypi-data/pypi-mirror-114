from base64 import b64decode, b64encode
from binascii import Error as B64Error
from sys import maxsize

from humanize import naturalsize

from ..field import UiString
from ..localization import TXT
from ..types import Adapter, TypeDef, native_adapter
from ..validationResult import ErrorTypes, ValidationMessage, ValidationResult


def from_string(string: str):
    try:
        return b64decode(string, validate=True)
    except B64Error as err:
        raise ValueError('Invalid base64 data.') from err


def to_string(value: bytes):
    return b64encode(value).decode('ascii')


adapters = dict(
    str=Adapter(from_=from_string, to=to_string),
    yaml=native_adapter,
)


def validator(value, path, min=0, max=maxsize):
    messages = []
    if len(value) < min:
        min_human = naturalsize(min, binary=True)
        messages.append(ValidationMessage(
            ErrorTypes.constraint_error,
            TXT('${path} must not be less than ${min_human}.', locals()),
            path,
        ))
    elif len(value) > max:
        max_human = naturalsize(max, binary=True)
        messages.append(ValidationMessage(
            ErrorTypes.constraint_error,
            TXT('${path} must not be greater than ${max_human}.', locals()),
            path,
        ))

    return ValidationResult(not messages, messages)


attributes = [
    dict(
        name='min',
        display=UiString('Minimum'),
        desc=UiString("The minimum size of the field's data, in bytes."),
        type='integer',
        assumed=0,
        attrs=dict(
            min=0,
            max=maxsize,
        ),
    ),
    dict(
        name='max',
        display=UiString('Maximum'),
        desc=UiString("The maximum size of the field's data, in bytes."),
        type='integer',
        assumed=maxsize,
        attrs=dict(
            min=0,
            max=maxsize,
        ),
    ),
]

type_def = TypeDef(
    'binary',
    bytes,
    adapters=adapters,
    validator=validator,
    attributes=attributes,
)
