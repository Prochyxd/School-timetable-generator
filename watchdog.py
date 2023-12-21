# watchdog.py
import time
from multiprocessing import Value, Lock

def watchdog_timer(timeout, counter, counter_lock):
    """
    Watchdog timer tracking the generation of schedules and terminating it after a specified time.
    """
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time

        with counter_lock:
            generated_schedules = counter.value

        print(f'Generated schedules: {generated_schedules}, Time: {elapsed_time:.2f} seconds')

        if elapsed_time >= timeout:
            print(f'Time limit ({timeout} seconds) reached. Stopping the generator.')
            break

        time.sleep(1)
