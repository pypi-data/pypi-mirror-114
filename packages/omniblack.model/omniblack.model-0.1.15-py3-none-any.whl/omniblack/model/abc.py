from abc import ABC, abstractmethod
from collections.abc import Mapping

from public import public


@public
class Localizable(ABC):
    @abstractmethod
    def localize(lang: str) -> str:
        pass


# Strings are considered localizeable so that double localization does not
# cause errors
Localizable.register(str)


@public
class Registry(Mapping):
    def __init__(self, model):
        self.__model = model
        cls_name = self.__class__.__name__
        setattr(self, f'_{cls_name}__model', model)
        self.__data = {}

    def __getitem__(self, key):
        return self.__data[key]

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as err:
            raise AttributeError(*err.args) from None

    def __repr__(self):
        cls_name = self.__class__.__name__
        data_repr = ', '.join(self.keys())
        return f'{cls_name}({data_repr})'

    def __iter__(self):
        return iter(self.__data)

    def __len__(self):
        return len(self.__data)

    def __contains__(self, key):
        return key in self.__data

    def __reversed__(self):
        return reversed(self.__data)

    def __bool__(self):
        return bool(self.__data)

    def __call__(self, name, item):
        self.__data[name] = item
        return item

    def keys(self):
        return self.__data.keys()

    def items(self):
        return self.__data.items()

    def values(self):
        return self.__data.values()

    def get(self, key, default=None):
        return self.__data.get(key, default)
