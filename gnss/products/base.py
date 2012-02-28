from gnss.base import DictBlock

class FileReferenceBlock(DictBlock):
    '''This block provides information on the Organization, point of contact, the
software and hardware involved in the creation of the file.'''
    def __init__(self, name='FILE/REFERENCE', **kwargs):
        super(FileReferenceBlock, self).__init__(name, **kwargs)