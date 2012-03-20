import re
from functools import wraps, partial
import warnings
from contextlib import contextmanager
from mmap import mmap
from itertools import takewhile
import os
from pprint import pprint

from .logger import logger
from .utils import slugify

DATATYPES = {}
QUIET_ON_CLEAN_VALUES = True

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
        
        #potential optimization point
        self.mmap.seek(0)
        
        name = bytes(name, 'ascii')

        startpos = self.mmap.find(b'+'+name)
        if startpos == -1:
            raise TextBlockDoesNotExists()
        
        self.mmap.seek(startpos)
        
        self.mmap.readline()
        self.line_num = 1
        line = b''
        while not line.startswith(b'-'+name):
            if line:
                yield line.decode(self.coding).strip('\n')
            line = self.mmap.readline()
            self.line_num += 1

    def close(self):
        if hasattr(self, 'file'):
            self.file.close()

        if hasattr(self, 'mmap'):
            self.mmap.close()

    def __del__(self):
        self.close()


    def clean_meta_week(self, value):
        return int(value)
    clean_meta_hour = clean_meta_day = clean_meta_week

    def clean_meta_center(self, value):
        return value.upper()

    def clean_meta(self, name, value):
        custom_cleaner = getattr(self, 'clean_meta_%s'%slugify(name), None)
        return custom_cleaner(value) if custom_cleaner else value.strip()

    def setup_meta_from_filename(self):
        group = self.tokenize_filename(os.path.basename(self.src),
                                       self.notation).group
        self.meta = dict(zip(self.tokens, [self.clean_meta(token,
                                    group(token)) for token in self.tokens]))


    def __init__(self, src):
        self.src = src
        if hasattr(self, 'notation') and hasattr(self, 'tokens'):
            self.setup_meta_from_filename()


    
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

non_transparsers = ('__getattribute__','clear', '__init__')

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
            self.__setitem__(*self.item(line.strip()))
        

    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs
        dict.__init__.__get__(self, dict)()
    
    setup_transparsers(locals(), dict, parse)

class TextBlock(str, BlockMixin):
    def parse(self):
        text = self.get_block(self.name)
        self = ''.join(text)
        
        #untransparse before any actions
        untransparse(self, dict)
        self._parsed = True
        

    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs
        dict.__init__.__get__(self, str)()
    
    setup_transparsers(locals(), str, parse)

class ListBlock(list, BlockMixin):
    cleaner_prefix = 'clean_'
    def slugify(self, header):
        return slugify(header)

    def default_clean(self, s):
        return s.strip()

    def clean(self, header, value):
        custom_cleaner = '%s%s'%(self.cleaner_prefix,
                                self.slugify(header))
        return getattr(self, custom_cleaner, self.default_clean)(value)

    def tokenize(self, line):
        try:
            return dict((header, self.clean(header, line[start:stop])) \
                    for (header, (start, stop)) in self.headers.items())
        except Exception as e:
            def info(obj):
                return dict((k,v) for k,v in obj.__dict__.items() \
                            if not (callable(v) or k.startswith('__')))
            pprint ({'block':info(self),
                     'data':info(self.instance)})
            if self.kwargs['quiet_on_clean_values']:
                print (e)
                return None
            else:
                raise
            
    def parse(self):
        lines = self.get_block(self.name)
        if not hasattr(self, 'headers'):
            self.headers = ParseHeaders()
        
        line = None
        if isinstance(self.headers, ParseHeaders) and not self.headers:
            line = self.headers.parse(lines)
        else:
            takewhile(lambda s:startswith('*'), lines)
            next(lines)

        #can remove transparsing decorators now
        untransparse(self, dict)
        self._parsed = True

        append_if_good_dataline = lambda tokens:tokens is not None \
                                                and self.append(tokens)
        if line:
            append_if_good_dataline(self.tokenize(line))
            
        for line in lines:
            append_if_good_dataline(self.tokenize(line))    

    def __init__(self, name, **kwargs):
        self.name = name
        kwargs['quiet_on_clean_values'] = kwargs.get('quiet_on_clean_values', 
                                                      QUIET_ON_CLEAN_VALUES)
        self.kwargs = kwargs
        list.__init__.__get__(self, list)()
    
    setup_transparsers(locals(), list, parse)


class ParseHeaders(dict):
    line_width = 80
    subsplitter = ' '
    def __init__(self, *args, **kwargs):
        self.prefix = kwargs.get('prefix', '*')
        super(ParseHeaders, self).__init__(*args, **kwargs)
    
    def clean_key(self, key):
        return key.strip('_')
    
    def flatten(self, start, stop, subheaders):
        if not len(subheaders):
            return

        headers = iter(subheaders[-1])
        for (header, (substart, substop)) in headers:
            if substart>=start and substop<=stop:
                has_subs = False
                for (subheader, (subsubstart, subsubstop)) in self.flatten(substart, 
                                                                           substop, 
                                                                           subheaders[:-1]):
                    has_subs = True
                    yield (''.join([header, self.subsplitter, subheader]), 
                           (subsubstart, subsubstop))
                if not has_subs:
                    yield (header, (substart, substop))

    def parse_header_line(self, line):
        if not hasattr(self, 'subheaders'):
            self.subheaders = []

        subheaders = []

        pos = len(line) - len(line[1:].lstrip())

        for header in line[pos:].split(' '):
            newpos = pos + len(header)
            if header.strip():
                subheaders += (self.clean_key(header), (pos, newpos)),
            pos = newpos + 1

        if len(self.subheaders):
            #see +SITE/ECCENTRICITY, last column
            if self.subheaders[-1][-1][1][1] > subheaders[-1][1][1]:
                subheaders[-1] = \
                  (subheaders[-1][0], (subheaders[-1][1][0], self.subheaders[-1][-1][1][1]))
        self.subheaders += subheaders,

    def parse(self, lines):
        line = next(lines)
        while line.startswith(self.prefix):
            self.parse_header_line(line)
            line = next(lines)
        super(ParseHeaders, self).__init__(self.flatten(0, self.line_width, self.subheaders))
        return line


    def __get__(self, instance, owner):
        if not instance:
            return self.__class__

        if not hasattr(instance, '_headers'):
            instance._headers = self.__class__()
            instance._headers.instance = instance

        return instance._headers

    