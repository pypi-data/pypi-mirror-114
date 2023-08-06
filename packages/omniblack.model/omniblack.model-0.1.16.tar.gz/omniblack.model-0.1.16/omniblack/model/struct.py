from __future__ import annotations

from collections.abc import Mapping
from functools import partial, wraps
from importlib import import_module
from importlib.resources import contents, open_text
from itertools import chain, groupby
from json import load
from operator import attrgetter, getitem, methodcaller
from pathlib import Path
from typing import TYPE_CHECKING, Union

from anyio import Lock, create_task_group
from anyio.to_thread import run_sync
from public import public
from rx import combine_latest
from rx.operators import map

from .abc import Registry
from .dot_path import DotPath
from .field import Field, UiString
from .format import Format, get_preferred_file
from .preprocess_struct import preprocess_struct_def
from .promise import Promise
from .undefined import undefined

if TYPE_CHECKING:
    from .model import Model

bases_path = DotPath(('implementation', 'python', 'bases'))

with open_text('omniblack.model.structs', 'struct.json') as struct_def_file:
    # The struct def of struct
    struct_struct_def = load(struct_def_file)


def is_ui_string(field):
    return (
        field['type'] == 'child'
        and field['attrs']['struct_name'] == 'ui_string'
    )


root_ui_string = {
    field['name']
    for field in struct_struct_def['fields']
    if is_ui_string(field)
}

struct_fields = tuple(field['name'] for field in struct_struct_def['fields'])


def import_base(base_str):
    module_id, name = base_str.split(':')
    module = import_module(module_id)
    return getattr(module, name)


class StructMeta(type):
    def __new__(
            cls,
            name,
            bases,
            attrs: dict,
            struct_def: dict,
            model: Model,
            is_base=False,
    ):
        model_bases = (
            import_base(base)
            for base in bases_path.get(struct_def, tuple())
        )
        final_bases = tuple(chain(model_bases, bases))

        fields = []
        if not is_base:
            attrs['_Struct__model'] = model
            for field in struct_def['fields']:
                field_name = field['name']
                field_descriptor = Field(**field, _model=model)
                fields.append(field_descriptor)
                attrs[field_name] = field_descriptor

            attrs['_Struct__fields'] = tuple(fields)
        # When the name of a field collides with a name
        # of a field from struct we store the value in
        # _Field__class_values and the field descriptor
        # will look it up when used on the class
        attrs['_Field__class_values'] = {}
        for field_name, value in struct_def.items():
            if field_name in root_ui_string:
                value = UiString(**value)

            if field_name in attrs:
                # The field descriptor know to check for this attribute
                # When being used on the class
                attrs['_Field__class_values'][field_name] = value
            else:
                attrs[field_name] = value

        return super().__new__(
            cls,
            name,
            final_bases,
            attrs,
        )

    def __repr__(cls):
        name = cls.name

        values = tuple(
            f'{name}={repr(getattr(cls, name, None))}'
            for name in struct_fields
        )
        values_str = ', '.join(values)

        return f'{name}({values_str})'


@public
def get_indiv_observable(indiv):
    return indiv._Struct__value_subject


@public
def indiv_fields(indiv):
    return indiv.__class__._Struct__fields


@public
def get_path(indiv):
    return indiv._Struct__path


@public
def get_model(indiv):
    return indiv._Struct__model


@public
def get_struct_name(indiv):
    return type(indiv).name


