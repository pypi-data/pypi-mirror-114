# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from typing import Union
from functools import wraps

from f1z1_common import ArgsTypes, CoroOrFunction, KwargsTypes, UnitOfTime

from ..components.counter import AsyncCountGenerator
from ..components.gather import QueueGather
from ..components.record import Recorder
from ..components.speed import Speed
from ..components.timeout import Timeout
from .base import IWorker
from .handler import WorkerHandler
from .worker import CounterWorker, TimeoutWorker

IntOrFloat = Union[int, float]


class AbstractWorkerDecorate(metaclass=ABCMeta):

    def __init__(self,
                 speed: IntOrFloat,
                 speed_unit: UnitOfTime = UnitOfTime.MILLISECOND,
                 thread_workers: int = None):
        self._gather = QueueGather(2 ** 31)
        self._recorder = Recorder()
        self._speed = Speed(speed, speed_unit)
        self._thread_workers = thread_workers

    def __call__(self, function: CoroOrFunction):
        d = self

        @wraps(function)
        def _wrapper(*args, **kwargs):
            return d._create_worker(
                d._handler(function, args=args, kwargs=kwargs)
            )

        return _wrapper

    @abstractmethod
    def _create_worker(self, handler) -> IWorker:
        raise NotImplementedError("")

    def _handler(self,
                 function: CoroOrFunction,
                 args: ArgsTypes = None,
                 kwargs: KwargsTypes = None):
        return WorkerHandler(
            function,
            args=args,
            kwargs=kwargs,
            thread_workers=self._thread_workers
        )


class CounterWorkerDecorate(AbstractWorkerDecorate):
    def __init__(self,
                 count: int,
                 speed: IntOrFloat,
                 speed_unit: UnitOfTime = UnitOfTime.MILLISECOND,
                 thread_workers: int = None):
        super().__init__(speed, speed_unit, thread_workers)
        self._counter = AsyncCountGenerator(count, self._speed)

    def _create_worker(self, handler):
        return CounterWorker(
            handler,
            counter=self._counter,
            gather=self._gather,
            recorder=self._recorder
        )


class TimeoutWorkerDecorate(AbstractWorkerDecorate):
    def __init__(self,
                 timeout: IntOrFloat,
                 speed: IntOrFloat,
                 speed_unit: UnitOfTime = UnitOfTime.MILLISECOND,
                 thread_workers: int = None):
        super().__init__(speed, speed_unit, thread_workers)
        self._timeout = Timeout(timeout, speed_unit)

    def _create_worker(self, handler):
        return TimeoutWorker(
            handler,
            gather=self._gather,
            recorder=self._recorder,
            speed=self._speed,
            timeout=self._timeout
        )
