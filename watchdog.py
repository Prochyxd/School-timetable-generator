# watchdog.py

import itertools
from datetime import datetime
from multiprocessing import Manager, Pool, Event
from functools import partial
from generator import generate_and_count, print_schedule

def run_with_timeout(timeout, args):
    start_time = datetime.now()

    with Manager() as manager:
        count = manager.Value('i', 0)
        lock = manager.Lock()
        stop_event = Event()
        pool_args = (args[0], args[1], args[2], args[3], lock, stop_event)

        with Pool() as pool:
            result = pool.apply_async(partial(generate_and_count, *pool_args), itertools.count())

            try:
                result.get(timeout=timeout)
            except TimeoutError:
                stop_event.set()  # Set the event to signal termination
                pool.close()
                pool.join()  # Wait for processes to terminate
                elapsed_time = datetime.now() - start_time
                print(f"\n\nTimeout reached after {timeout} seconds.")
            else:
                pool.close()
                pool.join()
                elapsed_time = datetime.now() - start_time
                print(f"\n\nGenerated schedules: {count.value} in {elapsed_time}")

if __name__ == "__main__":
    subjects = ["M", "DS", "PSS", "A", "TV", "PIS", "TP", "C", "CIT", "WA", "PV", "AM"]
    teachers = {"M": "Hr", "DS": "Vc", "PSS": "Ms", "A": "Pa", "TV": "Lc", "PIS": "Bc", "TP": "Ms", "C": "Su",
                "CIT": "Mz", "WA": "Hs", "PV": "Ma", "AM": "Kl"}
    classrooms = {"M": [25], "DS": [25], "PSS": [8], "A": [29], "TV": ["TV"], "PIS": [19], "TP": [29], "C": [25],
                  "CIT": [17], "WA": [19], "PV": [19], "AM": [25]}

    timeout_seconds = 5  # adjust the timeout as needed
    processes = 4  # adjust the number of processes as needed

    args = (subjects, teachers, classrooms, processes)

    run_with_timeout(timeout_seconds, args)
