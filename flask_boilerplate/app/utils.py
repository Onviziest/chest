from datetime import datetime


def log(*args, **kwargs):
    now = datetime.now()
    s = '[{date:%H:%M:%S}]'.format(date=now)
    print(s, *args, **kwargs)
