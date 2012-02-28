import os
from gnss.base import Blocks, BlocksRegistry
from .base import FileReferenceBlock

__all__ = ['UltraRapidSinex', 'RapidSinex', 'MultipleDayRapidSinex', 
           'DayFinalSinex', 'WeekFinalSinex', 'MultipleDayFinalSinex']

class Sinex(Blocks):
    '''combined station position and velocity solutions'''
    @classmethod
    def valid_filetype(cls, src):
        return src.endswith('.snx') and \
               cls.tokenize_filename(os.path.basename(src), cls.notation)

    reference = FileReferenceBlock()

class UltraRapidSinex(Sinex, metaclass=BlocksRegistry):
    '''
    Updates :   hourly
    Latency :   2-3 hours
    '''
    #notation = 'cenWWWWD_HH.snx'
    tokens = ('center', 'week', 'day', 'hour')
    notation = '^(?P<center>\w{3})(?P<week>\d{4})(?P<day>[0123456])_(?P<hour>[012]\d).snx$'


class RapidSinex(Sinex, metaclass=BlocksRegistry):
    '''
    Updates :   daily
    Latency :   12-21 hours
    '''
    #notation = 'cenWWWWDr.snx'
    tokens = ('center', 'week', 'day')
    notation = '^(?P<center>\w{3})(?P<week>\d{4})(?P<day>[0123456])r.snx$'


class MultipleDayRapidSinex(Sinex, metaclass=BlocksRegistry):
    '''
    Updates :   daily
    Latency :   ~ 1 day
    '''
    #notation = 'cenWWWWmr.snx'
    tokens = ('center', 'week')
    notation = '^(?P<center>\w{3})(?P<week>\d{4})mr.snx$'


class DayFinalSinex(Sinex, metaclass=BlocksRegistry):
    '''
    Updates :   weekly
    Latency :   ~ 3 weeks
    '''
    #notation = 'cenWWWWD.snx'
    tokens = ('center', 'week', 'day')
    notation = '^(?P<center>\w{3})(?P<week>\d{4})(?P<day>[0123456]).snx$'


class WeekFinalSinex(Sinex, metaclass=BlocksRegistry):
    '''
    Updates :   weekly
    Latency :   ~ 4 weeks
    '''
    #notation = 'cenWWWW7.snx'
    tokens = ('center', 'week')
    notation = '^(?P<center>\w{3})(?P<week>\d{4})7.snx$'


class MultipleDayFinalSinex(Sinex, metaclass=BlocksRegistry):
    '''
    Updates :   weekly
    Latency :   ~ 5 weeks
    '''
    #notation = 'cenWWWWm.snx'
    tokens = ('center', 'week')
    notation = '^(?P<center>\w{3})(?P<week>\d{4})m.snx$'