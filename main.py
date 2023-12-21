# main.py
import argparse
import yaml
from generator import generate_schedules
from watchdog import watchdog_timer
from multiprocessing import Process, Value, Lock

def parse_arguments():
    parser = argparse.ArgumentParser(description="School Schedule Generator")
    parser.add_argument("-r", "--random", action="store_true", help="Generate a random schedule")
    parser.add_argument("-n", "--num_schedules", type=int, default=1, help="Number of schedules to generate")
    parser.add_argument("-d", "--duration", type=int, default=10, help="Duration (in seconds) for generating schedules")
    parser.add_argument("-p", "--num_processes", type=int, default=4, help="Number of processes for parallel generation")
    return parser.parse_args()

def main():
    args = parse_arguments()

    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    # Initialize global variables for tracking the number of generated schedules
    counter = Value('i', 0)
    counter_lock = Lock()

    # Start the watchdog process to monitor the generation time
    watchdog_process = Process(target=watchdog_timer, args=(args.duration, counter, counter_lock))
    watchdog_process.start()

    # Generate schedules
    generated_schedules = generate_schedules(config, args.num_processes, args.duration, counter, counter_lock)

    # Wait for the watchdog process to finish
    watchdog_process.join()

if __name__ == "__main__":
    main()
