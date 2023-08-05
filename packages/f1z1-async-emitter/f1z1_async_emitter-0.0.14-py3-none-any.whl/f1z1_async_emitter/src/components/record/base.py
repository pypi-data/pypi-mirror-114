# @Time     : 2021/7/24
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from typing import Iterable, TypeVar

T = TypeVar("T")


class IRecorder(metaclass=ABCMeta):
    """
    recorder interface
    save result
    """

    @abstractmethod
    def length(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def empty(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def save(self, result: T) -> None:
        raise NotImplementedError("NotImplemented .save(result) -> None")

    @abstractmethod
    def __iter__(self) -> Iterable[T]:
        raise NotImplementedError("NotImplemented .__iter__() -> Iterable[T]")
