from functools import wraps
from itertools import chain


def partial(func, *args, **kwargs):
    @wraps(func)
    def wrapper(*new_args, **new_kwargs):
        return func(*new_args, *args, **kwargs, **new_kwargs)

    return wrapper


default_slots = ('__weakref__', )


def slots(cls, *dec_slots):
    if not isinstance(cls, type):
        return partial(slots, cls, *dec_slots)

    descriptor_slots = tuple(chain.from_iterable(
        attr.descriptor_slots
        for attr in vars(cls).values()
        if hasattr(attr, 'descriptor_slots')
    ))

    parent_slots = set(chain.from_iterable(
        parent_class.__slots__
        for parent_class in cls.__mro__
        if hasattr(parent_class, '__slots__')
    ))

    cls_slots = getattr(cls, '__slots__', tuple())
    cls_slots = set(chain(dec_slots, cls_slots, descriptor_slots))

    final_slots = tuple(cls_slots - parent_slots)

    try:
        del cls.__slots__
    except AttributeError:
        pass

    new_attrs = dict(cls.__dict__, __slots__=final_slots)
    return type(cls.__name__, cls.__mro__, new_attrs)
