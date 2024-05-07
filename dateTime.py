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
    time_stamps.sort()  # Sort the timestamps
    return time_stamps

def create_date_time_output(start_date, end_date, start_time, end_time):
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    date_timestamps = []
    for date in date_generated:
        if random.random() < 0.5:  # Randomly skip some dates
            continue
        time_stamps = generate_time_stamp(start_time, end_time)
        num_timestamps = random.randint(1, min(len(time_stamps), 20))  # Randomly select number of timestamps
        selected_timestamps = random.sample(time_stamps, num_timestamps)
        for timestamp in selected_timestamps:
            date_timestamps.append(f'{date.strftime("%Y-%m-%d")} {timestamp}')
    return sorted(date_timestamps) # Sort the datetime output

if __name__ == '__main__':
    print(create_date_time_output("2021-05-22", "2021-06-22", "22:00:00", "23:00:00"))

