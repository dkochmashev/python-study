# Ваша задача:
# 1. Создайте новый класс House
# 2. Создайте инициализатор для класса House, который будет задавать атрибут этажности self.numberOfFloors = 0
# 3. Создайте метод setNewNumberOfFloors(floors), который будет изменять атрибут numberOfFloors на параметр floors и выводить в консоль numberOfFloors
# 4. Полученный код напишите в ответ к домашнему заданию

# Скромное задание, подумал я...
# И решил поупражняться с классами как следует.
# Объектная модель спроектирована без должной глубины мысли, но критика все-равно приветствуется.


# Не полагаемся на внешние модули, а используем управляющие последовательности терминала ANSI

# Стиль текста оглавлений
def heading(text):
    print(f'\033[1m\033[30m\033[42m{text}\033[0m')

# Стиль текста повествования
def narrative(text):
    print(f'\033[3m\033[32m{text}\033[0m')

class Building:
    '''
    Абстрактное многоэтажное строение, характеризуемое только числом этажей
    '''
    # Число этажей является частным атрибутом, и доступен только через вызов методов класса
    __numberOfFloors = None

    def __init__(self):
        self.__numberOfFloors = 0
        print('Подготовлена строительная площадка')

    def __len__(self):
        return self.__numberOfFloors

    def __del__(self):
        print('Строение уничтожено')

    def getNumberOfFloors(self):
        return self.__numberOfFloors

    def setNewNumberOfFloors(self, floors):
        if self.isValidFloorNumberInput(floors):
            self.__numberOfFloors = floors
            return True
        return False

    def isValidFloorNumberInput(self, floorNumber):
        # Номер этажа или число этажей не должны быть отрицательными
        if floorNumber >= 0:
            return True
        return False

    # Формирует число этажей прописью
    def spellNumberOfFloors(self):
        if self.__numberOfFloors == 0:
            return 'есть только основание'

        lastDigit = self.__numberOfFloors % 10
        spellTemplate = f'{self.__numberOfFloors} этаж'

        # 1 этаж
        if lastDigit == 1 and self.__numberOfFloors != 11:
            return spellTemplate
        # 2, 3, 4 этажа
        elif 2 <= lastDigit <= 4 and not 12 <= self.__numberOfFloors <= 14 :
            return f'{spellTemplate}а'
        # N этажей (во всех остальных случаях)
        return f'{spellTemplate}ей'

class ResizableBuilding(Building):
    '''
    Строение, способное на лету изменять (достраивать недостающее или уничтожать лишнее) число этажей
    '''
    def __init__(self, floorBuilder):
        super().__init__()
        self.builder = floorBuilder

    def setNewNumberOfFloors(self, floors):
        # Проверяем корректность значения аргумента
        if not self.isValidFloorNumberInput(floors):
            return False

        currentFloorCount = self.getNumberOfFloors()

        # Кол-во этажей без изменений
        if floors == currentFloorCount:
            return False

        # Этажей становится БОЛЬШЕ, чем есть сейчас
        if abs(floors) > abs(currentFloorCount):
            super().setNewNumberOfFloors(
                self.builder.buildNewFloors(self.getNumberOfFloors(), floors - currentFloorCount)
            )
        # Этажей становится МЕНЬШЕ, чем есть сейчас
        else:
            super().setNewNumberOfFloors(
                self.builder.destroyUnusedFloors(self.getNumberOfFloors(), currentFloorCount - floors)
            )
        # Число этажей изменилось
        return True

class FloorBuilder:
    '''
    Бригада строителей абстрактных этажей
    '''
    def __init__(self, **kwargs):
        self.floorBuildMessage = kwargs['floorBuildMessage']
        self.floorDestroyMessage = kwargs['floorDestroyMessage']
        self.floorNumberSign = kwargs['floorNumberSign']

    def buildNewFloors(self, currentFloorCount, numberOfFloorsToAdd):
        for newFloorNumber in range(numberOfFloorsToAdd):
            print(self.floorBuildMessage, (currentFloorCount + newFloorNumber + 1) * self.floorNumberSign)
        return currentFloorCount + numberOfFloorsToAdd

    def destroyUnusedFloors(self, currentFloorCount, numberOfFloorsToDestroy):
        for destroyedFloorNumber in range(numberOfFloorsToDestroy):
            print(self.floorDestroyMessage, (currentFloorCount - destroyedFloorNumber) * self.floorNumberSign)
        return currentFloorCount - numberOfFloorsToDestroy

