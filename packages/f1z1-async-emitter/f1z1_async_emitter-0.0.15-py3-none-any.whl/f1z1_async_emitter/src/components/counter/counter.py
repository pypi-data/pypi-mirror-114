# @Time     : 2021/7/24
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from .base import IAsyncCountGenerator
from ..speed import IAwaitSpeed


class AsyncCountGenerator(IAsyncCountGenerator):
    """
    count generator
    """

    def __init__(self, count: int, speed: IAwaitSpeed):
        self._count = count
        self._speed = speed

    def count(self):
        return self._get_count()

    async def __aiter__(self):
        for _, number in enumerate(range(self.count())):
            yield number
            await self._speed

    def _get_count(self) -> int:
        _abs = abs(self._count)
        return 2 ** 31 if not _abs else _abs

    def __str__(self):
        return f"{self.__class__.__name__}(count={self.count()}, speed={self._speed})"
