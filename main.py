import yaml
import random
import time
import multiprocessing

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

def has_duplicate_hours(schedule):
    hours_set = set()
    for hour in schedule:
        if hour in hours_set:
            return True
        if hour != '____':
            hours_set.add(hour)
    return False

def evaluate_schedule(schedule, evaluation_criteria):
    total_penalty = 0

    for day, subjects in schedule:
        if has_duplicate_hours(subjects):
            total_penalty += evaluation_criteria['duplicate_hours_penalty']

        daily_hours = len(subjects)
        if daily_hours == 6:
            total_penalty += evaluation_criteria['6_hours_bonus']
        elif daily_hours == 7:
            total_penalty += evaluation_criteria['7_hours_bonus']
        elif daily_hours == 8:
            total_penalty += evaluation_criteria['8_hours_penalty']
        elif daily_hours == 9:
            total_penalty += evaluation_criteria['9_hours_penalty']
        elif daily_hours == 10:
            total_penalty += evaluation_criteria['10_hours_penalty']

    return total_penalty

def generate_schedule_worker(config, output_queue, progress_counter, exit_flag, best_schedule_lock, best_schedule, evaluation_criteria):
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
    while time.time() - start_time < 20:
        with progress_counter.get_lock():
            progress = progress_counter.value
        print(f"Progress: {progress} schedules generated")
        time.sleep(0.1)

    # Set exit flag to terminate processes
    with exit_flag.get_lock():
        exit_flag.value = 1

    # Wait for processes to finish
    for process in processes:
        process.join(timeout=1)  # Add a timeout to prevent indefinite waiting

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
