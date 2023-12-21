# generator.py
import yaml
import random
import concurrent.futures
import time
from itertools import repeat

def generate_daily_schedule(subjects, min_hours, max_hours, max_empty_hours):
    num_hours = random.randint(min_hours, max_hours)
    max_empty_hours = min(num_hours - 1, max_empty_hours)

    # Determine the number of empty slots (at most one)
    num_empty_slots = min(max_empty_hours, 1)

    # Create a list of subjects and empty slots
    schedule_items = subjects + ['____'] * num_empty_slots

    # Shuffle the list
    random.shuffle(schedule_items)

    # Trim the list to the desired number of hours
    daily_schedule = schedule_items[:num_hours]

    return daily_schedule

def generate_schedule_for_day(config, day, counter, counter_lock):
    daily_schedule = generate_daily_schedule(
        config['subjects'],
        config['hours_per_day']['min'],
        config['hours_per_day']['max'],
        config['max_empty_hours_per_day']
    )

    with counter_lock:
        counter.value += 1

    return day, daily_schedule

def generate_schedules(config, num_processes, duration, counter, counter_lock):
    schedules = {}
    days = config['days']
    
    def generate_schedule_for_day_wrapper(args):
        return generate_schedule_for_day(*args)

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        args_list = zip(repeat(config), days, repeat(counter), repeat(counter_lock))
        results = executor.map(generate_schedule_for_day_wrapper, args_list)

    for result in results:
        day, daily_schedule = result
        schedules[day] = daily_schedule

    print(f"Generated {counter.value} schedules in {duration:.2f} seconds")

    return schedules
