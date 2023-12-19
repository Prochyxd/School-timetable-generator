"""
This file is for generating A LOT OF SCHEDULES (timetables) for our school.
It will be using cores/threads on procesor to generate a big amout of school schedules/timetables.
When I say A LOT I mean A LOT. It must be generating over 50 000 schedules/timetables in 1 second.
It should be using all of the procesor's cores.
This code should run parallel.
"""
"""
Our school has subjects: M, DS, PSS, A, TV, PIS, TP, C, CIT, WA, PV, AM
Our school has teachers(subject they teach): Hr(M), Vc(DS), Ms(PSS), Pa(A), Lc(TV), Bc(PIS), Ms(TP), Su(C), Mz(CIT), Hs(WA), Ma(PV), Kl(AM)
Our school has classrooms(floor they are on, subjects taught there): 25(4, M, A, TP, C, AM), 19(3, PV, PIS, WA), 8(2, PSS), 29(4, A), TV(0, TV), 17(3, CIT, DS), 18(3, PV, PIS, WA)
Our school has days: Monday, Tuesday, Wednesday, Thursday, Friday
Our school should have between 6 - 9 hours per day
"""
import concurrent.futures
import random
import time

class ScheduleGenerator:
    def __init__(self):
        self.subjects = ["M", "DS", "PSS", "A", "TV", "PIS", "TP", "C", "CIT", "WA", "PV", "AM"]
        self.teachers = ["Hr", "Vc", "Ms", "Pa", "Lc", "Bc", "Ms", "Su", "Mz", "Hs", "Ma", "Kl"]
        self.classrooms = ["25", "19", "8", "29", "TV", "17", "18"]
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.hours = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.schedules = []
        self.scheduleCounter = 0

    def generateSchedule(self):
        schedule = []

        for _ in range(len(self.subjects)):
            subject = random.choice(self.subjects)
            teacher = random.choice(self.teachers)
            classroom = random.choice(self.classrooms)
            day = random.choice(self.days)
            hour = random.choice(self.hours)

            schedule.append(f'"{subject}, {teacher}, {classroom}"')

        return day, schedule

    def generateSchedules(self, amount):
        schedules = []

        for _ in range(amount):
            day, schedule = self.generateSchedule()
            schedules.append((day, schedule))

        return schedules

    def parallelGenerateSchedules(self, total_amount, num_threads):
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Rozdělíme práci mezi vlákna
            tasks = [executor.submit(self.generateSchedules, total_amount // num_threads) for _ in range(num_threads)]

            # Čekáme na dokončení všech úkolů
            concurrent.futures.wait(tasks)

            # Kombinujeme výsledky
            for task in tasks:
                self.schedules.extend(task.result())

    def printGeneratedSchedules(self):
        for day, schedule in self.schedules:
            print(f"{day}:\t{', '.join(schedule)}")

if __name__ == "__main__":
    generator = ScheduleGenerator()

    start_time = time.time()

    # Generujeme rozvrhy paralelně s 4 vlákny
    generator.parallelGenerateSchedules(total_amount=50000, num_threads=4)
    # Vytiskneme vygenerované rozvrhy
    generator.printGeneratedSchedules()

    end_time = time.time()

    print(f"Generated 50000 schedules in {end_time - start_time:.2f} seconds.")


