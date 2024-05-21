# -*- coding: utf-8 -*-

# соглашения о стиле кода
# PEP8 (Python Enhancement Proposal 8) - описан "правильный" стиль программирования в пайтон
# https://www.python.org/dev/peps/pep-0008/

# 4 пробела на каждый уровень отступа

# lowercase (слово в нижнем регистре)
# lower_case_with_underscores (слова из маленьких букв с подчеркиваниями)
# UPPERCASE (заглавные буквы)
# UPPERCASE_WITH_UNDERSCORES (слова из заглавных букв с подчеркиваниями)

# CapitalizedWords (слова с заглавными буквами, или CapWords, или CamelCase).
#   Замечание: когда вы используете аббревиатуры в таком стиле, пишите все буквы аббревиатуры заглавными —
#   HTTPServerError лучше, чем HttpServerError.

# mixedCase (отличается от CapitalizedWords тем, что первое слово начинается с маленькой буквы)
# Capitalized_Words_With_Underscores (слова с заглавными буквами и подчеркиваниями — уродливо!)

# блоки кода

x, y = 10, 29

if x < 0:
    print('Х меньше нуля')
    # https://peps.python.org/pep-0008/#other-recommendations:
    # "...Use your own judgment..."
    # Ставить или нет пробелы вокруг оператора возведения в степень (**) оставлен на усмотрение программиста.
    # Я решил не ставить.
    z = x**2 + y
else:
    print('Х больше нуля')
    z = x - y

print('Результат', z)

# ср. с С++

# Я конечно понимаю, что в некоторых ситуациях Python выглядит лаконичней, чем C/C++
# Но зачем в примере столько ошибок? Причем, в одной скомканной строке кода!
# Создается впечатление, что тут кто-то не любит (или просто не знает) C/C++ ...

# Во-первых, это обычный C, а не C++ (видно по использованию printf, а не cout)
# Во-вторых, в C/C++ нет оператора возведения в степень. Зато есть функции pow, powf, powl из стандартной библиотеки math.
# В-третьих, для определения строковой константы используются кавычки ("), а не апострофы (')
# В-четвертых, использование printf для вывода значения переменной выглядит иначе (см.ниже)
#                                         -> !! <-                    !             !                       !            !
# if (x < 0) { printf('Меньше нуля\n'); z = x**2 + y; } else { printf('Больше нуля\n'); z = x - y; } printf('Получается\n', z)

# Эквивалентно работающий пример (собирать с опцией -lm):

# #include <stdio.h>
# #include <math.h>
#
# int main()
# {
#     float x = 10, y = 29, z;
#
#     if (x < 0) {
#         printf("x меньше нуля\n");
#         z = powf(x, 2) + y;
#     } else {
#         printf("x больше нуля\n");
#         z = x - y;
#     }
#     printf("Результат %f\n", z);
#
#     return 0;
# }

# вложенные блоки кода

name = input('Enter your name >>>')
if name == 'Ola':
    opponent = 'Ola'
    print('Hi, Ola!')
else:
    if name == 'Sofi':
        opponent = 'Sofi'
        print('Hi, Sofi!')
    else:
        if name == 'Katy':
            opponent = 'Katy'
            print('Hi, Katy!')
        else:
            opponent = 'anonymous'
            print('Hi, anonymous!')

if x < 0:
    if y > 0:
        z = -x + y
    else:
        z = -x - y
else:
    z = x + y

# оператор pass

if x < 0:
    if y > 0:
        pass
    else:
        print('направо!')
else:
    print('стой!')

# Максимальная длина строки

my_poem = ['Варкалось, хливкие шорьки пырялись по наве',
           'И хрюкотали зелюки как мюмзики в мове',
           'О бойся Бармаглота, сын! Он так свирлеп и дик',
           'А в глуше рымит исполин - Злопастный Брандашмыг!', ]

# пробелы в операторах

x = 2
y = x * x + 1
is_big = x >= 3000

x = my_poem[-1]
print(x)

my_list = [2, 3, 4, 5, 6, ]

# reformat кода

x, y = 3, 8

if x == 3:
    print(42)

if x < 0:
    if y > 0:
        print('налево!')
    else:
        print('направо!')
else:
    print('стой!')

# названия переменных

count_of_my_pets = 34
if count_of_my_pets > 10:
    print('I need more space for my pets!')

my_favorite_pets_and_bird = ['cat', 'wolf', 'ostrich']
if 'lion' in my_favorite_pets_and_bird:
    print('Wow!')

# Заменил название списка в горбатом стиле (MyFavoritePetsAndBirds), чтобы не путать с названиями классов
my_favorite_pets_and_birds = ['cat', 'wolf', 'ostrich']

# рекомендации PEP8

# b (одиночная маленькая буква)
# B (одиночная заглавная буква)
# но лучше использовать только такие однобуквенные имена
#   i j k - для циклов
#   x y z - для координат

# никогда не используйте в названиях переменных одиночные l, I, O  !
lowercase_l = 34  # Заменил одиночную l на читаемое название
L = 43

if lowercase_l > L:
    print()

UPPERCASE_O = 9  # Заменил одиночную O на читаемое название полностью в верхнем регистре, т.к. возможно это именованная "константа"

if UPPERCASE_O > 0:
    print()

# автоматическое переименование в PyCharm и подсказки - вам не нужно набирать длинные названия переменных

ss = ['cat', 'wolf', 'ostrich']
if 'lion' in ss:
    print('Wow!')

# В каждой уважающей себя компании есть style guide (стайл-гайд) - руководство по стилю написания кода.
# Практически все они основываются на PEP8, с небольшими исключениями, принятыми в этой команде.
# Как пример стайл-гайда небольшой компании рекомендую почитать
# https://github.com/best-doctor/guides/blob/master/guides/python_styleguide.md
