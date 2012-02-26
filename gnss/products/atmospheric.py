from gnss.base import Blocks, BlocksRegistry

__all__ = ['Tropo',]

class Tropo(Blocks, metaclass=BlocksRegistry):
    @classmethod
    def valid_filetype(cls, src):
        return src.endswith('.tro')
