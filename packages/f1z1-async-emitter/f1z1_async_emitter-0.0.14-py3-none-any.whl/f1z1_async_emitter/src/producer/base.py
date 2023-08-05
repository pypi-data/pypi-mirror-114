# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from typing import TypeVar

"""
生产侧接口
"""

T = TypeVar("T")


class IWorker(metaclass=ABCMeta):
    """
    worker interface
    """

    @abstractmethod
    async def start(self) -> T:
        raise NotImplementedError("NotImplemented .start() -> T")


class IWorkerMaster(metaclass=ABCMeta):
    """
    worker master interface
    """

    @abstractmethod
    def add(self, worker: IWorker):
        raise NotImplementedError("NotImplemented .add(worker_or_group)")

    @abstractmethod
    def start(self) -> T:
        raise NotImplementedError("NotImplemented .start() -> T")


class IWorkerFactory(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs) -> T:
        raise NotImplementedError("NotImplemented .create() -> T")
