FIRST_NUMBER_START = 3      # Начало интервала чисел из "первой вставки"
FIRST_NUMBER_END = 20       # Конец интервала чисел из "первой вставки"
TRY_NUMBER_START = 1        # Начало интервала чисел для подбора пароля (концом является first_number)

# Входная функция
def main():
    try:
        print(f'Пароль: {password_for(get_first_number())}')
    except IOError:
        print('Если не можете ввести правильное первое число, Вам кирдык!')

# Возвращает "пары чисел друг за другом, чтобы число из первой вставки было кратно сумме их значений."
def password_for(number):
    password = str()
    for try_number1 in range(TRY_NUMBER_START, number):
        for try_number2 in range(try_number1 + 1, number):
            if number % (try_number1 + try_number2) == 0:
                password += f'{try_number1}{try_number2}'
    return password

# Считывает с клавиатуры и возвращает число из "первой вставки"
# Число должно находиться в интервале FIRST_NUMBER_START <= число <= FIRST_NUMBER_END
def get_first_number():
    first_number = int(input('Первое число: '))
    if (FIRST_NUMBER_START <= first_number <= FIRST_NUMBER_END):
        return first_number
    raise IOError

# Вспомогательная функция для проверки работы password_for(number)
def print_all_passwords():
    for first_number in range(FIRST_NUMBER_START, FIRST_NUMBER_END):
        print(f'{first_number} - {password_for(first_number)}')

# Поехали!
main()
