# Пункты задачи:

# Класс House
class House:
    # Внутри класса House определите метод __init__,
    # в который передадите название и кол-во этажей.
    def __init__(self, name, number_of_floors):
        # Внутри метода __init__ создайте атрибуты объекта self.name и self.number_of_floors,
        # присвойте им переданные значения.
        self.name = name
        self.number_of_floors = self._validate_floor_value(number_of_floors)
        if not self.number_of_floors:
            raise ValueError

    def _validate_floor_value(self, floor):
        # Номер этажа или число этажей должны быть целым положительным числом
        if isinstance(floor, int) and floor > 0:
            return floor
        return 0

    def _floor_exists(self, floor):
        floor = self._validate_floor_value(floor)
        # Указанный этаж должен быть в интервале 1 <= этаж <= число этажей в доме
        if 1 <= floor <= self.number_of_floors:
            return True
        # Если же new_floor больше чем self.number_of_floors или меньше 1
        return False

    # new_floor - номер этажа(int), на который нужно приехать
    def go_to(self, new_floor):
        if not self._floor_exists(new_floor):
            print("Такого этажа не существует")
            return
        # Выводим список этаже с 1 по new_floor включительно
        for i in range(1, new_floor + 1):
            print(i)

# Создайте объект класса House с произвольным названием и количеством этажей.
h1 = House('ЖК Горский', 18)
h2 = House('Домик в деревне', 2)
h1.go_to(5)
h2.go_to(10)
