import os

from datetime import datetime, timedelta

from .base import Blocks, datafile

class DateIndex(object):
    def range(self, since=None, until=None):
        since = since if since else self.since
        until = until if until else self.until

        for dataset in self.datasets:
            if (dataset.since<=since and dataset.until>=since)\
                or (dataset.since<=until and dataset.until>=until)\
                or (since<=dataset.since and until>=dataset.until):
                yield dataset

    def __init__(self, datadir):
        self.datadir = datadir

        self.datasets = []
        self.since = None
        self.until = None

        for src in os.listdir(self.datadir):
            src = os.path.join(self.datadir, src)
            if Dataset.valid_datadir(src):
                dataset = Dataset(src)

                if not self.since or self.since>dataset.since:
                    self.since = dataset.since

                if not self.until or self.until<dataset.until:
                    self.until = dataset.until

                self.datasets += dataset,

class Dataset(object):
    epoch = datetime(1980, 1, 6)
    end_of_week_back_offset = {'milliseconds':30}

    @classmethod
    def valid_datadir(cls, src):
        return os.path.isdir(src)

    def setup_daterange(self, src):
        self.week = int(os.path.basename(src))
        self.since = self.epoch + timedelta(weeks = self.week)
        self.until = self.since + \
                     timedelta(weeks = 1) - \
                     timedelta(**self.end_of_week_back_offset)

    def __init__(self, src):
        self.src = src
        self.data = []
        self.setup_daterange(src)

        for file in os.listdir(src):
            with datafile(os.path.join(src, file)) as data:
                if not data.__class__ is Blocks:
                    self.data += data,
