# from itertools import chain
from gnss import index
import time
from datetime import datetime
from pprint import pprint
import gc
from copy import copy
# # print (index.datasets[0].data[0])
# # print (index.datasets[0].data[0].meta)
# print (index)

# from numpy import linspace
# from scipy.interpolate import BarycentricInterpolator as Intepolator
# from scipy.interpolate import splprep, splev
# class Humidity(object):
#     # header = {0:'Date(dd-mm-yy)',
#     #           1:'Time(hh:mm:ss)',
#     #           19:'Water',
#     #           36:'WaterError'}
#     header = {0:'epoch',
#               1:'water',}

#     def __init__(self, src):
#         with open(src) as vapor:

#             [vapor.readline() for i in range(4)]
#             self.header = [h.strip() for h in vapor.readline().split(',')]
#             self.datetimes = []
#             self.timestamps = []
#             self.values = []
#             for dataline in vapor.readline():
#                 dataline = [h.strip() for h in vapor.readline().split(',')]
#                 dt = datetime.strptime(' '.join(dataline[:2]), "%d:%m:%Y %H:%M:%S")
#                 self.datetimes += dt,
#                 self.timestamps += time.mktime(dt.timetuple()),
#                 self.values += float(dataline[19]),

#         # linspace(min(self.datetimes), max(self.datetimes), 900)
#         # self.spline = Intepolator(self.timestamps, self.values)

    
# #     def __call__(self, at, *valuenames):
# #         pass

# vapor = Humidity('/home/den/project/geophys/docs/010101_120223_Kyiv.lev20')

# with open('humidity_cm.txt', 'w') as hfile:
#     for dt, ts, value in zip(vapor.datetimes, vapor.timestamps, vapor.values):
#         hfile.write('%s %s %s\n'%(dt, ts, value))

# # from pylab import plot, show
# # plot(vapor.datetimes, vapor.values, 'bo-', label='data')
# # plot(vapor.spline)
# print (len(vapor.datetimes),
#        min(vapor.datetimes), 
#        max(vapor.datetimes))

if __name__ == '__main__':
    index.datasets.sort(key=lambda data:data.week)
    f = open('trotot_hlsv.txt', 'w')
    while len (index.datasets):
        #this loop has memory lacks
        dataset = index.datasets.pop(0)
        if dataset.week < 1297:
            continue
        start = time.time()
        dataset.data.sort(key=lambda data:data.meta.get('day', 0))
        weekdata = []
        gc.collect()
        for data in dataset.data:
            if data.__class__.__name__ == 'Tropo'\
                and data.meta['center'] in ('WUT', 'COE', 'BKG'):
                
                for tropodata in data.solutions:
                    if tropodata['SITE'] == 'GLSV':
                        tropodata['CENTER'] = data.meta['center']
                        tropodata['SECONDS'] = int(time.\
                                        mktime(tropodata['EPOCH'].timetuple()))
                        weekdata.append(copy(tropodata))

        weekdata.sort(key=lambda data:data['EPOCH'])

        for tropodata in weekdata:
            f.write ('%(CENTER)s %(EPOCH)s %(SECONDS)s %(TROTOT)s %(STDDEV)s\n'%tropodata)
        
        print (dataset.week, time.time()-start)
        
        for data in dataset.data:
            data.close()
        dataset.data = []
        
        gc.collect()

    f.close()
