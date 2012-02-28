import re
from functools import wraps
import warnings
from contextlib import contextmanager
from mmap import mmap

from .logger import logger
from .utils import slugify

DATATYPES = {}

class BlocksRegistry(type):

    def register_datatype(new):
        if not new.valid_filetype in DATATYPES:
            DATATYPES[new.valid_filetype] = new
        return new

    def __new__(cls, name, bases, members):
        new = type(name, bases, members)
        new.valid_filetype = classmethod(new.valid_filetype.__func__)
        return cls.register_datatype(new)

class TextBlockDoesNotExists(Exception):
    pass

class Blocks(object):
    coding = 'ascii'
    @classmethod
    def valid_filetype(cls, src):
        return False
    
    @classmethod
    def tokenize_filename(cls, filename, notation):
        return re.match(notation, filename)

    def textblock(self, name):
        if not hasattr(self, 'file'):
            self.file = open(self.src, 'r+b')

        if not hasattr(self, 'mmap'):
            self.mmap = mmap(self.file.fileno(), 0)
        
        name = bytes(name, 'ascii')

        startpos = self.mmap.find(b'+'+name)
        if startpos == -1:
            raise TextBlockDoesNotExists()
        
        self.mmap.seek(startpos)
        
        self.mmap.readline()
        line = b''
        while not line.startswith(b'-'+name):
            if line:
                yield line.decode(self.coding).strip('\n').strip()
            line = self.mmap.readline()

        

    def __del__(self):
        if hasattr(self, 'file'):
            self.file.close()

        if hasattr(self, 'mmap'):
            self.mmap.close()

    def __init__(self, src):
        self.src = src

    
@contextmanager
def datafile(*args, **kwargs):
    for selector, cls in DATATYPES.items():
        if selector(*args, **kwargs):
            yield cls(*args, **kwargs)
            return
    
    # logger.warn('Cannot find suitable datatype for `%s`. Base class used'%\
    #                                                  (str(args)+' '+str(kwargs)))
    yield Blocks(*args, **kwargs)


class BlockMixin(object):

    def __get__(self, instance, owner):
        if not instance:
            return self.__class__
        if not hasattr(instance, self.name):
            setattr(instance, 
                    self.name, 
                    self.__class__(self.name, **self.kwargs))
            getattr(instance, self.name).instance = instance

        return getattr(instance, self.name)

    def get_block(self, name):
        try:
            return self.instance.textblock(name)
        except TextBlockDoesNotExists as e:
            if self.kwargs.get('mandatory', True):
                raise

non_transparsers = ('__getattribute__','clear', '__repr__', '__init__')


def transparse(wrapped, parser):
    @wraps(wrapped)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '_parsed'):
            parser.__get__(self, parser.__class__)()
        return wrapped.__get__(self, self.__class__)(*args, **kwargs)
    wrapper.transparsed = wrapped
    return wrapper

def untransparse(instance, to):
    for method_name in dir(instance):
        method = getattr(instance, method_name)
        if callable(method) and hasattr(method, 'transparsed'):
            setattr(instance, method_name, method.transparsed.__get__(instance, to))

def setup_transparsers(locals, base, parser, exclude=non_transparsers):
    for method_name in dir(base):
        if not method_name in exclude:
            method = getattr(base, method_name)
            if callable(method) and getattr(method, '__objclass__', None) is base:
                locals[method_name] = transparse(method, parser)


class DictBlock(dict, BlockMixin):
    key_column_len = 18
    def item(self, line):
        return (line[:(self.key_column_len-1)].strip(), 
                line[(self.key_column_len-1):].strip())

    def parse(self):
        text = self.get_block(self.name)
        #untransparse before any actions
        untransparse(self, dict)
        self._parsed = True
        for line in text:
            self.__setitem__(*self.item(line))
        

    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs
        dict.__init__.__get__(self, dict)()
    
    setup_transparsers(locals(), dict, parse)