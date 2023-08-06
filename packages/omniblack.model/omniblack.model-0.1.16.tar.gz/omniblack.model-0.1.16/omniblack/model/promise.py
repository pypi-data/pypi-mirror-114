from functools import wraps

from anyio import Event


def to_iter(func):
    @wraps(func)
    def method(*args, **kwargs):
        value = yield from func(*args, **kwargs).__await__()
        return value

    return method


class Promise:
    def __init__(self):
        self.__value = None
        self.__error = None
        self.__event = Event()

    @to_iter
    async def __await__(self):
        await self.__event.wait()
        if self.__error is not None:
            raise self.__error

        return self.__value

    def resolve(self, value):
        if self.__event.is_set():
            raise TypeError('Promise has already been settled')

        self.__value = value
        self.__event.set()

    def reject(self, error):
        if self.__event.is_set():
            raise TypeError('Promise has already been settled')

        self.__error = error
        self.__event.set()
