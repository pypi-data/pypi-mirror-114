from collections import UserDict
from reprlib import recursive_repr
from weakref import finalize


class Id(int):
    def __new__(cls, obj):
        super().__new__(cls, id(obj))


class NoQuoteStr(str):
    def __repr__(self):
        return self


class IdDict(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__finalizers = {}
        self.__names = {}

    def __getitem__(self, key):
        key_id = self.__get_id(key)
        return self.data[key_id]

    def __setitem__(self, key, value):
        key_id = self.__get_id(key)
        finalizer = finalize(key, self.__del_key, key_id)
        # this is only for memory management we don't care once
        # interpreter shutdown starts
        finalizer.atexit = False
        type_name = type(key).__name__
        self.__names[key_id] = type_name
        self.data[key_id] = value
        self.__finalizers[key_id] = finalizer

    def __delitem__(self, key):
        key_id = self.__get_id(key)
        self.__del_key(key_id)

    def __get_id(self, key):
        if isinstance(key, Id):
            return key
        else:
            return Id(key)

    def __del_key(self, key_id):
        try:
            del self.data[key_id]
        except KeyError:
            pass

        try:
            finalizer = self.__finalizers[key_id]
            finalizer.detach()
            del self.__finalizers[key_id]
        except KeyError:
            pass

        try:
            del self.__names[key_id]
        except KeyError:
            pass

    def __get_id_repr(self, key_id):
        finalizer = self.__finalizers[key_id]
        obj, func, args, kwargs = finalizer.peek()
        return NoQuoteStr(repr(obj))

    @recursive_repr()
    def __repr__(self):
        repr_dict = {
            self.__get_id_repr(key_id): value
            for key_id, value in self.items()
        }
        return f'{self.__class__.__name__}({repr(repr_dict)})'
