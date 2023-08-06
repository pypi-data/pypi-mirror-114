from collections import ChainMap, OrderedDict, defaultdict, deque
from collections.abc import MutableMapping, MutableSequence, MutableSet
from contextlib import suppress
from dataclasses import fields, is_dataclass
from functools import wraps
from itertools import chain
from warnings import warn

from public import public
from rx import combine_latest
from rx.operators import map as obs_map, switch_latest
from rx.subject import BehaviorSubject

builtin_mutating_methods = (
    '__delattr__',
    '__delete__',
    '__delitem__',
    '__iadd__',
    '__iand__',
    '__ifloordiv__',
    '__ilshift__',
    '__imatmul__',
    '__imod__',
    '__imul__',
    '__ior__',
    '__ipow__',
    '__irshift__',
    '__isub__',
    '__itruediv__',
    '__ixor__',
    '__set__',
    '__setattr__',
    '__setitem__',
)

abcs = {
    MutableMapping: ('pop', 'popitem', 'clear', 'update', 'setdefault'),
    MutableSequence: (
        'append',
        'insert',
        'reverse',
        'extend',
        'pop',
        'remove',
    ),
    MutableSet: ('clear', 'pop', 'remove', 'add', 'discard'),
}


def skip_first(wrapped_func):
    called = False

    @wraps(wrapped_func)
    def wrapper(*args, **kwargs):
        nonlocal called
        if not called:
            called = True
            return

        return wrapped_func(*args, **kwargs)

    return wrapper


@public
class MonitoredAttribute:
    def __set__(self, obj, new_value):
        super_obj = super(obj.__class__, obj.__class__)
        if hasattr(super_obj, self.__name):
            descriptor = getattr(super_obj, self.__name)
            descriptor.__set__(obj, new_value)
        else:
            setattr(obj, self.__set_name)

        obj._observable.on_next(obj)

    def __get__(self, obj, obj_type=None):
        super_obj = super(obj.__class__, obj.__class__)
        if hasattr(super_obj, self.__name):
            descriptor = getattr(super_obj, self.__name)
            return descriptor.__get__(obj, obj_type)
        else:
            if hasattr(obj, self.__set_name):
                return getattr(obj, self.__set_name)
            else:
                raise AttributeError(f'{self.__cls_name} object has no'
                                     f' attribute {self.__name}')

    def __delete__(self, obj):
        super_obj = super(obj.__class__, obj.__class__)
        if hasattr(super_obj, self.__name):
            descriptor = getattr(super_obj, self.__name)
            descriptor.__delete__(obj)
        else:
            delattr(obj, self.__set_name)

        obj._observable.on_next(obj)

    def __set_name__(self, cls, name):
        self.__name = name
        self.__set_name = f'_{self.__class__.__name__}__{name}'
        self.__objclass__ = cls
        self.__cls_name = cls.__name__


def create_monitor_method(method_name, bases):
    for base in bases:
        if hasattr(base, method_name):
            wrapped_func = getattr(base, method_name)
            break
    else:
        raise TypeError(f'Bases do not have the method {method_name}.')

    @wraps(wrapped_func)
    def wrapper(self, *args, **kwargs):
        func = getattr(super(self.__class__, self), method_name)
        ret_val = func(*args, **kwargs)
        self._observable.on_next(self)
        return ret_val

    return wrapper


def create_monitor_methods(methods, bases, missing_ok=False):
    for method_name in methods:
        try:
            yield method_name, create_monitor_method(method_name, bases)
        except TypeError:
            if not missing_ok:
                raise


def create_monitor_attributes(attributes):
    for attribute in attributes:
        yield attribute, MonitoredAttribute()


def monitor__init__(self, *args, **kwargs):
    self._observable = BehaviorSubject(self)
    self.observable = self._observable
    super(self.__class__, self).__init__(*args, **kwargs)


def monitor__del__(self):
    self._observable.on_completed()
    if self.observable is not self._observable:
        if hasattr(self.observable, 'on_completed'):
            self.observable.on_completed

    with suppress(AttributeError):
        super(self.__class__, self).__del__()


@public
def monitor(cls):
    mutating_methods = set(getattr(cls, 'mutating_methods', []))
    mutable_attributes = set(getattr(cls, 'mutable_attributes', []))
    bases = cls.__mro__

    # Filter out any other monitor classes
    bases = tuple(
        base
        for base in bases
        if not hasattr(base, '_MonitorMeta__monitor_class')
    )

    mutating_methods.update(chain.from_iterable(
        base.mutating_methods
        for base in bases
        if hasattr(base, 'mutating_methods')
    ))

    mutable_attributes.update(chain.from_iterable(
        base.mutable_attributes
        for base in bases
        if hasattr(base, 'mutable_attributes')
    ))

    for abc, methods in abcs.items():
        if issubclass(cls, abc):
            mutating_methods.update(methods)

    monitored_methods = chain(
        create_monitor_methods(mutating_methods, bases),
        create_monitor_methods(
            builtin_mutating_methods,
            bases,
            missing_ok=True,
        ),
        create_monitor_attributes(mutable_attributes),
    )

    attrs = dict(
        monitored_methods,
        _MonitorMeta__monitor_class=True,
        __init__=monitor__init__,
        __del__=monitor__del__,
    )

    return type(cls.__name__, bases, attrs)


