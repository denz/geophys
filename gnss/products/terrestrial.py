from gnss.base import Blocks, BlocksRegistry

__all__ = ['Sinex',]

class Sinex(Blocks, metaclass=BlocksRegistry):
    @classmethod
    def valid_filetype(cls, src):
        return src.endswith('.snx')