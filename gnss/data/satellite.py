from gnss.base import Blocks, BlocksRegistry
__all__ = []

# class RinexD(Blocks, metaclass=BlocksRegistry):
#     '''Hatanaka compressed GNSS observation'''
#     @classmethod
#     def valid_filetype(self, src):
#         return src.endswith('.rinex-d')

# class RinexN(Blocks, metaclass=BlocksRegistry):
#     '''GPS navigation file'''
#     @classmethod
#     def valid_filetype(self, src):
#         return src.endswith('.rinex-n')

# class RinexG(Blocks, metaclass=BlocksRegistry):
#     '''GLONASS navigation file'''
#     @classmethod
#     def valid_filetype(self, src):
#         return src.endswith('.rinex-g')

# class RinexL(Blocks, metaclass=BlocksRegistry):
#     '''Galileo navigation file'''
#     @classmethod
#     def valid_filetype(self, src):
#         return src.endswith('.rinex-l')

# class RinexQ(Blocks, metaclass=BlocksRegistry):
#     '''QZSS navigation file'''
#     @classmethod
#     def valid_filetype(self, src):
#         return src.endswith('.rinex-q')

# class RinexP(Blocks, metaclass=BlocksRegistry):
#     '''mixed GNSS navigation file'''
#     @classmethod
#     def valid_filetype(self, src):
#         return src.endswith('.rinex-p')

# class RinexM(Blocks, metaclass=BlocksRegistry):
#     '''meteorological observation file'''
#     @classmethod
#     def valid_filetype(self, src):
#         return src.endswith('.rinex-m')

# class RinexS(Blocks, metaclass=BlocksRegistry):
#     '''GNSS observation summary file'''
#     @classmethod
#     def valid_filetype(self, src):
#         return src.endswith('.rinex-s')

# class Brdc(Blocks, metaclass=BlocksRegistry):
#     '''daily GPS or GLONASS broadcast ephemerides'''
#     @classmethod
#     def valid_filetype(self, src):
#         return src.endswith('.brdc')