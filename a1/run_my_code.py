# Replace with the name of your file *without* .py
# also it needs to have no "-" or " " characters in it
import a1_MichaelCrystal as student_code

some_students = student_code.read_data("responses-wi23.csv")
print(some_students[1])
print(f"{student_code.count_answers(some_students)} questions")
print(f"{student_code.count_10Q(some_students)} like 10Q")
print(f"{student_code.count_CS(some_students)} are CS majors")
print(f"{len(student_code.list_tea(some_students))} like tea")
print(f"{len(student_code.list_coffee(some_students))} like coffee")
print(f"{student_code.count_by_year(some_students, 2026)} are 2026")
print(f"{len(student_code.find_students_south_of_wisconsin(some_students))} have never travelled as north as wisconsin")

south_winner = student_code.find_southernmost_student(some_students)
north_winner = student_code.find_northernmost_student(some_students)

print(f"{south_winner} is the farthest south")
print(f"{north_winner} is the farthest north")

