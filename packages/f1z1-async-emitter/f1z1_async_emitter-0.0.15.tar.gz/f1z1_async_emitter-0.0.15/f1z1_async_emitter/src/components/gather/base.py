# @Time     : 2021/7/24
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from typing import Iterable, AsyncIterable, List, TypeVar, Union

T = TypeVar("T")
IterOrList = Union[Iterable[T], List[T]]


class IAwaitBuffer(metaclass=ABCMeta):
    """
    await buffer
    This's a support __aiter__ of Product Queue
    It support set get speed
    """

    @abstractmethod
    def put(self, iter_or_list: IterOrList) -> None:
        """
        put  iter_or_list
        :param iter_or_list:
        :return:
        """
        raise NotImplementedError("NotImplemented .put(emitter)")

    @abstractmethod
    def pop(self) -> T:
        """
        get emitter
        :return:
        """
        raise NotImplementedError("NotImplemented .get() -> IEmitter")

    @abstractmethod
    def length(self) -> int:
        raise NotImplementedError("")

    @abstractmethod
    def empty(self) -> bool:
        """
        queue empty()
        :return:
        """
        raise NotImplementedError("NotImplemented .empty() -> bool")

    @abstractmethod
    async def __aiter__(self) -> AsyncIterable[T]:
        """
        async iter IEmitter
        :return:
        """
        raise NotImplementedError("NotImplemented .__iter__() -> AsyncIterable[T]")


class IGather(metaclass=ABCMeta):
    """
    task gather

    This's a support __iter__ of Costume Queue
    """

    @abstractmethod
    def length(self) -> int:
        raise NotImplementedError("")

    @abstractmethod
    def empty(self) -> bool:
        raise NotImplementedError("")

    @abstractmethod
    def put(self, item: T) -> None:
        raise NotImplementedError("NotImplemented .put(task) -> None")

    @abstractmethod
    def pop(self) -> T:
        raise NotImplementedError("NotImplemented .pop() -> Task")

    def __iter__(self) -> Iterable[T]:
        raise NotImplementedError("NotImplemented __iter__() -> Iterable[Task]")