class Struct(
        metaclass=StructMeta,
        struct_def=struct_struct_def,
        is_base=True,
        model=None,
):
    def __init__(self, values=None, *, is_base=False, **kwargs):
        self.__path = DotPath()
        if values is None or values is undefined:
            values = {}

        values |= kwargs

        if not is_base:
            cls = self.__class__
            self._Field__field_info = {}

            self.__value_subjects = {}
            for field in cls.__fields:
                value_subject, = field.init_indiv(
                    self,
                    values.get(field.name, undefined),
                )
                self.__value_subjects[field.name] = value_subject

            self.__value_subject = combine_latest(
                *self.__value_subjects.values()
            ).pipe(
                map(lambda items: self)
            )

        super().__init__()

    def __repr__(self):
        cls = self.__class__
        name = cls.__name__

        values = tuple(
            f'{field.name}={repr(getattr(self, field.name, undefined))}'
            for field in cls.__fields
        )

        values_str = ', '.join(values)

        return f'{name}({values_str})'

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __eq__(self, other):
        if not isinstance(other, Struct):
            return NotImplemented

        cls = self.__class__

        for field in cls.__fields:
            try:
                self_value = self[field.name]
            except KeyError:
                self_value = undefined

            try:
                other_value = other[field.name]
            except KeyError:
                other_value = undefined

            if self_value != other_value:
                return False
        else:
            return True

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError as err:
            raise KeyError(*err.args) from None

    def __setitem__(self, key, value):
        try:
            return setattr(self, key, value)
        except AttributeError as err:
            raise KeyError(*err.args) from None

    def __delitem__(self, key):
        try:
            return delattr(self, key)
        except AttributeError as err:
            raise KeyError(*err.args) from None

    def __iter__(self):
        cls = self.__class__
        for field in cls.__fields:
            if field.name in self:
                yield field.name

    def __reversed__(self):
        cls = self.__class__
        for field in reversed(cls.__fields):
            if field.name in self:
                yield field.name

    def __copy__(self):
        cls = self.__class__
        values = {}
        for field in cls.__fields:
            try:
                values[field.name] = self[field.name]
            except KeyError:
                pass

        return cls(**values)

    def __set_path(self, path: DotPath):
        self.__path = path

    def __deepcopy__(self, memo):
        from copy import deepcopy
        cls = self.__class__
        values = {}
        for field in cls.__fields:
            try:
                values[field.name] = deepcopy(self[field.name], memo)
            except KeyError:
                pass

        return cls(**values)

    @classmethod
    async def load_file(cls, file: Path):
        return await run_sync(cls.load_file_sync, file)

    @classmethod
    def load_file_sync(cls, file: Path):
        model = cls.__model
        format = model.formats.by_suffix[file.suffix]
        with file.open() as file_obj:
            rec = format.load(file_obj)
            indiv = model.coerce_from(rec, format, cls.name)
            return indiv


def async_cache(func):
    cache = {}

    @wraps(func)
    async def cache_func(*args):
        if args in cache:
            return await cache[args]

        future = func(*args)
        cache[args] = future
        try:
            return await future
        except Exception:
            del cache[args]
            raise

    return cache_func


@async_cache
async def get_contents(package, model: Model):
    resources = await run_sync(contents, package)

    resources = (
        Path(resource)
        for resource in resources
        if Path(resource).suffix in model.formats.by_suffix
    )

    return tuple(
        get_preferred_file(files, model)
        for name, files in groupby(resources, attrgetter('stem'))
    )


def is_loadable(path, model):
    return path.suffix in model.formats.by_suffix


