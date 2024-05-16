# Исходные данные
grades = [[5, 3, 3, 5, 4], [2, 2, 2, 3], [4, 5, 5, 2], [4, 4, 3], [5, 5, 5, 4, 5]]
students = {'Johnny', 'Bilbo', 'Steve', 'Khendrik', 'Aaron'}

# Словарь со средними оценками учеников
average_grade = {}

i = 0   # Индекс элемента списка оценок (grades)
for student_name in sorted(students):
    average_grade[student_name] = sum(grades[i]) / len(grades[i])
    i = i + 1

print(average_grade)
