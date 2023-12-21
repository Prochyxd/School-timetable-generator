import argparse
import yaml
from generator import generate_schedule

def parse_arguments():
    parser = argparse.ArgumentParser(description="School Schedule Generator")
    parser.add_argument("-r", "--random", action="store_true", help="Generate a random schedule")
    parser.add_argument("-n", "--num_schedules", type=int, default=1, help="Number of schedules to generate")
    return parser.parse_args()

def main():
    args = parse_arguments()

    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    if args.random:
        # Generate a random schedule
        schedule = generate_schedule(config)
        for day, subjects in schedule.items():
            print(f"{day}: {', '.join(subjects)}")

    else:
        # Generate and print the specified number of schedules
        for _ in range(args.num_schedules):
            schedule = generate_schedule(config)
            for day, subjects in schedule.items():
                print(f"{day}: {', '.join(subjects)}")
            print("\n---\n")  # Separation between schedules

if __name__ == "__main__":
    main()
