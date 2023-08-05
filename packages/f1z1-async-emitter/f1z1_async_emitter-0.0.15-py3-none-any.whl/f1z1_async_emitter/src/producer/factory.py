# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from f1z1_common import UnitOfTime
from f1z1_async_runner import create_runner, start

from ..components.gather import AwaitBufferQueue, QueueGather, SetGather
from ..components.record import RecorderChain
from ..components.speed import Speed, IntOrFloat
from .base import IWorker, IWorkerFactory
from .builder import Int2E16
from .worker import WorkerGroup, is_worker
from .master import WorkerMaster


class WorkerGroupFactory(IWorkerFactory):
    """
    worker group factory
    """

    @classmethod
    def create(cls,
               count: int = Int2E16,
               speed: IntOrFloat = 10,
               speed_unit: UnitOfTime = UnitOfTime.MILLISECOND) -> WorkerGroup:
        less = cls._less_count(count)
        return WorkerGroup(
            AwaitBufferQueue(Speed(speed, speed_unit), less),
            QueueGather(less),
            RecorderChain()
        )

    @classmethod
    def _less_count(cls, count: int):
        return min(abs(count), Int2E16)


class WorkerMasterFactory(IWorkerFactory):
    """
    worker master factory
    """

    @classmethod
    def create(cls, maxsize: int = None) -> WorkerMaster:
        return WorkerMaster(SetGather(maxsize), RecorderChain())


def create_group(count: int = Int2E16,
                 speed: IntOrFloat = 10,
                 speed_unit: UnitOfTime = UnitOfTime.MILLISECOND):
    return WorkerGroupFactory.create(count, speed, speed_unit)


def create_master(maxsize: int = None):
    return WorkerMasterFactory.create(maxsize)


def run(worker: IWorker):
    if not is_worker(worker):
        raise ValueError(
            f"worker need IWorker, but got {type(worker).__name__}"
        )
    runner = create_runner(worker.start())
    return start(runner)
