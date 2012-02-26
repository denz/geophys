import warnings
from contextlib import contextmanager


DATATYPES = {}

class BlocksRegistry(type):
    def register_datatype(new):
        if not new.valid_filetype in DATATYPES:
            DATATYPES[new.valid_filetype] = new
        return new

    def __new__(cls, *args, **kwargs):
        return cls.register_datatype(type(*args, **kwargs))


class Blocks(object):
    @classmethod
    def valid_filetype(cls, src):
        return False

    def __init__(self, src):
        self.src = src

@contextmanager
def datafile(*args, **kwargs):
    for selector, cls in DATATYPES.items():
        if selector(*args, **kwargs):
            yield cls(*args, **kwargs)
            return
    
    warnings.warn('Cannot find suitable datatype for `%s`. Base class used'%\
                                                    (str(args)+' '+str(kwargs)))
    yield Blocks(*args, **kwargs)