@public
@monitor
class MonitoredCollection:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        child_monitored = self.child_observables

        if child_monitored:
            combined = combine_latest(self._observable, *child_monitored)
        else:
            combined = self._observable

        self.__combined_observables = BehaviorSubject(combined)
        self.observable = self.__combined_observables.pipe(
            switch_latest(),
            obs_map(lambda value: self),
        )
        self.__subscription = self._observable.subscribe(
            on_next=lambda value: self.__update_combined(),
            on_error=self.__combined_observables.on_error
        )

    def __del__(self):
        self.__subscription.dispose()
        self.__combined_observables.on_completed()

    def __update_combined(self):
        child_monitored = self.child_observables

        if child_monitored:
            combined = combine_latest(self._observable, *child_monitored)
        else:
            combined = self._observable

        self.__combined_observables.on_next(combined)

    @property
    def children(self):
        return iter(self)

    @property
    def child_observables(self):
        return tuple(map(
            self.get_observable,
            filter(self.is_observable, self.children),
        ))

    def is_observable(self, value):
        return hasattr(value, 'observable')

    def get_observable(self, value):
        return getattr(value, 'observable')


@public
@monitor
class MonitoredList(MonitoredCollection, list):
    mutating_methods = ('sort', )


@public
@monitor
class MonitoredDeque(MonitoredCollection, deque):
    mutating_methods = (
        'appendleft',
        'extendleft',
        'popleft',
        'rotate',
    )


@public
@monitor
class MonitoredDict(MonitoredCollection, dict):
    @property
    def children(self):
        return self.values()


@public
@monitor
class MonitoredDefaultDict(MonitoredCollection, defaultdict):
    @property
    def children(self):
        return self.values()


@public
@monitor
class MonitoredOrderedDict(MonitoredCollection, OrderedDict):
    mutating_methods = (
        'popitem',
        'move_to_end',
    )

    @property
    def children(self):
        return self.values()


@public
@monitor
class MonitoredChainMap(ChainMap):
    mutating_methods = ('new_child', )
    mutable_attributes = ('parents', )

    def __init__(self, *args, child_cls=MonitoredDict, **kwargs):
        self.__child_subscription = None
        self.child_cls = child_cls
        super().__init__(*args, **kwargs)

    def __del__(self):
        if self.__child_subscription is not None:
            self.__child_subscription.dispose()

    @property
    def maps(self):
        return self.__maps

    @maps.setter
    def maps(self, new_value):
        self.__child_subscription.dispose()
        new_value = map(self.convert_monitored_dict, new_value)
        self.__maps = MonitoredList(new_value)
        self.__child_subscription = self.__maps.observable.subscribe(
            on_next=self.__monitor_maps,
            on_error=lambda err: self.observable.on_error(err),
        )

    def __monitor_maps(self, new_maps):
        need_update = any(
            not isinstance(map, self.dict_cls)
            for map in new_maps
        )

        if need_update:
            self.maps = new_maps

    def new_child(self, m=None):
        if m is None:
            m = {}

        m = self.child_cls(m)
        return self.__class__(m, *(
            self.child_cls(map)
            for map in self.maps
        ), child_cls=self.child_cls)

    @property
    def children(self):
        return (self.maps, )

    def convert_monitored_dict(self, value):
        if isinstance(value, self.child_cls):
            return value
        else:
            return self.child_cls(value)


@public
def monitor_dataclass(dataclass):
    if not is_dataclass(dataclass):
        raise TypeError(
            "'monitor_dataclass' may only be called on a dataclass class",
        )
    class_fields = fields(dataclass)
    try:
        frozen = dataclass.__dataclass_params__.frozen
    except AttributeError:
        frozen = False
        warn(
            'Frozen dataclass detection has failed, this relied upon an'
            ' undocumented feature of dataclasses. Please contact the'
            ' the developers so we can look at updating the frozen dataclass'
            ' detection.'
        )

    if frozen:
        raise TypeError('Frozen dataclasses cannot be monitored')

    mutable_attributes = set(dataclass.mutable_attributes)
    mutable_attributes.update(
        field.name
        for field in class_fields
    )
    dataclass.mutable_attributes = tuple(mutable_attributes)
    return monitor(dataclass)
