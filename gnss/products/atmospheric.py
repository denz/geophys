import os
from gnss.base import Blocks, BlocksRegistry, ListBlock, DictBlock
from gnss.cleaners import clean_date
__all__ = ['Tropo',]


class Coordinates(ListBlock):
    def __init__(self, name='TROP/STA_COORDINATES', **kwargs):
        super(Coordinates, self).__init__(name, **kwargs)

    def clean_sta_x(self, value):
        return float(value)
    clean_sta_y = clean_sta_z = clean_sta_x



class Solutions(ListBlock):
    def __init__(self, name='TROP/SOLUTION', **kwargs):
        super(Solutions, self).__init__(name, **kwargs)
    def clean_epoch(self, value):
        return clean_date(value)

    def clean_trotot(self, value):
        return float(value)

    clean_stddev = clean_trotot


class Tropo(Blocks, metaclass=BlocksRegistry):
    #notation = 'cenWWWWD.tro'
    tokens = ('center', 'week', 'day')
    notation = '^(?P<center>\w{3})(?P<week>\d{4})(?P<day>[0123456]).tro$'

    @classmethod
    def valid_filetype(cls, src):
        return src.endswith('.tro') and \
               cls.tokenize_filename(os.path.basename(src), cls.notation)
    reference = DictBlock('FILE/REFERENCE')
    description = DictBlock('TROP/DESCRIPTION')
    coordinates = Coordinates()
    solutions = Solutions()