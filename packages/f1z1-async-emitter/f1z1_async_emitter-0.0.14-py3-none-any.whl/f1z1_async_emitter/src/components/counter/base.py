# @Time     : 2021/7/24
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from typing import AsyncIterable


class IAsyncCountGenerator(metaclass=ABCMeta):
    """
    count generator interface
    """

    @abstractmethod
    async def __aiter__(self) -> AsyncIterable[int]:
        raise NotImplementedError("NotImplemented .__aiter__() -> AsyncIterable[int]")
