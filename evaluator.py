# evaluator.py
def has_duplicate_hours(schedule):
    hours_set = set()
    for hour in schedule:
        if hour in hours_set:
            return True
        if hour != '____':
            hours_set.add(hour)
    return False

def count_free_hours(schedule):
    return schedule.count('____')

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

        # Check if M, C, or A is in the first hour and apply penalty
        if subjects and subjects[0] in {'M', 'C', 'A'}:
            total_penalty += evaluation_criteria['first_hour_penalty']

        # Check if there is a free hour in the first 4 hours and apply penalty
        if any(subject == '____' for subject in subjects[:4]):
            total_penalty += evaluation_criteria['free_hour_in_first_4_hours_penalty']

        # Check if more than 1 free hour and apply penalty
        free_hours = count_free_hours(subjects)
        if free_hours > 1:
            total_penalty += evaluation_criteria['multiple_free_hours_penalty'] * (free_hours - 1)

    return total_penalty
