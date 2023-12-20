# generator.py

import itertools
import random
import logging
from multiprocessing import Manager, Pool, cpu_count
from functools import partial

def generate_schedule(subjects, teachers, classrooms, days=5, periods_per_day=9):
    schedule = []
    for day in range(days):
        daily_schedule = generate_daily_schedule(subjects, teachers, classrooms, periods_per_day)
        schedule.append(daily_schedule)
    return schedule

def generate_daily_schedule(subjects, teachers, classrooms, periods_per_day):
    daily_schedule = []
    for period in range(periods_per_day):
        subject = random.choice(subjects)
        teacher = random.choice(teachers[subject])
        classroom = random.choice(classrooms[subject])
        daily_schedule.append((subject, teacher, classroom))
    return daily_schedule

def print_schedule(schedule):
    logging.info("\nGenerated Schedule:")
    for day, daily_schedule in enumerate(schedule, start=1):
        logging.info(f"\nDay {day}:")
        for period, (subject, teacher, classroom) in enumerate(daily_schedule, start=1):
            logging.info(f"  Period {period}: Subject={subject}, Teacher={teacher}, Classroom={classroom}")

def generate_and_count(args):
    subjects, teachers, classrooms, schedule_count, lock = args
    schedule = generate_schedule(subjects, teachers, classrooms)
    with lock:
        schedule_count.value += 1
        logging.info(f"\rGenerated schedules: {schedule_count.value}")
        print_schedule(schedule)  # Print the generated schedule
    return schedule

def generate_schedules_parallel(args):
    subjects, teachers, classrooms, processes = args
    with Manager() as manager:
        schedule_count = manager.Value('i', 0)
        lock = manager.Lock()
        partial_generate = partial(generate_and_count, (subjects, teachers, classrooms, schedule_count, lock))
        with Pool(processes=processes) as pool:
            pool.map(partial_generate, itertools.count())

if __name__ == "__main__":
    import sys
    logging.basicConfig(filename='generator_log.txt', level=logging.INFO)

    subjects = ["M", "DS", "PSS", "A", "TV", "PIS", "TP", "C", "CIT", "WA", "PV", "AM"]
    teachers = {"M": "Hr", "DS": "Vc", "PSS": "Ms", "A": "Pa", "TV": "Lc", "PIS": "Bc", "TP": "Ms", "C": "Su",
                "CIT": "Mz", "WA": "Hs", "PV": "Ma", "AM": "Kl"}
    classrooms = {"M": [25], "DS": [25], "PSS": [8], "A": [29], "TV": ["TV"], "PIS": [19], "TP": [29], "C": [25],
                  "CIT": [17], "WA": [19], "PV": [19], "AM": [25]}

    processes = cpu_count()  # Use all available CPU cores

    args = (subjects, teachers, classrooms, processes)

    generate_schedules_parallel(args)
