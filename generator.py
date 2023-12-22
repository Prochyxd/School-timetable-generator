# generator.py
import random

def generate_daily_schedule(subjects, min_hours, max_hours, max_empty_hours):
    num_hours = random.randint(min_hours, max_hours)
    max_empty_hours = min(num_hours - 1, max_empty_hours)

    # Determine the number of empty slots
    num_empty_slots = min(max_empty_hours, 2)  # Increased to 2 for the maximum number of free hours

    # Create a list of subjects and empty slots
    schedule_items = subjects + ['____'] * num_empty_slots

    # Shuffle the list
    random.shuffle(schedule_items)

    # Trim the list to the desired number of hours
    daily_schedule = schedule_items[:num_hours]

    return daily_schedule
