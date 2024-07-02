class Vehicle:
    __COLOR_VARIANTS = { 'red', 'green', 'blue', 'yellow', 'black', 'white' }

    def __init__(self, owner, model, color, engine_power):
        self.owner = str(owner)
        self.__model = str(model)
        self.__engine_power = int(engine_power)
        self.set_color(color)

    def get_owner(self):
        return f'Владелец: {self.owner}'

    # Возвращает строку: "Модель: <название модели транспорта>"
    def get_model(self):
        return f'Модель: {self.__model}'

    # Возвращает строку: "Мощность двигателя: <мощность>"
    def get_horsepower(self):
        return f'Мощность двигателя: {self.__engine_power}'

    # Возвращает строку: "Цвет: <цвет транспорта>"
    def get_color(self):
        return f'Цвет: {self.__color}'

    # Распечатывает результаты методов (в том же порядке):
    # get_model()\n
    # get_horsepower()\n
    # get_color()\n
    # get_owner()\n
    def print_info(self):
        print(self.get_model(), self.get_horsepower(), self.get_color(), self.get_owner(), sep='\n')

    # Принимает аргумент new_color(str),
    # меняет цвет __color на new_color, если он есть в списке __COLOR_VARIANTS,
    # в противном случае выводит на экран надпись: "Нельзя сменить цвет на <новый цвет>".
    def set_color(self, new_color):
        new_color_str = str(new_color).lower()
        if new_color_str in self.__COLOR_VARIANTS:
            self.__color = new_color_str
        else:
            print(f'Нельзя сменить цвет на {new_color}')

class Sedan(Vehicle):
    __PASSENGERS_LIMIT = 5


# Текущие цвета __COLOR_VARIANTS = {'red', 'green', 'blue', 'yellow', 'black', 'white'}
vehicle1 = Sedan('Fedos', 'Toyota Mark II', 'blue', 500)

# Изначальные свойства
vehicle1.print_info()

# Меняем свойства (в т.ч. вызывая методы)
vehicle1.set_color('Pink')
vehicle1.set_color('BLACK')
vehicle1.owner = 'Vasyok'

# Проверяем что поменялось
vehicle1.print_info()
