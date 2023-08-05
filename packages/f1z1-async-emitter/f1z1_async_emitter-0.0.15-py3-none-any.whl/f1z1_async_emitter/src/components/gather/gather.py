# @Time     : 2021/7/24
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from collections import deque
from typing import Optional

from .base import IGather


def is_gather(value):
    return isinstance(value, IGather)


class QueueGather(IGather):

    def __init__(self, maxsize: Optional[int] = None):
        self._queue = deque(maxlen=maxsize)

    def length(self):
        return len(self._queue)

    def empty(self):
        return not self.length()

    def put(self, item) -> None:
        self._queue.append(item)

    def pop(self):
        return self._queue.popleft()

    def __iter__(self):
        while True:
            if self.empty():
                break
            yield self.pop()

    def __str__(self):
        return f"{self.__class__.__name__}(queue={self._queue})"


class SetGather(IGather):
    """
    Emit Task Collection
    """

    def __init__(self, maxsize: Optional[int] = None):
        self._set = set()
        self._maxsize = maxsize

    def length(self):
        return len(self._set)

    def empty(self):
        return not self.length()

    def full(self):
        maxsize = self._maxsize
        if maxsize is None:
            return False
        return self.length() >= maxsize

    def put(self, worker):
        if self.full():
            return
        self._set.add(worker)

    def pop(self):
        return self._set.pop()

    def __iter__(self):
        if not self.empty():
            for _, item in enumerate(self._set):
                yield item

    def __str__(self):
        return f"{self.__class__.__name__}(set={self._set})"
