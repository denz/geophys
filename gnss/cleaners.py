from datetime import datetime, timedelta, date
def clean_date(value):
    year, day, second = [int(v) for v in value.split(':')]
    if (year, day, second) == (0,0,0):
        return None
    
    age=2000
    if (year+age)>date.today().year:
        age = 1900
    
    return datetime(year+age, 1, 1) + timedelta(days=day, seconds=second)
