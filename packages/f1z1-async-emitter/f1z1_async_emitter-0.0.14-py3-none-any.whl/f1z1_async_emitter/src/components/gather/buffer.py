# @Time     : 2021/7/24
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from collections import deque
from typing import Optional

from f1z1_common import is_validators

from ..speed import IAwaitSpeed
from .base import IAwaitBuffer, IterOrList


class AwaitBufferQueue(IAwaitBuffer):
    """
    emit buffer queue
    """

    def __init__(self, speed: IAwaitSpeed, maxsize: Optional[int] = None):
        self._speed = speed
        self._buffer = deque(maxlen=maxsize)

    def length(self):
        return len(self._buffer)

    def empty(self):
        return not self.length()

    def put(self, iter_or_list: IterOrList):
        self._buffer.extend(self._to_iter_or_list(iter_or_list))

    def pop(self):
        return self._buffer.popleft()

    async def __aiter__(self):
        while True:
            if self.empty():
                break
            yield self.pop()
            await self._speed

    def _to_iter_or_list(self, iter_or_list: IterOrList) -> IterOrList:
        return [] if not is_validators.is_iterable(iter_or_list) else iter_or_list

    def __str__(self):
        return f"{self.__class__.__name__}(buffer={str(self._buffer)}, speed={self._speed})"

    def __len__(self):
        return len(self._buffer)
