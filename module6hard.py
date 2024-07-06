# Запуск дополнительных тестов
# Если требуется проверка задания строго по ТЗ, установите значение в False
EXTRA_TESTS = False

import math
if EXTRA_TESTS:
    from pprint import pprint

class RGBColor:
    def __init__(self, r, g ,b):
        if  not 0 <= r <= 255 or \
            not 0 <= g <= 255 or \
            not 0 <= b <= 255:
            raise ValueError
        self.__rgb = [r, g, b]

    def __str__(self):
        return f'#{str().join(f"{cc:X}" for cc in self.__rgb)}'

    def get_rgb_values(self):
        return self.__rgb

class Figure:
    sides_count = 0
    _side_arg_count = 0

    def __init__(self, rgb, *sides, **kwargs):
        if not self.set_color(*rgb):
            # При некорретности заданного цвета, устанавливаем черный цвет
            self.set_color(0, 0, 0)
        self.set_sides(*sides)
        self.set_filled(kwargs['filled'] if 'filled' in kwargs else False)

    def is_filled(self):
        return self.__filled

    def set_filled(self, filled = True):
        if 'filled' not in self.__dict__ or self.filled != filled:
            self.__filled = filled
            # Инициируем все сопутствующие изменению заливки вычисления у потомков
            self._on_fill_update()

    def _is_valid_color(self, r, g, b):
        try:
            RGBColor(r, g, b)
        except:
            return False
        else:
            return True

    # Правильно было бы назвать _are_valid_sides...
    def _is_valid_sides(self, *sides):
        # Проверка, что кол-во переданных аргументов является необходимым и достаточным для определения фигуры
        if len(sides) != self._side_arg_count:
            return False
        # Длины сторон фигуры должны быть положительными целыми числами
        for side in sides:
            if not isinstance(side, int) or side <= 0:
                return False
        # Стороны фигуры заданы корректно
        return True

    def set_color(self, r, g, b):
        try:
            self.__color = RGBColor(r, g, b)
        except:
            # Невозможно установить заданный цвет фигуры
            return False
        # Инициируем все сопутствующие изменению цаета вычисления у потомков
        self._on_color_update()
        return True

    def get_color(self):
        return self.__color.get_rgb_values()

    def _on_color_update(self):
        pass

    def _on_fill_update(self):
        pass

    def _on_sides_update(self):
        pass

    def set_sides(self, *sides):
        if self._is_valid_sides(*sides):
            self.__sides = [*sides] * (self.sides_count // self._side_arg_count)
        elif not self.__sides:
            self.__sides = [1] * self.sides_count
        # Инициируем все сопутствующие изменению сторон вычисления у потомков
        self._on_sides_update()

    def get_sides(self):
        return self.__sides

    def get_side(self, side_index = 0):
        return self.__sides[side_index] if side_index < len(self.__sides) else None


class Figure2D(Figure):
    def __init__(self, rgb, *sides, **kwargs):
        super().__init__(rgb, *sides, **kwargs)
        self._calc_perimeter()

    def _calc_perimeter(self):
        self._perimeter = sum(self.get_sides())

    def get_perimeter(self):
        return self._perimeter

    def _on_sides_update(self):
        super()._on_sides_update()
        self._calc_square()

    def __len__(self):
        return self._perimeter


class Figure3D(Figure2D):
    def get_volume(self):
        return self._volume

    def _on_sides_update(self):
        super()._on_sides_update()
        self._calc_volume()


class Circle(Figure2D):
    sides_count = 1
    _side_arg_count = 1

    def _calc_radius(self):
        self._radius = self.get_side() / math.pi / 2

    def _calc_square(self):
        self._square = math.pi * self._radius ** 2

    def _on_sides_update(self):
        self._calc_perimeter()
        self._calc_radius()
        super()._on_sides_update()

    def get_radius(self):
        return self._radius

    def get_square(self):
        return self._square


class Triangle(Figure2D):
    sides_count = 3
    _side_arg_count = 3

    def _calc_square(self):
        p = self._perimeter / 2
        self._square = math.sqrt(
            p   * (p - self.get_side(0))
                * (p - self.get_side(1))
                * (p - self.get_side(2)))

    def __calc_height(self):
        self.__height = [(2 * self._square) / side for side in self.get_sides()]

    def _on_sides_update(self):
        self._calc_perimeter()
        super()._on_sides_update()
        self.__calc_height()

    def get_square(self):
        return self._square

    def get_height(self):
        return self.__height


class Cube(Figure3D):
    sides_count = 12
    _side_arg_count = 1

    def _calc_square(self):
        self._square = 6 * self.get_side() ** 2

    def _calc_volume(self):
        self._volume = self.get_side() ** 3

    def _on_sides_update(self):
        self._calc_perimeter()
        super()._on_sides_update()


class Sphere(Circle, Figure3D):
    def _calc_perimeter(self):
        self._perimeter = math.inf

    def _calc_square(self):
        self._square = 4 * math.pi * self.get_radius() ** 2

    def _calc_volume(self):
        self._volume = 4 / 3 * math.pi * self.get_radius() ** 3


if EXTRA_TESTS:
    triangle = Triangle((111,121,131), 3, 4 ,5)
    print(triangle)
    pprint(vars(triangle))

circle1 = Circle((200, 200, 100), 10) # (Цвет, стороны)
if EXTRA_TESTS:
    print(circle1)
    pprint(vars(circle1))

if EXTRA_TESTS:
    sphere = Sphere((201,102,233),10)
    print(sphere)
    pprint(vars(sphere))

cube1 = Cube((222, 35, 130), 6)
if EXTRA_TESTS:
    print(cube1)
    pprint(vars(cube1))

# Проверка на изменение цветов:
circle1.set_color(55, 66, 77) # Изменится
cube1.set_color(300, 70, 15) # Не изменится
print(circle1.get_color())
print(cube1.get_color())

# Проверка на изменение сторон:
cube1.set_sides(5, 3, 12, 4, 5) # Не изменится
circle1.set_sides(15) # Изменится
print(cube1.get_sides())
print(circle1.get_sides())

# Проверка периметра (круга), это и есть длина:
print(len(circle1))

# Проверка объёма (куба):
print(cube1.get_volume())
