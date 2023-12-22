# Schedule Generator

This program generates daily schedules based on provided criteria and evaluates them using specified penalties and bonuses. The generated schedules are then ranked based on their scores.

## File Structure

The project is organized into four main files:

1. **generator.py**: Contains functions for generating daily schedules.

2. **evaluator.py**: Contains functions for evaluating the quality of daily schedules.

3. **watchdog.py**: Implements a watchdog function to monitor progress and terminate the program after a specified time.

4. **main.py**: The main script that orchestrates the schedule generation process.

## How to Run

1. Ensure you have Python installed on your machine.

2. Install the required dependencies:
   ```bash
   pip install PyYAML

3. Create a configuration file named config.yaml with the following structure:
subjects:
  - subject1
  - subject2
  # Add more subjects as needed

days:
  - Monday
  - Tuesday
  - Wednesday
  - Thursday
  - Friday

hours_per_day:
  min: 6
  max: 10

max_empty_hours_per_day: 1

(mine is in config.yaml in this folder)

4. Run the main script:

bash

python main.py

5. Monitor the progress in the console. The program will terminate after 20 seconds.

6. View the generated schedule with the highest score in the console output.



Evaluation Criteria

The evaluation_criteria dictionary in main.py contains the penalties and bonuses for evaluating the quality of schedules. You can customize these values based on your preferences. The current criteria include penalties for duplicate hours, multiple free hours, and penalties/bonuses based on the total hours per day.

Additional Notes

    The program utilizes multiprocessing to speed up the schedule generation process by running multiple processes simultaneously.

    The watchdog function ensures that the program terminates after 20 seconds to prevent indefinite execution.

    The watchdog.py file is a standalone script that can be reused in other projects for monitoring progress.

THIS IS ADAM PROCHÁZKA´S PROJECT FOR SCHOOL PURPOSES (alfa 1)