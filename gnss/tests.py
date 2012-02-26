import os
import unittest

from gnss import index


class IndexTestCase(unittest.TestCase):
    def test_index_init(self):
        for dataset in index.datasets:
            os.path.isdir(dataset.src)
    def test_(self):
        for dataset in index.datasets:
            self.assertTrue(len(dataset.data))


class SinexBlocksFileTestCase(unittest.TestCase):

    testfile = '/home/den/project/geophys/gdc/data/1426/asi14260.snx'
    def test_datafile_func(self):
        from gnss import datafile
        with datafile(self.testfile) as sinex:
            self.assertTrue(sinex.src == self.testfile)

    def test_datatype_register(self):
        from gnss.base import Blocks, BlocksRegistry, DATATYPES

        class TestBlocks0(Blocks, metaclass=BlocksRegistry):
            pass

        self.assertTrue(TestBlocks0 in DATATYPES.values())

    def test_datatype_selector(self):
        from gnss import datafile
        from gnss.base import Blocks, BlocksRegistry, DATATYPES
        from gnss.products.terrestrial import Sinex

        with datafile(self.testfile) as sinex:
            self.assertTrue(sinex.__class__ is Sinex)

if __name__=='__main__':
    unittest.main()

