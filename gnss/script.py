# from itertools import chain
from gnss import index
import time
from datetime import datetime
from pprint import pprint
import gc
from copy import copy

if __name__ == '__main__':
    index.datasets.sort(key=lambda data:data.week)
    f = open('trotot_hlsv.txt', 'w')
    while len (index.datasets):
        #this loop has memory lacks
        dataset = index.datasets.pop(0)
        if dataset.week < 1297:
            #there is no tropodata before that week
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
