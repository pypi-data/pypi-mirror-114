from collections import defaultdict
from functools import partial
from typing import Any, NamedTuple

from public import public

from .dot_path import DotPath
from .field import Field
from .struct import get_path
from .undefined import undefined


@public
class WalkerYield(NamedTuple):
    value: Any
    field_def: Field
    path: DotPath
    root_value: Any

    @property
    def dict(self):
        return self._asdict()


@public
class walk:
    def __init__(
            self,
            indiv,
            filter=None,
            descend=None,
            skipped=None,
            path=None,
            struct_def=None,
            _root_value=None,
    ):
        self.indiv = indiv
        self.filter = filter
        self.descend = descend
        self.skipped = skipped
        self.__root_value = _root_value if _root_value is not None else indiv

        self.path = path if path is not None else get_path(indiv)
        self.struct_def = struct_def if struct_def is not None else type(indiv)

    def should_descend(self, *args, **kwargs):
        if self.descend:
            return self.descend(*args, **kwargs)
        else:
            return True

    def should_visit(self, *args, **kwargs):
        if self.filter:
            return self.filter(*args, **kwargs)
        else:
            return True

    def notify_skip(self, field_def, descended, visited, *args, **kwargs):
        if self.skipped:
            is_child = field_def['type'] == 'child'
            if (not visited) or (is_child and not descended):
                return self.skipped(
                    *args,
                    field_def=field_def,
                    descended=descended,
                    visited=visited,
                    **kwargs,
                )
        else:
            return True

    def __iter__(self):
        for field in self.struct_def.fields:
            name = field['name']
            field_path = self.path | name

            try:
                value = self.indiv[name]
            except KeyError:
                value = undefined

            yield_value = WalkerYield(
                value=value,
                field_def=field,
                path=field_path,
                root_value=self.__root_value,
            )

            visited = self.should_visit(yield_value)
            is_child = field['type'] == 'child'
            descended = is_child and self.should_descend(yield_value)

            if visited:
                yield yield_value

            if descended:
                yield from walk(
                    indiv=value,
                    filter=self.filter,
                    descend=self.descend,
                    skipped=self.skipped,
                    _root_value=self.__root_value,
                )

            self.notify_skip(
                **yield_value.dict,
                visited=visited,
                descended=descended,
            )

    def down_skip(self, skips, descended, path, **kwargs):
        skips[path] = descended

    def down_should_visit(self, skips, node_information: WalkerYield):
        visited = self.should_visit(node_information)

        descended = skips[node_information.path]

        self.notify_skip(
            **node_information.dict,
            visited=visited,
            descended=descended,
        )

    def __reversed__(self):
        skips = defaultdict(lambda: True)
        down_skipped = partial(self.down_skip, skips)
        fields = tuple(walk(
            indiv=self.indiv,
            descend=self.descend,
            skipped=down_skipped,
        ))

        fields = reversed(fields)

        yield from filter(fields, partial(self.down_should_visit, skips))


@public
def visit_leaves(info: WalkerYield):
    field_def = info.field_def
    return field_def['type'] != 'child'
