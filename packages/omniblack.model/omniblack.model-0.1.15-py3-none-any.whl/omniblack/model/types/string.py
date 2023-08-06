from functools import cache
from re import Pattern, compile
from sys import maxsize

from ..field import UiString
from ..localization import TXT
from ..types import TypeDef, native_adapter
from ..validationResult import ErrorTypes, ValidationMessage, ValidationResult

adapters = {
    name: native_adapter
    for name in ('string', 'json', 'yaml', 'toml', 'ini')
}


@cache
def create_allowed_chars_re(allowed_chars: str) -> Pattern:
    return compile(rf'[^{allowed_chars}]')


def validator(value, path, min_len=0, max_len=maxsize, allowed_chars=None):
    messages = []
    if len(value) > max_len:
        messages.append(ValidationMessage(
            ErrorTypes.constraint_error,
            TXT('${path} may not be longer than ${max_len}.', locals()),
            path,
        ))

    elif len(value) < min_len:
        messages.append(ValidationMessage(
            ErrorTypes.constraint_error,
            TXT('${path} may not be shorter than ${min_len}.', locals()),
            path,
        ))

    if allowed_chars:
        allowed_chars_re = create_allowed_chars_re(allowed_chars)
        if allowed_chars_re.search(value) is not None:
            msg = TXT(
                '${path} may only contain the characters ${allowed_chars}.',
                locals(),
            )
            messages.append(ValidationMessage(
                ErrorTypes.constraint_error,
                msg,
                path,
            ))

        return ValidationResult(not messages, messages)


attributes = [
    dict(
        name='allowed_chars',
        display=UiString('Allowed Characters'),
        desc=UiString(
            "A string of characters that are allowed in the field's values.",
        ),
        type='string',
    ),
    dict(
        name='min_len',
        display=UiString('Minimum Length'),
        desc=UiString("The minimum length of the field's value."),
        type='integer',
        assumed=0,
        attrs=dict(
            min=0,
            max=maxsize,
        ),
    ),
    dict(
        name='max_len',
        display=UiString('Maximum'),
        desc=UiString("The maximum length of the field's value."),
        type='integer',
        assumed=maxsize,
        attrs=dict(
            min=0,
            max=maxsize,
        ),
    ),
]

type_def = TypeDef(
    'string',
    str,
    adapters=adapters,
    validator=validator,
    attributes=attributes,
)
