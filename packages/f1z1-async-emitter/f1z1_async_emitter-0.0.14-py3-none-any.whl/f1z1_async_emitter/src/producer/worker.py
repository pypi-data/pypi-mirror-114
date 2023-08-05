# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from typing import Iterable

from ..components.counter import IAsyncCountGenerator
from ..components.gather import IAwaitBuffer, IGather
from ..components.record import IRecorder
from ..components.speed import IAwaitSpeed
from ..components.timeout import ITimeout
from ..customer import WorkerJoin
from .handler import IWorkerHandler, WorkerHandler


class IWorker(metaclass=ABCMeta):
    """
    worker interface
    """

    @abstractmethod
    async def start(self) -> IRecorder:
        raise NotImplementedError("NotImplemented .start() -> T")


class CounterWorker(IWorker):
    """
    设置总量 worker
    """

    def __init__(self,
                 handler: IWorkerHandler,
                 counter: IAsyncCountGenerator,
                 gather: IGather,
                 recorder: IRecorder):
        self._handler = handler
        self._counter = counter
        self._gather = gather
        self._recorder = recorder

    async def start(self):
        gather = self._gather
        handle = self._handler.handle
        async for index in self._counter:
            handle(gather)

        # 交由消费侧
        return await self.join(gather)

    async def join(self, gather: IGather):
        worker_join = WorkerJoin(self._recorder, gather)
        return await worker_join.join()

    def __str__(self):
        return "{__class__.__name__}(counter={counter}, gather={gather})".format(
            __class__=self.__class__,
            counter=self._counter,
            gather=self._gather,
        )


class TimeoutWorker(IWorker):
    """
    超时 worker
    """

    def __init__(self,
                 handler: IWorkerHandler,
                 gather: IGather,
                 recorder: IRecorder,
                 speed: IAwaitSpeed,
                 timeout: ITimeout):
        self._handler = handler
        self._gather = gather
        self._recorder = recorder
        self._speed = speed
        self._timeout = timeout

    async def start(self) -> IRecorder:
        gather = self._gather
        handle = self._handler.handle
        speed = self._speed
        is_timeout = self._timeout.is_timeout
        self._timeout.start()
        while not is_timeout():
            handle(gather)
            await speed
        return await self.join(gather)

    async def join(self, gather: IGather):
        worker_join = WorkerJoin(self._recorder, gather)
        return await worker_join.join()

    def __str__(self):
        return "{__class__.__name__}(timeout={timeout}, gather={gather})".format(
            __class__=self.__class__,
            gather=self._gather,
            timeout=self._timeout
        )


class WorkerGroup(IWorker):

    def __init__(self,
                 buffer: IAwaitBuffer,
                 gather: IGather,
                 recorder: IRecorder):
        """

        :param buffer:
        :param gather:
        :param recorder:
        """
        self._buffer = buffer
        self._gather = gather
        self._recorder = recorder

    def stuff(self, workers: Iterable[IWorker]) -> None:
        filtered = self._filter(workers)
        self._buffer.put(filtered)

    async def start(self):
        gather = self._gather
        async for worker in self._buffer:
            self._put(worker, gather)
        # 交由消费侧
        return await self.join(gather)

    async def join(self, gather: IGather):
        worker_join = WorkerJoin(self._recorder, gather)
        return await worker_join.join()

    def _put(self, worker: IWorker, gather: IGather):
        handler = WorkerHandler(
            worker.start
        )
        handler.handle(gather)

    def _filter(self, workers: Iterable[IWorker]):
        """
        过滤 worker
        :param workers:
        :return:
        """
        return (worker for _, worker in enumerate(workers) if self._is_worker(worker))

    def _is_worker(self, value):
        return isinstance(value, IWorker)

    def __str__(self):
        return f"{self.__class__.__name__}(workers={self._buffer.length()})"


def is_worker(value):
    return isinstance(value, IWorker)
