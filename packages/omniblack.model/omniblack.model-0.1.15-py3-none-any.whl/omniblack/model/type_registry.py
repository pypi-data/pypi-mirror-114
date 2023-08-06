from collections.abc import Callable, MutableMapping, MutableSequence
from importlib import import_module
from typing import Any, Literal

from .abc import Registry
from .dot_path import DotPath
from .errors import CoercionError
from .field import Field
from .localization import TXT
from .types import Adapter, TypeExt
from .undefined import undefined
from .validationResult import ErrorTypes, ValidationMessage, ValidationResult

direction_displays = {
    'from_': 'from',
    'to': 'to',
}


def create_adapter(direction: Literal['from_', 'to']):
    def adapt(self, format_name, value, type_name, original_format=None):
        adapters = self[type_name].adapters
        if format_name in adapters:
            adapter = adapters[format_name]
            if adapter.native:
                return value

            if direction in adapter:
                converted_value = adapter[direction](value)
                return converted_value

        if format_name != 'string':
            return adapt(self, 'string', value, type_name, format_name)
        else:
            dir = direction_displays[direction]
            if original_format is None:
                original_format = format_name
            raise CoercionError(
                f'Canont convert {type_name} {dir} {original_format}.'
            )

    return adapt


class TypeRegistry(Registry):
    to_format = create_adapter('to')
    from_format = create_adapter('from_')

    def __init__(self, model):
        super().__init__(model)
        self.__register_builtin('boolean')
        self.__register_builtin('binary')
        # self.__register_builtin('estimate')
        self.__register_builtin('integer')
        self.__register_builtin('string')

    def __register_builtin(self, type_name):
        module = import_module(f'.types.{type_name}', __package__)
        self(standard=True, **module.type_def.dict)

    def __call__(
        self,
        name,
        implementation,
        adapters,
        validator,
        attributes,
        exts=None,
        *,
        standard=False,
    ):
        model_type = ModelType(
            name,
            implementation,
            adapters,
            validator,
            attributes,
            exts,
            standard=standard,
        )
        return super().__call__(name, model_type)


def validate(*args, **kwargs):
    return True


class ModelType:
    name: str
    impl: type
    adapters: MutableMapping[str, Adapter]
    validator: Callable[(Any, ), ValidationResult]
    attributes: MutableSequence[Field]
    exts: MutableSequence[TypeExt]

    def __init__(
        self,
        name,
        implementation,
        adapters,
        validator,
        attributes,
        exts,
        standard=False,
    ):
        self.name = name
        self.impl = implementation
        self.adapters = adapters
        self.__validator = validator
        self.attributes = attributes
        self.exts = exts
        self.__standard = standard

    def __call__(self, *args, **kwargs):
        return self.impl(*args, **kwargs)

    def __repr__(self):
        impl = repr(self.impl)
        name = repr(self.name)
        return f'<RegisteredType name={name} implementation={impl}>'

    def __bool__(self):
        return True

    def validate(
            self,
            value: Any,
            required: bool,
            path: DotPath,
            **attrs,
    ):
        if required and value is undefined:
            msg = ValidationMessage(
                ErrorTypes.constraint_error,
                f'"{path}" is required.',
                path,
            )
            return ValidationResult(False, msg)
        elif not isinstance(value, self.impl):
            name = self.name
            txt = TXT(
                '${value} is not valid for the type ${name}.',
                locals(),
            )
            msg = ValidationMessage(ErrorTypes.invalid_value, txt, path)
            return ValidationResult(False, msg)

        else:
            return self.__validator(value, path, **attrs)
