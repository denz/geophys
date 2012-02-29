import os
import unittest

from gnss import index
from datetime import datetime, timedelta

class IndexTestCase(unittest.TestCase):
    pass
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

    def test_dict_parser(self):
        from gnss import datafile
        with datafile(self.testfile) as sinex:
            # sinex.reference.parse()
            self.assertTrue(sinex.reference == {'DESCRIPTION': 'ASI -  TELESPAZIO S.p.A.', 'HARDWARE': 'HP9000/785', 'CONTACT': 'Lina.Ferraro@asi.it', 'INPUT': 'stacov format', 'OUTPUT': 'sinex format', 'SOFTWARE': 'MicroCosm 2005.0'})

    def test_dict_transparent_parsing(self):
        from gnss import datafile
        with datafile(self.testfile) as sinex:
            self.assertTrue(len(sinex.reference)==6)
            self.assertTrue(sinex.reference['DESCRIPTION'] == 'ASI -  TELESPAZIO S.p.A.')            

    def test_list_parser_auto_header(self):
        from gnss import datafile
        with datafile(self.testfile) as sinex:
            sinex.phase_centers.parse()
            self.assertTrue(sinex.phase_centers.headers=={'AZ_EL': (70, 80), 'DESCRIPTION': (1, 21), 'L2->ARP(m) EAST': (63, 69), 'L1->ARP(m) UP': (28, 34), 'L1->ARP(m) EAST': (42, 48), 'L1->ARP(m) NORTH': (35, 41), 'L2->ARP(m) NORTH': (56, 62), 'L2->ARP(m) UP': (49, 55), 'S/N': (22, 27)})
    

    def test_parser_cleaner(self):
        from gnss import datafile
        with datafile(self.testfile) as sinex:
            # sinex.gps_phase_centers.parse()
            self.assertTrue(sinex.phase_centers==[{'AZ_EL': '------', 'DESCRIPTION': 'LEIAT504GG      NONE', 'L2->ARP(m) EAST': -0.0001, 'L1->ARP(m) UP': 0.0903, 'L1->ARP(m) EAST': 0.0009, 'L1->ARP(m) NORTH': 0.0008, 'L2->ARP(m) NORTH': -0.0001, 'L2->ARP(m) UP': 0.1191, 'S/N': '00029'}, {'AZ_EL': '------', 'DESCRIPTION': 'TPSCR3_GGD      NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.0617, 'L1->ARP(m) EAST': -0.0005, 'L1->ARP(m) NORTH': 0.0007, 'L2->ARP(m) NORTH': 0.0006, 'L2->ARP(m) UP': 0.0956, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '73803'}, {'AZ_EL': '------', 'DESCRIPTION': 'AOAD/M_T        NONE', 'L2->ARP(m) EAST': -0.0006, 'L1->ARP(m) UP': 0.0912, 'L1->ARP(m) EAST': -0.0005, 'L1->ARP(m) NORTH': 0.0006, 'L2->ARP(m) NORTH': -0.0001, 'L2->ARP(m) UP': 0.1201, 'S/N': '00404'}, {'AZ_EL': '------', 'DESCRIPTION': 'TPSCR3_GGD      CONE', 'L2->ARP(m) EAST': 0.0, 'L1->ARP(m) UP': 0.0615, 'L1->ARP(m) EAST': -0.0004, 'L1->ARP(m) NORTH': 0.0008, 'L2->ARP(m) NORTH': 0.0003, 'L2->ARP(m) UP': 0.0948, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'AOAD/M_T        NONE', 'L2->ARP(m) EAST': -0.0006, 'L1->ARP(m) UP': 0.0912, 'L1->ARP(m) EAST': -0.0005, 'L1->ARP(m) NORTH': 0.0006, 'L2->ARP(m) NORTH': -0.0001, 'L2->ARP(m) UP': 0.1201, 'S/N': '200'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'TRM29659.00     NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.092, 'L1->ARP(m) EAST': -0.0009, 'L1->ARP(m) NORTH': -0.0001, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1205, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'JPSREGANT_DD_E  NONE', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.1008, 'L1->ARP(m) EAST': -0.0003, 'L1->ARP(m) NORTH': 0.0001, 'L2->ARP(m) NORTH': 0.0002, 'L2->ARP(m) UP': 0.1165, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'ASH701945C_M    SCIT', 'L2->ARP(m) EAST': -0.0004, 'L1->ARP(m) UP': 0.0886, 'L1->ARP(m) EAST': -0.0004, 'L1->ARP(m) NORTH': 0.0007, 'L2->ARP(m) NORTH': -0.0002, 'L2->ARP(m) UP': 0.1176, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'ASH701941.B     NONE', 'L2->ARP(m) EAST': -0.0004, 'L1->ARP(m) UP': 0.0892, 'L1->ARP(m) EAST': -0.0004, 'L1->ARP(m) NORTH': 0.0004, 'L2->ARP(m) NORTH': -0.0004, 'L2->ARP(m) UP': 0.1188, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'LEIAT504        LEIS', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.0884, 'L1->ARP(m) EAST': -0.0001, 'L1->ARP(m) NORTH': 0.0007, 'L2->ARP(m) NORTH': -0.0003, 'L2->ARP(m) UP': 0.1151, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'LEIAT504        LEIS', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.0884, 'L1->ARP(m) EAST': -0.0001, 'L1->ARP(m) NORTH': 0.0007, 'L2->ARP(m) NORTH': -0.0003, 'L2->ARP(m) UP': 0.1151, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'LEIAT504        LEIS', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.0884, 'L1->ARP(m) EAST': -0.0001, 'L1->ARP(m) NORTH': 0.0007, 'L2->ARP(m) NORTH': -0.0003, 'L2->ARP(m) UP': 0.1151, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'LEIAT504        LEIS', 'L2->ARP(m) EAST': 0.0002, 'L1->ARP(m) UP': 0.0884, 'L1->ARP(m) EAST': -0.0001, 'L1->ARP(m) NORTH': 0.0007, 'L2->ARP(m) NORTH': -0.0003, 'L2->ARP(m) UP': 0.1151, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'LEIAT504        NONE', 'L2->ARP(m) EAST': 0.0001, 'L1->ARP(m) UP': 0.0912, 'L1->ARP(m) EAST': -0.0003, 'L1->ARP(m) NORTH': 0.0001, 'L2->ARP(m) NORTH': -0.0001, 'L2->ARP(m) UP': 0.1173, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'LEIAT302+GP     NONE', 'L2->ARP(m) EAST': -0.0058, 'L1->ARP(m) UP': 0.0304, 'L1->ARP(m) EAST': 0.0014, 'L1->ARP(m) NORTH': 0.0054, 'L2->ARP(m) NORTH': 0.0033, 'L2->ARP(m) UP': 0.0339, 'S/N': '-----'}, {'AZ_EL': '------', 'DESCRIPTION': 'AOAD/M_T        NONE', 'L2->ARP(m) EAST': -0.0006, 'L1->ARP(m) UP': 0.0912, 'L1->ARP(m) EAST': -0.0005, 'L1->ARP(m) NORTH': 0.0006, 'L2->ARP(m) NORTH': -0.0001, 'L2->ARP(m) UP': 0.1201, 'S/N': '-----'}])
            self.assertTrue('%s'%sinex.site_ids)

    def test_(self):
        from gnss import datafile
        testfile = '/home/den/project/geophys/gnss/datafiles/1426/asi14260.tro'
        # from gnss.base import ParseHeaders
        # h = ParseHeaders()
        # h.parse(iter(['*INDEX TYPE__ CODE PT SOLN REF_EPOCH___ UNIT S __ESTIMATED_VALUE____ _STD_DEV___','']))
        # print (h)
        with datafile(testfile) as tropo:
            '%s'%tropo.reference
            '%s'%tropo.description
            '%s'%tropo.coordinates
            '%s'%tropo.solutions

if __name__ == '__main__':
    unittest.main()