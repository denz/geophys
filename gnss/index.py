import os
from .base import Blocks, datafile

class DateIndex(object):
    def __init__(self, datadir):
        self.datadir = datadir

        self.datasets = []

        for src in os.listdir(self.datadir):
            src = os.path.join(self.datadir, src)
            if Dataset.valid_datadir(src):
                self.datasets += Dataset(src),

class Dataset(object):
    @classmethod
    def valid_datadir(cls, src):
        return os.path.isdir(src)

    def __init__(self, src):
        self.src = src
        self.data = []
        for file in os.listdir(src):
            with datafile(os.path.join(src, file)) as data:
                if not data.__class__ is Blocks:
                    self.data += data,
