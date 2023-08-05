# @Time     : 2021/7/24
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod


class ITimeout(metaclass=ABCMeta):
    __slots__ = "_st", "_timeout", "_unit"

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def is_timeout(self) -> bool:
        raise NotImplementedError()
