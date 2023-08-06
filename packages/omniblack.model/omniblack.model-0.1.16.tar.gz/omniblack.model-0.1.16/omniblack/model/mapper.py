from collections.abc import Mapping
from copy import deepcopy
from functools import partial

from .walker import walk


def items(source):
    if isinstance(source, Mapping):
        yield from source.items()
    else:
        for name in source:
            yield name, source[name]


def get(source: Mapping, key: str):
    try:
        source[key]
    except (KeyError):
        return None


def setdefault(source, key, value):
    if key in source:
        return source[key]
    else:
        source[key] = value
        return value


def defaults_deep(dest, *sources: Mapping):
    for source in deepcopy(sources):
        for key, value in items(source):
            dest_value = get(dest, key)
            if isinstance(value, Mapping) and isinstance(dest_value, Mapping):
                defaults_deep(dest_value, value)
            else:
                setdefault(dest, key, value)


def skip(path, value, visited, descended, new_rec, **kwargs):
    if not visited and descended:
        new_values = path.get(new_rec)
        defaults_deep(new_values, value)
    else:
        path.set(new_rec, value)


def map(cb, indiv, filter=None, descend=None, reversed=False):
    new_rec = dict()
    skipped = partial(skip, new_rec=new_rec)
    walker = walk(indiv, filter, descend, skipped=skipped)
    if reversed:
        walker = reversed(walker)

    for field in walker:
        new_value = cb(field)
        path = field.path
        path.set(new_rec, new_value)

    return new_rec
