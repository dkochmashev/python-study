# Использование %:

# Переменные: количество участников первой команды (team1_num).
team1_num = 5
# Пример итоговой строки: "В команде Мастера кода участников: 5 !"
print("В команде Мастера кода участников: %d !" % team1_num)

# Переменные: количество участников в обеих командах (team1_num, team2_num).
team2_num = 6
# Пример итоговой строки: "Итого сегодня в командах участников: 5 и 6 !"
print("Итого сегодня в командах участников: %d и %d !" % (team1_num, team2_num))

# Использование format():

# Переменные: количество задач решённых командой 2 (score_2).
score_2 = 42
# Пример итоговой строки: "Команда Волшебники данных решила задач: 42 !"
print("Команда Волшебники данных решила задач: {score} !".format(score=score_2))

# Переменные: время за которое команда 2 решила задачи (team1_time).
team1_time = 18015.2
# Пример итоговой строки: "Волшебники данных решили задачи за 18015.2 с !"
print("Волшебники данных решили задачи за {:.1f} с !".format(team1_time))

# Использование f-строк:

# Переменные: количество решённых задач по командам: score_1, score_2
score_1 = 40
# Пример итоговой строки: "Команды решили 40 и 42 задач.”
print(f'Команды решили {score_1} и {score_2} задач.')
#
# Переменные: исход соревнования (challenge_result).
team2_time = 16234.2
if score_1 > score_2 or score_1 == score_2 and team1_time > team2_time:
    challenge_result = 'Победа команды Мастера кода!'
elif score_1 < score_2 or score_1 == score_2 and team1_time < team2_time:
    challenge_result = 'Победа команды Волшебники Данных!'
else:
    challenge_result = 'Ничья!'
# Пример итоговой строки: "Результат битвы: победа команды Мастера кода!"
print(f'Результат битвы: {challenge_result}')

# Переменные: количество задач (tasks_total) и среднее время решения (time_avg).
tasks_total = score_1 + score_2
time_avg = (team1_time + team2_time) / tasks_total
# Пример итоговой строки: "Сегодня было решено 82 задач, в среднем по 350.4 секунды на задачу!"
print(f'Сегодня было решено {tasks_total} задач, в среднем по {time_avg:.1f} секунды на задачу!')