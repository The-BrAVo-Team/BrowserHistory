from datetime import datetime, timedelta
import random

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
        
        # Generate a random integer between 0 and 999,999
        random_microseconds = random.randint(0, 999999)
        
        webkit_timestamp = microseconds_since_epoch + random_microseconds
        
        return webkit_timestamp


"""
# Webkit to date
print(epochConverter.date_from_webkit('13366155003000000'))  # 2024-07-22 20:50:03

# Date string to Webkit timestamp
print(epochConverter.date_to_webkit('2024-07-22 20:50:03'))  # 13366155003000000
"""