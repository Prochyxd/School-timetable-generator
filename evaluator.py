# evaluator.py

def has_duplicate_hours(schedule):
    """
    Check if a daily schedule has duplicate hours.

    Parameters:
    - schedule (list): Daily schedule to check for duplicate hours.

    Returns:
    - True if there are duplicate hours, False otherwise.
    """
    hours_set = set()
    for hour in schedule:
        if hour in hours_set:
            return True
        if hour != '____':
            hours_set.add(hour)
    return False

def count_free_hours(schedule):
    """
    Count the number of free hours (empty slots) in a daily schedule.

    Parameters:
    - schedule (list): Daily schedule to count free hours.

    Returns:
    - Number of free hours in the schedule.
    """
    return schedule.count('____')

def evaluate_schedule(schedule, evaluation_criteria):
    """
    Evaluate a daily schedule based on various criteria.

    Parameters:
    - schedule (tuple): Hashable format of the daily schedule.
    - evaluation_criteria (dict): Dictionary containing evaluation criteria and associated penalties/bonuses.

    Returns:
    - total_penalty (int): Total penalty based on the evaluation criteria.
    """
    total_penalty = 0

    for day, subjects in schedule:
        if has_duplicate_hours(subjects):
            total_penalty += evaluation_criteria['duplicate_hours_penalty']

        free_hours = count_free_hours(subjects)
        
        if free_hours > 1:
            total_penalty += evaluation_criteria['multiple_free_hours_penalty']

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
