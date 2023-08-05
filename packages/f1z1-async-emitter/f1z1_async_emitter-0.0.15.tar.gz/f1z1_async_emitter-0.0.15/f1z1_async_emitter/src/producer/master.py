# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count

from f1z1_async_runner import create_runner, start

from ..components.gather import IGather
from ..components.record import IRecorder
from .base import IWorkerMaster
from .worker import IWorker, is_worker


class WorkerMaster(IWorkerMaster):

    def __init__(self, gather: IGather, recorder: IRecorder):
        self._gather = gather
        self._recorder = recorder

    def add(self, worker_or_group: IWorker) -> None:
        """
        add worker or worker group -> set
        :param worker_or_group:
        :return:
        """
        self._check_worker(worker_or_group)
        self._gather.put(worker_or_group)

    def run(self, worker_or_group: IWorker = None) -> IRecorder:
        """
        run worker or worker group
        :param worker_or_group:
        :return:
        """
        runner = create_runner(worker_or_group.start())
        return start(runner)

    def start(self) -> IRecorder:
        """
        multi process start
        :return:
        """
        gather = self._gather
        save = self._save

        with ProcessPoolExecutor(max_workers=self._less_workers(gather)) as executor:
            # TODO: 暂时稳定
            fut_set = {executor.submit(self.run, worker) for worker in gather}
            for fut in as_completed(fut_set):
                save(fut)
        return self._recorder

    def _save(self, fut):
        self._recorder.save(fut.result())

    def _less_workers(self, gather: IGather) -> int:
        return min(gather.length(), cpu_count())

    def _check_worker(self, worker):
        if not is_worker(worker):
            raise ValueError(
                f"worker need IWorker or IWorkerGroup, but got {type(worker).__name__}"
            )

    def __str__(self):
        return "{__class__.__name__}(gather={gather}, length={length})".format(
            __class__=self.__class__,
            gather=set(map(lambda x: ", ".join([str(x), str(id(x))]), self._gather)),
            length=self._gather.length()
        )
