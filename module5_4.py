# Ваша задача:
# 1. Создайте новый класс Buiding с атрибутом total
# 2. Создайте инициализатор для класса Buiding, который будет увеличивать атрибут количества созданных объектов класса Building total
# 3. В цикле создайте 40 объектов класса Building и выведите их на экран командой print
# 4. Полученный код напишите в ответ к домашнему заданию

class Building:
    # Частный атрибут класса
    __total = 0

    def __init__(self):
        Building.__total += 1

    def __del__(self):
        Building.__total -= 1

    def built():
        return Building.__total

buildings = list()

# Строим микрорайон
for i in range(40):
    buildings.append(Building())

print(f'Построено {Building.built()} зданий')

# Вызываем бульдозеры...
del buildings

print(f'Осталось {Building.built()} зданий')
