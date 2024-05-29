# Напиши функцию get_multiplied_digits, которая принимает аргумент целое чиcло number
# и подсчитывает произведение цифр этого числа.
#
# Пункты задачи:
# 1. Напишите функцию get_multiplied_digits и параметр number в ней.
def get_multiplied_digits(number):
    # 2. Создайте переменную str_number и запишите строковое представление(str) числа number в неё.
    str_number = str(number)

    # 3. Основной задачей будет отделение первостоящей цифры в числе:
    #    создайте переменную first и запишите в неё первый символ из str_number в числовом представлении(int).
    first = str_number[0]

    # 4. Возвращайте значение first * get_multiplied_digits(int(str_number[1:])).
    #    Таким образом вы умножите первую цифру числа на результат работы этой же функции c числом,
    #    но уже без первой цифры.

    # 4 пункт можно выполнить только тогда, когда длина str_number больше 1,
    # т.к. в противном случае не получиться взять срез str_number[1:].
    if len(str_number) > 1:
        # Про отрицательные числа в ТЗ конечно ничего нет, но чем чёрт не шутит...
        if first == '-':
            first = '-1'
        # Рекурсия, если в числе более одной цифры.
        return int(first) * get_multiplied_digits(int(str_number[1:]))
    # Если же длина str_number не больше 1, тогда вернуть оставшуюся цифру first.
    return number

# Стек вызовов будет выглядеть следующим образом:
# get_multiplied_digits(40203) -> 4 * get_multiplied_digits(203) -> 4 * 2 * get_multiplied_digits(3) -> 4 * 2 * 3
print(get_multiplied_digits(0))
print(get_multiplied_digits(11))
print(get_multiplied_digits(+302))
print(get_multiplied_digits(40302))
print(get_multiplied_digits(-5040302))
