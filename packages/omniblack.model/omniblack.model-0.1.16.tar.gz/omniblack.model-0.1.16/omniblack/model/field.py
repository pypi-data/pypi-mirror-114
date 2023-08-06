from __future__ import annotations

from collections.abc import Container, Mapping
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

from public import public
from rx.subject import BehaviorSubject

from .undefined import undefined


@public
class UiString(Mapping):
    __slots__ = ('en', 'es', 'fr')

    def __iter__(self):
        for key in self.__slots__:
            if self[key]:
                yield key

    def __getitem__(self, key):
        return getattr(self, key)

    def __len__(self):
        length = 0
        for key in self.__slots__:
            if self[key]:
                length += 1

        return length

    def __delattr__(self, key):
        setattr(self, key, None)

    def __init__(self, en, es=None, fr=None):
        self.en = en
        self.es = es
        self.fr = fr

    def __repr__(self):
        cls_name = self.__class__.__name__
        attrs = (f"{key}={repr(value)}"
                 for key, value in self.items())

        attr_str = ', '.join(attrs)
        return f'{cls_name}({attr_str})'

    en: str
    es: str
    fr: str


class DistinctSubject(BehaviorSubject):
    def on_next(self, value):
        if value != self.value:
            return super().on_next(value)


@dataclass
class InstanceInfo:
    current_value: Any = undefined
    value_subject: DistinctSubject = None

    def __post_init__(self):
        if self.value_subject is None:
            self.value_subject = DistinctSubject(self.current_value)

    def __del__(self):
        """
            Cleanup the subjects.
        """
        try:
            self.value_subject.on_completed()
        except AttributeError:
            pass

        try:
            self.value_subject.dispose()
        except AttributeError:
            pass


def sort_overrides(item):
    key, cls = item
    return len(key)


@public
class Field:
    name: str
    display: UiString
    list: bool
    required: bool
    type: str
    default: Any
    attrs: SimpleNamespace  # This is dynamic depending on the type
    valid_values: Container

    __type_overrides = {}

    descriptor_slots = ('_Field__field_info', )

    def __init_subclass__(
        cls,
        /,
        *,
        type=undefined,
        list=undefined,
        **kwargs,
    ):
        super().__init_subclass__(**kwargs)

        keys = {}
        if type is not undefined:
            keys['type'] = type

        if list is not undefined:
            keys['list'] = list

        key = tuple(keys.items())

        all_overrides = tuple(Field.__type_overrides.items()) + ((key, cls),)
        Field.__type_overrides = dict(
            sorted(all_overrides, key=sort_overrides, reverse=True)
        )

    def __new__(cls, *args, **kwargs):
        for requirements, override in Field.__type_overrides.items():
            matches = all(
                kwargs.get(name, None) == value
                for name, value in requirements
            )

            if matches:
                cls = override
                break

        return super().__new__(cls)

    def __init__(
        self,
        *,
        name,
        display,
        desc,
        type,
        attrs=undefined,
        valid_values=undefined,
        list=undefined,
        assumed=undefined,
        default=undefined,
        required=undefined,
        _model=None,
    ):
        self.name = name
        self.display = UiString(**display)
        self.desc = UiString(**desc)
        self.type = type
        self.attrs = attrs
        self.valid_values = valid_values
        self.default = default
        self.assumed = assumed
        self.__list = list
        self.__required = required
        self._model = _model

    def __set_name__(self, owner, name):
        # objclass helps with inspecting the object
        self.__objclass__ = owner

    @property
    def required(self):
        return (
            self.__required
            if self.__required is not undefined
            else False
        )

    @required.setter
    def required(self, new_value):
        self.__required = new_value

    @required.deleter
    def required(self):
        self.__required = undefined

    @property
    def list(self):
        return (
            self.__list
            if self.__list is not undefined
            else False
        )

    @list.setter
    def list(self, new_value):
        self.__list = new_value

    @list.deleter
    def list(self):
        self.__list = undefined

    def __get__(self, obj, obj_type):
        if obj is None:
            try:
                return obj_type.__class_values[self.name]
            except KeyError:
                name = obj_type.__name__
                raise AttributeError(
                    f'{name} does not have the attribute {self.name}.'
                )

        instance_info = self.get_info(obj)
        value = instance_info.current_value
        if value is undefined:
            if self.assumed is not undefined:
                return self.assumed
            else:
                raise AttributeError(f'{self.name} is not set.')
        else:
            return value

    def get_info(self, indiv):
        return indiv.__field_info[self.name]

    def __set__(self, obj, new_value):
        instance_info = self.get_info(obj)
        instance_info.current_value = new_value
        # we use get so that assumed values are used correctly
        try:
            final_value = self.__get__(obj, None)
        except AttributeError:
            final_value = undefined

        instance_info.value_subject.on_next(final_value)

    def __delete__(self, obj):
        self.__set__(obj, undefined)

    def init_indiv(self, indiv, value=undefined, _subject=None):
        """
            Create the state information for one indiv of this field.
            Params:
                indiv: The indiv this subject and value should be associated
                    with.
                value: The initial value of the field.
            Returns a named tuple of value_subject, valid_subject.
                These subjects will be completed and disposed when the
                indiv is gc-ed.
        """
        instance_info = InstanceInfo(value, value_subject=_subject)
        indiv.__field_info[self.name] = instance_info
        self.__set__(indiv, value)
        return (instance_info.value_subject, )

    def __repr__(self):
        cls = self.__class__
        cls_name = cls.__name__
        values = (
            f'{name}={repr(getattr(self, name, None))}'
            for name in (
                'attrs',
                'desc',
                'display',
                'list',
                'name',
                'required',
                'type',
                'valid_values',
            )
            if getattr(self, name, None) is not None
            if getattr(self, name, None) is not undefined
        )
        value_str = ', '.join(values)
        return f'{cls_name}({value_str})'


@public
class ListField(Field, list=True):
    pass
