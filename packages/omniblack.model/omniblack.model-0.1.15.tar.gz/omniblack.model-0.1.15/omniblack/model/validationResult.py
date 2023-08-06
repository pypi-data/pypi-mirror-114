from collections.abc import (
    Hashable,
    Iterable,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)
from dataclasses import dataclass
from enum import Enum
from functools import cached_property, partial
from itertools import chain
from typing import Any, TypedDict, Union

from public import public

from .abc import Localizable
from .dot_path import DotPath

mutable_container = (MutableMapping, MutableSequence)


class FrozenDict(Mapping):
    def __init__(self, *args, **kwargs):
        self._d = dict(*args, **kwargs)

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        return self._d[key]

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f'{cls_name}({repr(self._d)})'

    @classmethod
    def freeze(cls, target: mutable_container, *, _seen=None):
        if _seen is None:
            _seen = set()

        if isinstance(target, MutableMapping):
            freeze_mapping = partial(cls.freeze_mapping, _seen=_seen)

            forzen_values = map(freeze_mapping, target.items())

            return cls(forzen_values)
        else:
            return tuple(cls.freeze(value, _seen=_seen) for value in target)

    @classmethod
    def freeze_mapping(cls, item: Sequence[Hashable, Any], *, _seen):
        print(item)
        key, value = item
        if isinstance(value, mutable_container) and value not in _seen:
            value = cls.freeze(value, _seen=_seen)
        else:
            _seen.add(value)

        return key, value

    @cached_property
    def __hash(self):
        hash_ = 0
        for pair in self.items():
            hash_ ^= hash(pair)
        return hash_

    def __hash__(self):
        return self.__hash


@public
class ErrorTypes(Enum):
    model_error = 'The model contains an invalid setup.'
    invalid_value = 'The provided value is invalid for this type.'
    coercion_error = ('The value provided could not be coerced to/from the'
                      'specified format.')
    constraint_error = 'A constraint was violated.'

    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)


DotPathOrStr = Union[DotPath, str]


def coerce_str(path):
    if isinstance(path, DotPath):
        return path
    else:
        return DotPath.fromString(path)


@public
class ValidationMessageLike(TypedDict):
    type: ErrorTypes
    message: Localizable
    paths: Iterable[DotPath]
    suggestions: Iterable[Localizable]


@public
@dataclass(frozen=True)
class ValidationMessage:
    type: ErrorTypes
    message: Localizable
    paths: tuple[DotPath]
    suggestions: tuple[Localizable] = tuple()

    def __init__(
        self,
        type: ErrorTypes,
        message: Localizable,
        paths: Union[Iterable[DotPathOrStr], DotPathOrStr],
        suggestions: Iterable[Localizable] = tuple(),
    ):
        if isinstance(paths, (str, DotPath)):
            paths = (paths, )

        paths = tuple(coerce_str(path) for path in paths)

        object.__setattr__(self, 'paths', paths)

        object.__setattr__(self, 'suggestions', tuple(suggestions))

        object.__setattr__(self, 'type', type)

        object.__setattr__(self, 'message', message)


def coerce_msg(message):
    if not isinstance(message, ValidationMessage):
        return ValidationMessage(**message)

    return message


ValidationMsgLike = Union[ValidationMessage, ValidationMessageLike]
public(ValidationMsgLike=ValidationMsgLike)

messages_type = Union[Iterable[ValidationMsgLike], ValidationMsgLike]


@public
@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    messages: tuple[ValidationMessage]

    def __init__(
        self,
        valid: bool,
        messages: messages_type = tuple(),
    ):

        if not isinstance(messages, Iterable):
            messages = (messages, )

        messages_coerced = tuple(map(coerce_msg, messages))

        object.__setattr__(self, 'valid', valid)
        object.__setattr__(self, 'messages', messages_coerced)

    def merge(self, *other_results):
        final_valid = all(
            result.valid
            for result in chain((self, ), other_results)
        )

        all_messages = chain.from_iterable(
            result.messages
            for result in chain((self,), other_results)
        )

        return self.__class__(valid=final_valid, messages=all_messages)

    def __bool__(self):
        return self.valid

    def __iter__(self):
        return iter(self.messages)

    def __add__(self, other):
        return self.merge(other)

    def __or__(self, other):
        return self.merge(other)