@public
class StructRegistry(Registry):
    def __init__(self, model):
        super().__init__(model)
        self.__loading_structs = {}
        self.__struct_locations = {}
        self.__struct_loading_lock = Lock()

    async def __call__(self, struct_def: Union[str, dict], *bases):
        meta_structs, = preprocess_struct_def(struct_def)
        async with create_task_group() as tg:
            for struct_name in meta_structs:
                tg.start_soon(
                    self.load_meta_struct,
                    struct_name,
                )

        name = struct_def['name']
        return super().__call__(name,  StructMeta(
            name,
            chain((Struct, ), bases),
            {},
            struct_def=struct_def,
            model=self.__model,
        ))

    async def load_meta_struct(self, struct_name):
        if struct_name in self:
            return self[struct_name]

        struct_def = await self.load_struct_def_resource(
            Path(struct_name).with_suffix('.json'),
            'omniblack.model.structs',
        )

        child_fields = filter(
            lambda field: field['type'] == 'child',
            struct_def.fields,
        )

        async with create_task_group() as tg:
            for child_field in child_fields:
                tg.start_soon(
                    self.load_meta_struct,
                    child_field['attrs']['struct_name'],
                )

        return self[struct_name]

    async def load_model_dir(self, dir: Path):
        async with create_task_group() as tg:
            dir_iter = filter(methodcaller('is_file'), dir.iterdir())
            dir_iter = filter(
                partial(is_loadable, model=self.__model),
                dir_iter,
            )
            sort_dir_iter = partial(sorted, dir_iter, key=attrgetter('stem'))
            dir_iter = await run_sync(sort_dir_iter)

            for name, paths in groupby(dir_iter, attrgetter('stem')):
                path = get_preferred_file(paths, self.__model)
                tg.start_soon(self.load_struct_def_file, path)

    async def load_model_package(self, package):
        async with create_task_group() as tg:
            for resource in await get_contents(package, self.__model):
                tg.start_soon(
                    self.load_struct_def_resource,
                    resource,
                    package,
                )

    async def load_struct_def_file(self, path):
        name = path.stem
        existing_prom = None
        promise = Promise()

        async with self.__struct_loading_lock:
            if name in self.__loading_structs:
                if self.__struct_locations[name] != path:
                    raise ValueError(
                        f'Conflicting paths found for {name}.'
                        ' Structs may not be loaded twice.',
                        path,
                        self.__struct_locations[name]
                    )

                existing_prom = self.__loading_structs[name]
            else:
                self.__loading_structs[name] = promise
                self.__struct_locations[name] = promise

        if existing_prom is not None:
            return await existing_prom

        try:
            format = self.__model.formats.by_suffix[path.suffix]
            struct_def = await run_sync(
                self.load_file,
                path,
                format,
            )

            struct_cls = await self(struct_def)
        except Exception as err:
            promise.reject(err)
            raise

        promise.resolve(struct_cls)
        return struct_cls

    async def load_struct_def_resource(self, resource_path, package):
        struct_name = resource_path.name
        promise = Promise()
        existing_prom = None
        async with self.__struct_loading_lock:
            if struct_name in self.__loading_structs:
                if package != self.__struct_locations[struct_name]:
                    raise ValueError(
                        f'Conflicting paths found for {struct_name}.'
                        ' Structs may not be loaded twice.',
                        (resource_path, package),
                        self.__struct_locations[struct_name]
                    )

                existing_prom = self.__loading_structs[struct_name]
            else:
                self.__loading_structs[struct_name] = promise
                self.__struct_locations[struct_name] = resource_path

        if existing_prom is not None:
            return await existing_prom

        try:
            format = self.__model.formats.by_suffix[resource_path.suffix]
            struct_def = await run_sync(
                self.load_resource,
                resource_path,
                package,
                format,
            )

            struct_cls = await self(struct_def)
            promise.resolve(struct_cls)
            return struct_cls
        except Exception as err:
            promise.reject(err)
            raise

    def load_resource(self, resource: Path, package: str, format: Format):
        with open_text(package, str(resource)) as file_obj:
            return format.load(file_obj)

    def load_file(self, path: Path, format: Format):
        with open(path) as file_obj:
            return format.load(file_obj)


class ChildField(Field, type='child'):
    def init_indiv(self, indiv, value=undefined):
        parent_path = get_path(indiv)
        path = parent_path | self.name
        struct_name = self.attrs['struct_name'].removeprefix('meta:')
        struct_cls = self._model.structs[struct_name]
        child_indiv = struct_cls(value)
        child_indiv._Struct__set_path(path)
        subject = get_indiv_observable(child_indiv)
        return super().init_indiv(indiv, child_indiv, _subject=subject)

    def __set__(self, parent_indiv, new_value):
        info = self.get_info(parent_indiv)
        indiv = info.current_value
        if new_value is not undefined:
            getter = (
                getitem
                if isinstance(new_value, Mapping)
                else getattr
            )

            for field in indiv_fields(indiv):
                try:
                    indiv[field.name] = getter(new_value, field.name)
                except (KeyError, AttributeError):
                    del indiv[field.name]
        else:
            for field in indiv_fields(indiv):
                del indiv[field.name]
