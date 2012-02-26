import os
import logging
from contextlib import contextmanager


from ftplib import FTP as FTP_BASE
from ftplib import error_perm

import subprocess

logger = logging.getLogger(__name__)

NOT_A_DIRECTORY = '550 That is not a directory.'

@contextmanager
def file_decompressor(name, mode):
    try:
        f = open(name, mode)
        yield f
    finally:
        f.close()
        if name.lower().endswith('.z'):
            logger.info('Decompressing %s'%name)
            subprocess.call('uncompress %s'%(name), shell=True)

class FTP(FTP_BASE):
    def fetchfile(self, src, dst, file_postprocessor):
        writer = file_postprocessor or open
        with writer(dst, 'wb') as dest:
            self.retrbinary('RETR %s'%src, dest.write)
    
    def fetchall(self, src, dst, recursively=True, file_postprocessor=None):
        for name in self.nlst(src):
            self.cwd(src)
            os.chdir(dst)
            try:
                self.cwd(name)
                if not os.path.exists(name):
                    os.mkdir(name)
                subsrc = '%s/%s'%(src, name)
                subdst = os.path.join(dst, name)
                logger.info('Fetching from `%s` to `%s`'%(subsrc,  subdst))

                self.fetchall('%s/%s'%(src, name),
                              os.path.join(dst, name),
                              recursively, file_postprocessor)

            except error_perm as e:
                if str(e) == NOT_A_DIRECTORY:
                    self.fetchfile(name, name, 
                        file_postprocessor=file_postprocessor)
                else:
                    raise