# Ваша задача:
# 1. Создайте новый класс Building
# 2. Создайте инициализатор для класса Building, который будет задавать целочисленный атрибут этажности self.numberOfFloors и строковый атрибут self.buildingType
# 3. Создайте(перегрузите) __eq__, используйте атрибут numberOfFloors и buildingType для сравнения
# 4. Полученный код напишите в ответ к домашнему заданию

# Не полагаемся на внешние модули, а используем управляющие последовательности терминала ANSI

# Стиль текста оглавлений
def heading(text):
    print(f'\033[1m\033[30m\033[42m{text}\033[0m')

# Стиль текста повествования
def narrative(text):
    print(f'\033[3m\033[32m{text}\033[0m')


class Building:
    def __init__(self, numberOfFloors = 0):
        self.numberOfFloors = numberOfFloors

    def __str__(self):
        return f'здание, у которого {self.spellNumberOfFloors()}'

    def __bool__(self):
        return self.numberOfFloors > 0

    def __eq__(self, other):
        return self.numberOfFloors == other.numberOfFloors

    def __lt__(self, other):
        return self.numberOfFloors < other.numberOfFloors

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __str__(self):
        return f'Здание, у которого {self.spellNumberOfFloors()}'

    # Формирует число этажей прописью
    def spellNumberOfFloors(self):
        if self.numberOfFloors == 0:
            return 'есть только фундамент'

        lastDigit = self.numberOfFloors % 10
        spellTemplate = f'{self.numberOfFloors} этаж'

        # 1 этаж
        if lastDigit == 1 and self.numberOfFloors != 11:
            return spellTemplate
        # 2, 3, 4 этажа
        elif 2 <= lastDigit <= 4 and not 12 <= self.numberOfFloors <= 14 :
            return f'{spellTemplate}а'
        # N этажей (во всех остальных случаях)
        return f'{spellTemplate}ей'


def describe_building(building):
    # Преобразование к типу bool
    if building:
        print('Построено', str(building).lower())
    else:
        print('Здание еще не построено.')

def compare_two_buildings(building1, building2):
    # Преобразование к типу bool
    if building1:
        print('Первое', building1, end=' ')
    else:
        print('Фундамент первого здания', end=' ')

    if building1 == building2:
        print('такой же высоты, как и', end=' ')
    elif building1 < building2:
        print('ниже, чем', end=' ')
    else:
        print('выше, чем', end=' ')

    if building2:
        print('второе', building2)
    else:
        print('фундамент второго здания')

heading('Проверяем преобразование объекта в тип bool')

narrative('Описываем пустой объект')
describe_building(Building())
narrative('Описываем не пустой объект')
describe_building(Building(2))

print()

heading('Проверяем перегрузку операторов сравнения')

narrative('Сравниваем меньшее с большим')
compare_two_buildings(Building(3), Building(33))
narrative('Сравниваем большее с меньшим')
compare_two_buildings(Building(5), Building(2))
narrative('Сравниваем равное')
compare_two_buildings(Building(9), Building(9))
narrative('Сравниваем пустое с не пустым')
compare_two_buildings(Building(), Building(1))
narrative('Сравниваем не пустое с пустым')
compare_two_buildings(Building(2), Building())
narrative('Сравниваем пустое с пустым')
compare_two_buildings(Building(), Building())
