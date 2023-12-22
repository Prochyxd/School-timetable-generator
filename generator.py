# generator.py

import random

def generate_daily_schedule(subjects, min_hours, max_hours, max_empty_hours):
    """
    Generate a daily schedule with random subjects and a varying number of empty slots.

    Parameters:
    - subjects (list): List of subjects.
    - min_hours (int): Minimum number of hours in a daily schedule.
    - max_hours (int): Maximum number of hours in a daily schedule.
    - max_empty_hours (int): Maximum number of empty slots in a daily schedule.

    Returns:
    - daily_schedule (list): Generated daily schedule.
    """
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
