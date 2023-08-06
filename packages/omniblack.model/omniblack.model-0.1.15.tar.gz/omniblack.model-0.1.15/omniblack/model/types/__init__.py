from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Mapping,
    MutableMapping,
    MutableSequence,
    NamedTuple,
    Optional,
)

from public import public

from ..field import Field
from ..validationResult import ValidationResult


class TypedValue(NamedTuple):
    type: str
    value: Any


@public
@dataclass(frozen=True)
class Adapter:
    """
    An adapter that can convert from the runtime reperstation of a type
    into a specific format.

    Attributes:
        from_: The function to use when converting from the format
            to the runtime reperstation.
        to: The function to use when converting from the runtime
            reperstation to this format.
        native: This type is natively supported by the format.
    """
    from_: Optional[Callable[[Any], Any]] = None
    to: Optional[Callable[[Any], Any]] = None
    native: bool = False

    def __contains__(self, key):
        value = self[key]
        return value is not None

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError as err:
            raise KeyError(*err.args) from None


native_adapter = Adapter(native=True)


class TypeExt(NamedTuple):
    adapters: Optional[Mapping[str, Adapter]] = None
    validator: Optional[Callable[[Mapping], ValidationResult]] = None
    attributes: Optional[Mapping[str, Field]] = None


def invoke(funcs, args, kwargs):
    first, *rest = funcs
    next_func = None
    if rest:
        next_func = create_invoke(*rest)

    return first(*args, next_func=next_func, **kwargs)


def create_invoke(*funcs):
    def invoker(*args, **kwargs):
        return invoke(funcs, args, kwargs)

    return invoker


@public
@dataclass(frozen=True)
class TypeDef:
    name: str = field(compare=True)
    implementation: type = field(compare=False)
    adapters: MutableMapping[str, Adapter] = field(compare=False)
    validator: Callable[[Mapping], ValidationResult] = field(compare=False)
    attributes: MutableSequence[Field] = field(compare=False)
    exts: MutableSequence[TypeExt] = field(compare=False, default_factory=list)

    @property
    def dict(self):
        return {
            'name': self.name,
            'implementation': self.implementation,
            'adapters': self.adapters,
            'validator': self.validator,
            'attributes': self.attributes,
            'exts': self.exts,
        }
