# main.py

import yaml
import multiprocessing
import time

from generator import generate_daily_schedule
from evaluator import has_duplicate_hours, evaluate_schedule
from watchdog import watchdog

def generate_schedule_worker(config, output_queue, progress_counter, exit_flag, best_schedule_lock, best_schedule, evaluation_criteria):
    """
    Worker function for generating schedules.

    Parameters:
    - config (dict): Configuration data loaded from `config.yaml`.
    - output_queue (multiprocessing.Queue): Queue for storing generated schedules.
    - progress_counter (multiprocessing.Value): Counter for the progress of schedule generation.
    - exit_flag (multiprocessing.Value): Flag to signal termination.
    - best_schedule_lock (multiprocessing.Lock): Lock for accessing the best schedule.
    - best_schedule (multiprocessing.Manager().list): Manager list for storing the best schedule.
    - evaluation_criteria (dict): Dictionary containing evaluation criteria and associated penalties/bonuses.

    Returns:
    - None
    """
    while not exit_flag.value:
        schedule = {}
        for day in config['days']:
            daily_schedule = generate_daily_schedule(
                config['subjects'],
                config['hours_per_day']['min'],
                config['hours_per_day']['max'],
                config['max_empty_hours_per_day']
            )
            schedule[day] = daily_schedule

        # Convert the schedule to a hashable format
        schedule_tuple = tuple((day, tuple(subjects)) for day, subjects in schedule.items())

        score = evaluate_schedule(schedule_tuple, evaluation_criteria)

        with best_schedule_lock:
            current_best_score = evaluate_schedule(best_schedule[0][0], evaluation_criteria) if best_schedule else float('-inf')
            if score > current_best_score:
                best_schedule[:] = [(schedule_tuple, score)]

        output_queue.put(schedule)
        with progress_counter.get_lock():
            progress_counter.value += 1

def main():
    with open("config.yaml", "r") as config_file:
        config_data = yaml.safe_load(config_file)

    num_processes = multiprocessing.cpu_count()

    output_queue = multiprocessing.Queue()
    progress_counter = multiprocessing.Value('i', 0)
    exit_flag = multiprocessing.Value('i', 0)
    best_schedule_lock = multiprocessing.Lock()
    best_schedule = multiprocessing.Manager().list()
    
    # Define your evaluation criteria here
    evaluation_criteria = {
        'duplicate_hours_penalty': -1000,
        'multiple_free_hours_penalty': -100,
        '6_hours_bonus': 100,
        '7_hours_bonus': 50,
        '8_hours_penalty': -1,
        '9_hours_penalty': -100,
        '10_hours_penalty': -250
        # Add more criteria as needed
    }

    processes = [
        multiprocessing.Process(
            target=generate_schedule_worker,
            args=(config_data, output_queue, progress_counter, exit_flag, best_schedule_lock, best_schedule, evaluation_criteria)
        )
        for _ in range(num_processes)
    ]

    for process in processes:
        process.start()

    # Watchdog loop
    start_time = time.time()
    watchdog_process = multiprocessing.Process(
        target=watchdog,
        args=(progress_counter, start_time, exit_flag)
    )
    watchdog_process.start()

    for process in processes:
        process.join(timeout=1)  # Add a timeout to prevent indefinite waiting

    # Wait for the watchdog process to finish
    watchdog_process.join()

    # Find the best schedule among the generated ones
    best_schedule_list = best_schedule[:]
    best_schedule_list.sort(key=lambda x: x[1], reverse=True)
    
    # Print the best schedule
    print("Best Schedule:")
    if best_schedule_list:
        best_schedule_dict, best_score = best_schedule_list[0]
        for day, subjects in best_schedule_dict:
            print(f"{day}: {', '.join(subjects)}")
        print(f"Score: {best_score}")
    else:
        print("No schedules generated.")
        
    with progress_counter.get_lock():
        generated_schedules = progress_counter.value
    print(f"Generated {generated_schedules} schedules in 20 seconds")

if __name__ == "__main__":
    main()
