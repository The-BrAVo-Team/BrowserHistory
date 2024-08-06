from datetime import datetime, timedelta

class epochConverter:
    def date_from_webkit(webkit_timestamp):
        epoch_start = datetime(1601, 1, 1)
        delta = timedelta(microseconds=int(webkit_timestamp))
        return epoch_start + delta

    def date_to_webkit(date_string):
        epoch_start = datetime(1601, 1, 1)
        date_ = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        diff = date_ - epoch_start
        microseconds_since_epoch = diff.days * 86400 * 10**6 + diff.seconds * 10**6 + diff.microseconds
        return '{:<017d}'.format(microseconds_since_epoch)

"""
# Webkit to date
print(epochConverter.date_from_webkit('13366155003000000'))  # 2024-07-22 20:50:03

# Date string to Webkit timestamp
print(epochConverter.date_to_webkit('2024-07-22 20:50:03'))  # 13366155003000000
"""