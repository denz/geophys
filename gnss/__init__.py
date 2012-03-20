import os

from .logger import logger
from .index import DateIndex
from .utils import FTP, file_decompressor
from .base import DATATYPES, Blocks, datafile

#make sure that all datatypes registered
from .products.atmospheric import *
from .products.satellite import *
from .products.terrestrial import *

from .data.satellite import *
from .data.station import *


DATASITE = 'igs.bkg.bund.de/EUREF/products/'
DATADIR_NAME = '/home/den/wine_c/mirror/igs.bkg.bund.de/EUREF/products'
DATADIR = os.path.abspath(os.path.join(os.path.dirname(__file__), DATADIR_NAME))

__all__ = ['index', 'datafile']

if not os.path.exists(DATADIR):
    logger.info('Loading data from %s'%DATASITE)

    os.mkdir(DATADIR)
    HOST, ROOT = DATASITE.strip('/').split('/', 1)
    ROOT = '/'+ROOT

    with FTP(HOST) as ftp:
        ftp.login()
        ftp.fetchall(ROOT, DATADIR, file_postprocessor=file_decompressor)


index = DateIndex(DATADIR)