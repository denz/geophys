from datetime import datetime, timedelta, date
from gnss.base import ListBlock

class SiteIds(ListBlock):
    '''This block provides general information for each site containing estimated
parameters.'''
    def __init__(self, name='SITE/ID', **kwargs):
        super(SiteIds, self).__init__(name, **kwargs)
    def clean_approx_lat(self, value):
        d, m, s = value.split()
        return int(d), int(m), float(s)

    clean_approx_lon = clean_approx_lat

class PhaseCenters(ListBlock):
    def __init__(self, name='SITE/GPS_PHASE_CENTER', **kwargs):
        super(PhaseCenters, self).__init__(name, **kwargs)

    def default_clean(self, value):
        return float(value)

    def clean_string(self, value):
        return value.strip()

    clean_s_n = clean_description = clean_az_el = clean_string

class DateCleanerMixin(object):
    def clean_date(self, value):
        year, day, second = [int(v) for v in value.split(':')]
        if (year, day, second) == (0,0,0):
            return None
        
        age=2000
        if (year+age)>date.today().year:
            age = 1900
        
        return datetime(year+age, 1, 1) + timedelta(days=day, seconds=second)

    clean_data_start=clean_data_end=clean_mean_epoch=clean_ref_epoch=clean_date

class Recievers(DateCleanerMixin, ListBlock):
    def __init__(self, name='SITE/RECEIVER', **kwargs):
        super(Recievers, self).__init__(name, **kwargs)


class Antennas(DateCleanerMixin, ListBlock):
    def __init__(self, name='SITE/ANTENNA', **kwargs):
        super(Antennas, self).__init__(name, **kwargs)


class Eccentricities(DateCleanerMixin, ListBlock):
    def __init__(self, name='SITE/ECCENTRICITY', **kwargs):
        super(Eccentricities, self).__init__(name, **kwargs)


    def clean_arp_benchmark_m_up(self, value):
        return float(value.strip())

    clean_arp_benchmark_m_east = \
        clean_arp_benchmark_m_north = \
        clean_arp_benchmark_m_up

class Epochs(DateCleanerMixin, ListBlock):
    def __init__(self, name='SOLUTION/EPOCHS', **kwargs):
        super(Epochs, self).__init__(name, **kwargs)

class Estimates(DateCleanerMixin, ListBlock):
    headers = {'SOLN': (22, 26), 'INDEX': (1, 6), 'CODE': (14, 18), 'PT': (19, 21), 'ESTIMATED_VALUE': (47, 68), 'REF_EPOCH': (27, 39), 'S': (45, 46), 'STD_DEV': (69, 80), 'TYPE': (7, 13), 'UNIT': (40, 44)}
    def __init__(self, name='SOLUTION/ESTIMATE', **kwargs):
        super(Estimates, self).__init__(name, **kwargs)
    
    def clean_estimated_value(self, value):
        return float(value.strip())
    
    clean_std_dev = clean_estimated_value

class MatrixEstimates(ListBlock):
    def __init__(self, name='SOLUTION/MATRIX_ESTIMATE L CORR', **kwargs):
        super(MatrixEstimates, self).__init__(name, **kwargs)

    def default_clean(self, value):
        v = value.strip()
        return float(value) if v else None

    def clean_para1(self, value):
        return int(value)
    clean_para2 = clean_para1
