# @Time     : 2021/7/24
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod

from f1z1_common import ArgsTypes, CoroOrFunction, KwargsTypes, TaskFactory

from ..components.gather import IGather


class IWorkerHandler(metaclass=ABCMeta):
    __slots__ = "_factory"

    @abstractmethod
    def handle(self, gather: IGather) -> None:
        raise NotImplementedError()


class WorkerHandler(IWorkerHandler):
    __slots__ = "_factory"

    def __init__(self,
                 target: CoroOrFunction,
                 args: ArgsTypes = None,
                 kwargs: KwargsTypes = None,
                 thread_workers: int = None):
        self._factory = TaskFactory(
            target, args, kwargs, thread_workers
        )

    def handle(self, gather: IGather):
        gather.put(self._create())

    def _create(self):
        return self._factory.create_task()
