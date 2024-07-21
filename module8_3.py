# Класс Car должен обладать следующими свойствами:
# 1. Атрибут объекта model - название автомобиля (строка).
# 2. Атрибут объекта __vin - vin номер автомобиля (целое число).
#    Уровень доступа private.
# 3. Метод __is_valid_vin(vin_number) - принимает vin_number и проверяет его на корректность.
#    Возвращает True, если корректный, в других случаях выбрасывает исключение.
#    Уровень доступа private.
# 4. Атрибут __numbers - номера автомобиля (строка).
# 5. Метод __is_valid_numbers(numbers) - принимает numbers и проверяет его на корректность.
#    Возвращает True, если корректный, в других случаях выбрасывает исключение.
#    Уровень доступа private.
# 6. Классы исключений IncorrectVinNumber и IncorrectCarNumbers, объекты которых обладают
#    атрибутом message - сообщение, которое будет выводиться при выбрасывании исключения.

class InvalidCarDataException(BaseException):
    def __init__(self, message):
        super().__init__()
        self.message = message

### ТЗ требует создать отдельный класс для каждого вида ошибок в данных машины
IncorrectVinNumber = InvalidCarDataException
IncorrectCarNumbers = InvalidCarDataException

class Car:
    def __init__(self, model, vin, numbers):
        self.model = model
        ### Несмотря на то, что метод __is_valid_vin возвращает True при успешной проверка значения,
        ### необязательно использовать условие if self.__is_valid_vin(vin),
        ### т.к. при некорретном значении vin возникнет исключение и атрибут __vin не будет определен.
        self.__is_valid_vin(vin)
        self.__vin = vin
        ### Несмотря на то, что метод __is_valid_numbers возвращает True при успешной проверка значения,
        ### Необязательно использовать условие if self.__is_valid_numbers(numbers),
        ### т.к. при некорретном значении numbers возникнет исключение и атрибут __numbers не будет определен.
        self.__is_valid_numbers(numbers)
        self.__numbers = numbers

    # 1. Выбрасывает исключение IncorrectVinNumber с сообщением 'Некорректный тип vin номер',
    #    если передано не целое число. (тип данных можно проверить функцией isinstance).
    # 2. Выбрасывает исключение IncorrectVinNumber с сообщением 'Неверный диапазон для vin номера',
    #    если переданное число находится не в диапазоне от 1000000 до 9999999 включительно.
    # 3. Возвращает True, если исключения не были выброшены.
    def __is_valid_vin(self, vin):
        if not isinstance(vin, int):
            raise IncorrectVinNumber('Некорректный тип vin номер')
        if not 1000000 <= vin <= 9999999:
            raise IncorrectVinNumber('Неверный диапазон для vin номера')
        ### Непонятно зачем ТЗ требует что-то возвращать,
        ### если положительным результатом является сам факт отсутствии исключений...
        return True

    # 1. Выбрасывает исключение IncorrectCarNumbers с сообщением 'Некорректный тип данных для номеров',
    #    если передана не строка. (тип данных можно проверить функцией isinstance).
    # 2. Выбрасывает исключение IncorrectCarNumbers с сообщением 'Неверная длина номера',
    #    переданная строка должна состоять ровно из 6 символов.
    # 3. Возвращает True, если исключения не были выброшены.
    def __is_valid_numbers(self, numbers):
        if not isinstance(numbers, str):
            raise IncorrectCarNumbers('Некорректный тип данных для номеров')
        if len(numbers) != 6:
            raise IncorrectCarNumbers('Неверная длина номера')
        ### Непонятно зачем ТЗ требует что-то возвращать,
        ### если положительным результатом является сам факт отсутствии исключений...
        return True


try:
    first = Car('Model1', 1000000, 'f123dj')
except IncorrectVinNumber as exc:
    print(exc.message)
except IncorrectCarNumbers as exc:
    print(exc.message)
else:
    print(f'{first.model} успешно создан')

try:
    second = Car('Model2', 300, 'т001тр')
except IncorrectVinNumber as exc:
    print(exc.message)
except IncorrectCarNumbers as exc:
    print(exc.message)
else:
    print(f'{second.model} успешно создан')

try:
    third = Car('Model3', 2020202, 'нет номера')
except IncorrectVinNumber as exc:
    print(exc.message)
except IncorrectCarNumbers as exc:
    print(exc.message)
else:
    print(f'{third.model} успешно создан')
