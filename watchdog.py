# watchdog.py

import time
import multiprocessing

def watchdog(progress_counter, start_time, exit_flag):
    """
    Watchdog function that monitors the progress of schedule generation and terminates after a specified time.

    Parameters:
    - progress_counter (multiprocessing.Value): Counter for the progress of schedule generation.
    - start_time (float): Start time of the schedule generation.
    - exit_flag (multiprocessing.Value): Flag to signal termination.

    Returns:
    - None (runs indefinitely until the exit flag is set or time limit is reached).
    """
    while not exit_flag.value:
        with progress_counter.get_lock():
            progress = progress_counter.value
        print(f"Progress: {progress} schedules generated")
        time.sleep(0.1)

        # Check if the time limit (20 seconds) has been reached
        if time.time() - start_time >= 20:
            with exit_flag.get_lock():
                exit_flag.value = 1
            break
