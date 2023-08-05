# @Time     : 2021/7/24
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from itertools import chain

from .base import IRecorder


def is_recorder(value):
    return isinstance(value, IRecorder)


class Recorder(IRecorder):

    def __init__(self):
        self._record = []

    def length(self):
        return len(self._record)

    def empty(self):
        return not self.length()

    def save(self, record):
        """
        保存结果
        :param record:
        :return:
        """
        self._record.append(record)

    def __iter__(self):
        if not self.empty():
            for item in self._record:
                yield item

    def __str__(self):
        return f"{self.__class__.__name__}(record={self._record}, length={self.length()})"


class RecorderChain(IRecorder):

    def __init__(self):
        self._recorder = Recorder()

    def length(self) -> int:
        return self._recorder.length()

    def empty(self) -> bool:
        return self._recorder.empty()

    def save(self, record: IRecorder):
        """
        保存结果记录器
        :param record:
        :return:
        """
        if not self._is_recoder(record):
            return
        self._recorder.save(record)

    def __iter__(self):
        return chain(*self._recorder)

    def _is_recoder(self, value):
        return isinstance(value, IRecorder)
