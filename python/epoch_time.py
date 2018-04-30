import time
from datetime import datetime as dt
from calendar import timegm

utc_time = time.strptime("2017-11-18T04:05:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
epoch_time = timegm(utc_time)

print('Epoch time for 2017-11-18T04:05:00.000Z: {0}'.format(epoch_time))

print('Date & time from epoch: {0}'.format(dt.utcfromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S')))
