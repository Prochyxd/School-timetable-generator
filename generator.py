"""
This file is for generating A LOT OF random SCHEDULES (timetables) for our school.
It will be using cores/threads on procesor to generate a big amout of school schedules/timetables.
When I say A LOT I mean A LOT.
It should be using all of the procesor's cores parallelly.
"""
"""
Our school has subjects: M, DS, PSS, A, TV, PIS, TP, C, CIT, WA, PV, AM
Our school has teachers(subject they teach): Hr(M), Vc(DS), Ms(PSS), Pa(A), Lc(TV), Bc(PIS), Ms(TP), Su(C), Mz(CIT), Hs(WA), Ma(PV), Kl(AM)
Our school has classrooms(floor they are on, subjects taught there): 25(4, M, A, TP, C, AM), 19(3, PV, PIS, WA), 8(2, PSS), 29(4, A), TV(0, TV), 17(3, CIT, DS), 18(3, PV, PIS, WA)
Our school has days: Monday, Tuesday, Wednesday, Thursday, Friday
Our school should have between 6 - 9 hours per day
"""
import itertools
from multiprocessing import Pool
import time

# Definition of data
subjects = ["M", "DS", "PSS", "A", "TV", "PIS", "TP", "C", "CIT", "WA", "PV", "AM"]
teacher_subjects = {"Hr": ["M"], "Vc": ["DS"], "Ms": ["PSS"], "Pa": ["A"], "Lc": ["TV"],
                    "Bc": ["PIS"], "Ms": ["TP"], "Su": ["C"], "Mz": ["CIT"], "Hs": ["WA"], "Ma": ["PV"], "Kl": ["AM"]}
classrooms = {"25": ["M", "A", "TP", "C", "AM"], "19": ["PV", "PIS", "WA"], "8": ["PSS"],
              "29": ["A"], "TV": ["TV"], "17": ["CIT", "DS"], "18": ["PV", "PIS", "WA"]}

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
hours = list(range(6, 10))

def generate_schedules(permutation):
    schedules = []
    for day_permutation in itertools.permutations(permutation):
        for hour_permutation in itertools.permutations(hours):
            schedule = {day: {hour: None for hour in hours} for day in day_permutation}
            for i, day in enumerate(day_permutation):
                for j, hour in enumerate(hour_permutation):
                    subject = permutation[i * len(hours) + j]
                    classroom = find_classroom(subject)
                    teacher = find_teacher(subject)
                    schedule[day][hour] = {"subject": subject, "classroom": classroom, "teacher": teacher}
            schedules.append(schedule)
    return schedules

def find_classroom(subject):
    for classroom, content in classrooms.items():
        if subject in content:
            return classroom
    return None

def find_teacher(subject):
    for teacher, subjects_taught in teacher_subjects.items():
        if subject in subjects_taught:
            return teacher
    return None

def print_schedule_count_and_schedules(count, schedules):
    print(f"Generated schedules: {count}")
    for schedule in schedules:
        print_schedule(schedule)

def print_schedule(schedule):
    print("Generated Schedule:")
    for day, hours in schedule.items():
        print(f"{day}: {hours}")

if __name__ == "__main__":
    permutations_subjects = list(itertools.permutations(subjects))
    permutations_days = list(itertools.permutations(days))

    num_cores = 6  # Change this to the number of available cores on your computer
    permutations_subjects_chunked = [permutations_subjects[i::num_cores] for i in range(num_cores)]

    with Pool(num_cores) as pool:
        results = []
        schedule_count = 0
        start_time = time.time()
        print_interval = 1  # Print count every second
        while True:
            for result in pool.imap_unordered(generate_schedules, permutations_subjects_chunked):
                results.append(result)
                schedule_count += len(result)

            current_time = time.time()
            elapsed_time = current_time - start_time
            # Print the count and schedules every second
            if elapsed_time >= print_interval:
                print_schedule_count_and_schedules(schedule_count, [schedule for result in results for schedule in result])
                start_time = current_time
                schedule_count = 0  # Reset count

    # The loop is infinite, so this part will never be reached in normal circumstances
    # If you want to continue working with the final_schedules, you might consider breaking out of the loop.
    final_schedules = [schedule for result in results for schedule in result]
    print(f"Total number of generated schedules: {len(final_schedules)}")