# Функция, которая складывает 3 числа (sum_three)
def sum_three(*numbers):
    if len(*numbers) != 3:
        raise ValueError('Требуется три числа')
    return sum(*numbers)

# Функция декоратор (is_prime), которая распечатывает "Простое", если результат 1ой функции будет простым числом
# и "Составное" в противном случае.
def is_prime(func):
    def wrapper(*numbers):
        result = func(numbers)
        for divider in range(2, result):
            if not result % divider:
                return 'Составное'
        return 'Простое'
    return wrapper

sum_three = is_prime(sum_three)

# Пример:
result = sum_three(2, 3, 6)
print(result)
