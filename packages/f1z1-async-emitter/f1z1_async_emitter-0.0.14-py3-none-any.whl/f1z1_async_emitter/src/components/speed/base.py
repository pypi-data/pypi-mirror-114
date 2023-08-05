# @Time     : 2021/7/24
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod



class IAwaitSpeed(metaclass=ABCMeta):
    """
    speed interface
    """

    @abstractmethod
    def __await__(self):
        raise NotImplementedError("NotImplemented .__await__()")
