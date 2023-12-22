import yaml
import random

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

def generate_schedule(config):
    schedule = {}

    for day in config['days']:
        daily_schedule = generate_daily_schedule(
            config['subjects'],
            config['hours_per_day']['min'],
            config['hours_per_day']['max'],
            config['max_empty_hours_per_day']
        )
        schedule[day] = daily_schedule

    return schedule