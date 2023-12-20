# School-timetable-generator
Project for generating and evaluating school timetables in Python.
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