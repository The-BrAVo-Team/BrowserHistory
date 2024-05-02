import datetime
import random

def generate_time_stamp(start_time, end_time):
    start = datetime.datetime.strptime(start_time, "%H:%M:%S")
    end = datetime.datetime.strptime(end_time, "%H:%M:%S")
    
    time_stamps = []
    current = start
    while current <= end:
        time_stamps.append(current.strftime("%H:%M:%S"))
        current += datetime.timedelta(seconds=random.randint(1, 10))  # Simulate random web usage duration
    return time_stamps

start = datetime.datetime.strptime("21-06-2020", "%d-%m-%Y")
end = datetime.datetime.strptime("07-07-2021", "%d-%m-%Y")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

for date in date_generated:
    start_time = "20:00:00"
    end_time = "22:30:00"
    time_stamps = generate_time_stamp(start_time, end_time)
    for timestamp in time_stamps:
        print(f'{date.strftime("%d-%m-%Y")} {timestamp}')
