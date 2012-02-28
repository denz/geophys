import os
import unittest

from gnss import index
from datetime import datetime, timedelta

class IndexTestCase(unittest.TestCase):
    def test_index_init(self):
        for dataset in index.datasets:
            os.path.isdir(dataset.src)
    def test_index_datasets(self):
        for dataset in index.datasets:
            self.assertTrue(len(dataset.data))
    
    def test_dataset_daterange(self):
        self.assertTrue(index.datasets[0].week == 1426)
        
        since = index.datasets[0].since
        until = index.datasets[0].until
        self.assertTrue(since.year == 2007)
        self.assertTrue(since.month == 5)
        self.assertTrue(since.day == 6)

        self.assertTrue(until.year == 2007)
        self.assertTrue(until.month == 5)
        self.assertTrue(until.day == 12)

        delta = since - datetime(2007, 1, 1)
        #timedelta is zero indexed - so 125 instead 126
        self.assertTrue(delta.days == 125)
    
    def test_iter(self):
        since = index.datasets[0].since
        until = index.datasets[0].until
        oneday = timedelta(days=1)
        self.assertTrue(len([d for d in index.range()]))
        self.assertTrue(len([d for d in index.range(since, datetime.now())]))
        self.assertTrue(not len([d for d in index.range(datetime.now(),
                                                        datetime.now())]))
        
        self.assertTrue(len([d for d in index.range(since+oneday,
                                                    until-oneday)]))

        self.assertTrue(len([d for d in index.range(since-oneday,
                                                    until+oneday)]))

class DatafileTestCase(unittest.TestCase):

    testfile = '/home/den/project/geophys/gnss/datafiles/1426/asi14260.snx'
    def test_datafile_func(self):
        from gnss import datafile
        with datafile(self.testfile) as sinex:
            self.assertTrue(sinex.src == self.testfile)

    def test_datatype_register(self):
        from gnss.base import Blocks, BlocksRegistry, DATATYPES

        class TestBlocks0(Blocks, metaclass=BlocksRegistry):
            notation = '.*'

        self.assertTrue(TestBlocks0 in DATATYPES.values())
        del DATATYPES[TestBlocks0.valid_filetype]

    def test_datatype_selector(self):
        from gnss import datafile
        from gnss.base import Blocks, BlocksRegistry, DATATYPES
        from products.terrestrial import DayFinalSinex

        with datafile(self.testfile) as sinex:
            self.assertTrue(sinex.__class__.__name__ is 'DayFinalSinex')



class BlocksTestCase(unittest.TestCase):
    testfile = '/home/den/project/geophys/gnss/datafiles/1426/asi14260.snx'
    
    def test_block_getter(self):
        from products.terrestrial import DayFinalSinex
        sinex0 = DayFinalSinex(self.testfile)
        sinex1 = DayFinalSinex(self.testfile)
        self.assertTrue(sinex0.reference is not sinex1.reference)
        self.assertTrue(sinex0.reference == sinex0.reference)
        self.assertTrue(sinex1.reference == sinex1.reference)

    def test_textblock(self):
        from gnss import datafile
        with datafile(self.testfile) as sinex:
            self.assertTrue(len(list(sinex.textblock('FILE/REFERENCE'))))

class DictBlockTestCase(unittest.TestCase):
    testfile = '/home/den/project/geophys/gnss/datafiles/1426/asi14260.snx'

    def test_parser(self):
        from gnss import datafile
        with datafile(self.testfile) as sinex:
            sinex.reference.parse()
            self.assertTrue(sinex.reference == {'DESCRIPTION': 'ASI -  TELESPAZIO S.p.A.', 'HARDWARE': 'HP9000/785', 'CONTACT': 'Lina.Ferraro@asi.it', 'INPUT': 'stacov format', 'OUTPUT': 'sinex format', 'SOFTWARE': 'MicroCosm 2005.0'})

    def test_transparent_parsing(self):
        from gnss import datafile
        with datafile(self.testfile) as sinex:
            self.assertTrue(len(sinex.reference)==6)
            self.assertTrue(sinex.reference['DESCRIPTION'] == 'ASI -  TELESPAZIO S.p.A.')            
        

if __name__ == '__main__':
    unittest.main()