import time
import config
import yaml
from generator import generate_schedule

def main():
    with open("config.yaml", "r") as config_file:
        config_data = yaml.safe_load(config_file)

    
    # Generate a random schedule
    schedule = generate_schedule(config_data)
    for day, subjects in schedule.items():
        print(f"{day}: {', '.join(subjects)}")

    #Generate as many schedules as possible in one minute
    num_schedules = 0
    start_time = time.time()

    while True:
        schedule = generate_schedule(config_data)
        num_schedules += 1

        elapsed_time = time.time() - start_time
        if elapsed_time >= 180:
            break

    print(f"Generated {num_schedules} schedules in {elapsed_time} seconds")

if __name__ == "__main__":
    main()



    #Generated 8694215 schedules in 180.0014967918396 seconds