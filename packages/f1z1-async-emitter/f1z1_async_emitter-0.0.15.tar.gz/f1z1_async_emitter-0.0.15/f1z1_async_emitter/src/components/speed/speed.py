# @Time     : 2021/7/24
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import sleep
from collections.abc import Awaitable
from functools import lru_cache
from typing import Union

from f1z1_common import timeunit, UnitOfTime

from .base import IAwaitSpeed

IntOrFloat = Union[int, float]


class Speed(Awaitable, IAwaitSpeed):

    def __init__(self, int_or_float: IntOrFloat, speed_unit: UnitOfTime):
        self._speed = int_or_float
        self._speed_unit = speed_unit

    def __await__(self):
        return self._await_impl(self._speed_unit).__await__()

    async def _await_impl(self, speed_unit: UnitOfTime):
        return await sleep(self._use_lru_cache(speed_unit))

    @lru_cache()
    def _use_lru_cache(self, speed_unit: UnitOfTime) -> float:
        return self._speed / timeunit(speed_unit)

    def __str__(self):
        return f"{self.__class__.__name__}(speed={self._use_lru_cache(self._speed_unit)})"