class House(ResizableBuilding):
    '''
    Многоэтажный жилой дом в комплекте с бригадой строителей,
    автоматически подстраивающих его под желаемые размеры
    '''
    def __init__(self):
        super().__init__(
            FloorBuilder(
                floorBuildMessage='Быстренько достраиваем этаж',
                floorDestroyMessage='Превращаем в прах этаж',
                floorNumberSign=1
            )
        )

    # Переопределение данного метода требуется для перехвата попыток изменения
    # числа этажей втихаря, т.е. минуя этап их строительства.
    def __setattr__(self, key, value):
        # Перехватываем попытки изменения ключевого свойства объекта в обход интерфейса класса
        if key == 'numberOfFloors':
            if super().setNewNumberOfFloors(value):
                print('Теперь у дома', self.spellNumberOfFloors())
            else:
                print('У дома по прежнему', self.spellNumberOfFloors())
        # Для изменения всех остальных свойств объекта вызываем соответствующий метод базового класса
        else:
            super().__setattr__(key, value)

    # Представление объекта в виде строки
    def __str__(self):
        return f'Дом, у которого {self.spellNumberOfFloors()}'

    def __del__(self):
        print('Дом снесен')
        super().__del__()

    def setNewNumberOfFloors(self, floors):
        self.numberOfFloors = floors


class Bunker(ResizableBuilding):
    '''
    Многоуровневый бункер в комплекте с бригадой землекопов,
    автоматически подстраивающих его под желаемые размеры
    '''
    def __init__(self):
        super().__init__(
            FloorBuilder(
                floorBuildMessage = 'Бодро копаем этаж',
                floorDestroyMessage = 'Заваливаем грунтом этаж',
                floorNumberSign = -1
            )
        )

    # Переопределение данного метода требуется для перехвата попыток изменения
    # числа этажей втихаря, т.е. минуя этап их строительства.
    def __setattr__(self, key, value):
        # Перехватываем попытки изменения ключевого свойства объекта в обход интерфейса класса
        if key == 'numberOfFloors':
            if super().setNewNumberOfFloors(value):
                print('Теперь у бункера', self.spellNumberOfFloors())
            else:
                print('У бункера по прежнему', self.spellNumberOfFloors())
        # Для изменения всех остальных свойств объекта вызываем соответствующий метод базового класса
        else:
            super().__setattr__(key, value)

    # Представление объекта в виде строки
    def __str__(self):
        return f'Бункер, у которого {self.spellNumberOfFloors()}'

    def __del__(self):
        print('Бункер закопан')
        super().__del__()

    def setNewNumberOfFloors(self, floors):
        self.numberOfFloors = floors


heading("Сначала действуем строго по ТЗ, т.е. строим дом")
print()

narrative("Решили мы построить дом...")
house = House()
print(house)

narrative("Пять этажей воздвигли в нём.")
house.setNewNumberOfFloors(5)

narrative("Но тень от стен на двор легла,\n"
          "и этажей в нём стало два...")
house.setNewNumberOfFloors(2)

narrative("Тут ипотечный бум настал,\n"
          "Равшан свой инструмент достал.\n"
          'Насяльникэ сказал: "Вперёд!"\n'
          "Дом превратился в небоскрёб.")
house.setNewNumberOfFloors(120)

narrative("Вдруг дунул свежий ветерок,\n"
          "Качнулся дом и на бок лёг.\n"
          "Труд светлых дней и тьмы ночей -\n"
          "Теперь лишь груда кирпичей.")
house.setNewNumberOfFloors(0)

narrative("Ноль этажей иль дома нет.\n"
          "Как ни скажи, а смысл равен.\n"
          "Признаемся, друзья, теперь\n"
          "У нас всего лишь есть фундамент.")
house.setNewNumberOfFloors(0)

narrative("Начнем мы с чиатого листа,\n"
          "И уничтожим все былое...")
del house

narrative("Решили мы построить дом.")
house = House()

narrative("Теперь мы действуем с умом.\n"
          "Джамшут нам быстро возведёт\n"
          "Тринадцать этажей на счастье!")
house.setNewNumberOfFloors(13)
print(house)

narrative("А теперь прозаично пытаемся напрямую изменить свойство объекта.")
house.numberOfFloors = -1   # Ошибочный ввод кол-ва этажей не приведет к изменению состояния объекта
house.numberOfFloors = 0    # Это даст тот же результат, что и вызов setNewNumberOfFloors(0)
print(house)

print()
heading("Теперь построим дом наоборот, т.е. выкопаем бункер")
print()

narrative("Во глубине сибирских руд\n"
          "Решили выкопать мы бункер\n"
          "Не пропадет наш скорбный труд\n"
          "И может сами будем целы...")
bunker = Bunker()
print(bunker)

narrative("Копали бункер вчетвером:\n"
          "Иван, Василий, лом, лопата")
bunker.setNewNumberOfFloors(10)
narrative("Был результат наш - о-го-го!")
print('Выкопано', len(bunker), 'этажей!!!')

narrative("И даже мы перестарались.")
bunker.setNewNumberOfFloors(2)

narrative("Потом приехал Николай\n"
          "На экскаваторе японском\n"
          "Ему сказали закопать\n"
          "Всё наше чудное творенье.")
bunker.setNewNumberOfFloors(0)

narrative("Ну и т.д.")
bunker.numberOfFloors = -5
bunker.numberOfFloors = 5
print(bunker)

narrative("\nНа этом всё...")
