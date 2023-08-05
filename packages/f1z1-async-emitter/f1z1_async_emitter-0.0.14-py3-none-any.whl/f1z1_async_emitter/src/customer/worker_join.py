# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import as_completed

from ..components.gather import IGather
from ..components.record import IRecorder
from .base import IJoin


class WorkerJoin(IJoin):
    __slots__ = "_recorder", "_gather"

    def __init__(self, recorder: IRecorder, gather: IGather):
        self._recorder = recorder
        self._gather = gather

    async def join(self) -> IRecorder:
        for _, task in enumerate(as_completed(self._gather)):
            await self.save(task)
        return self._recorder

    async def save(self, task):
        result = await task
        self._recorder.save(result)

    def __str__(self):
        return f"{self.__class__.__name__}(record={self._recorder}, gather={self._gather})"
