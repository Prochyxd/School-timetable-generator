# watchdog.py
import time

def watchdog(progress_counter, start_time, exit_flag):
    while not exit_flag.value and time.time() - start_time < 20:
        with progress_counter.get_lock():
            progress = progress_counter.value
        print(f"Progress: {progress} schedules generated")
        time.sleep(0.1)
    print("Watchdog terminated")
