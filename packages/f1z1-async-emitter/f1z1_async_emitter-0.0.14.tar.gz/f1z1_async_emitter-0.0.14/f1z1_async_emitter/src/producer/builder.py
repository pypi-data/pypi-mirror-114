# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod

from f1z1_common import CoroOrFunction, UnitOfTime, ArgsTypes, KwargsTypes

from ..components.counter import AsyncCountGenerator
from ..components.gather import IGather, QueueGather, is_gather
from ..components.record import IRecorder, Recorder, is_recorder
from ..components.speed import Speed, IntOrFloat
from ..components.timeout import Timeout
from .base import IWorker
from .handler import WorkerHandler
from .worker import CounterWorker, TimeoutWorker

Int2E16 = 2 ** 31
MINUTE_30 = 1800


class AbstractWorkerBuilder(metaclass=ABCMeta):

    def __init__(self,
                 target: CoroOrFunction,
                 args: ArgsTypes = None,
                 kwargs: KwargsTypes = None,
                 thread_workers: int = None):
        self._target = target
        self._args = () if not args else args
        self._kwargs = {} if not kwargs else kwargs
        self._thread_workers = thread_workers

        self._gather = QueueGather(Int2E16)
        self._recorder = Recorder()
        self._speed = Speed(100, UnitOfTime.MILLISECOND)

    def set_gather(self, gather: IGather):
        self._check_gather(gather)
        self._gather = gather
        return self

    def set_recorder(self, recorder: IRecorder):
        self._check_recorder(recorder)
        self._recorder = recorder
        return self

    def set_speed(self,
                  int_or_float: IntOrFloat,
                  speed_unit: UnitOfTime = UnitOfTime.MILLISECOND):
        self._speed = Speed(int_or_float, speed_unit)
        return self

    @abstractmethod
    def build(self) -> IWorker:
        raise NotImplementedError()

    def _create_handler(self):
        return WorkerHandler(
            self._target,
            self._args,
            self._kwargs,
            self._thread_workers
        )

    def _check_gather(self, gather):
        if not is_gather(gather):
            raise ValueError(
                f"gather need IGather, but got {type(gather).__name__}"
            )

    def _check_recorder(self, recoder):
        if not is_recorder(recoder):
            raise ValueError(
                f"recoder need IRecorder, but got {type(recoder).__name__}"
            )


class CounterWorkerBuilder(AbstractWorkerBuilder):

    def __init__(self,
                 target: CoroOrFunction,
                 args: ArgsTypes = None,
                 kwargs: KwargsTypes = None,
                 thread_workers: int = None):
        super().__init__(target, args, kwargs, thread_workers)
        self._count = 1

    def set_count(self, count: int):
        self._count = abs(count)
        return self

    def build(self) -> CounterWorker:
        return CounterWorker(
            self._create_handler(),
            AsyncCountGenerator(self._count, self._speed),
            self._gather,
            self._recorder
        )


class TimeoutWorkerBuilder(AbstractWorkerBuilder):

    def __init__(self,
                 target: CoroOrFunction,
                 args: ArgsTypes = None,
                 kwargs: KwargsTypes = None,
                 thread_workers: int = None):
        super().__init__(target, args, kwargs, thread_workers)
        self._timeout = Timeout(MINUTE_30, UnitOfTime.SECOND)

    def set_timeout(self, int_or_float: IntOrFloat, unit: UnitOfTime = UnitOfTime.SECOND):
        self._timeout = Timeout(int_or_float, unit)
        return self

    def build(self) -> TimeoutWorker:
        return TimeoutWorker(
            self._create_handler(),
            self._gather,
            self._recorder,
            self._speed,
            self._timeout
        )
