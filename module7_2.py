# Создайте функцию custom_write(file_name, strings), которая принимает аргументы
#    file_name - название файла для записи,
#    strings - список строк для записи.
# Функция должна:
# 1. Записывать в файл file_name все строки из списка strings, каждая на новой строке.
# 2. Возвращать словарь strings_positions, где ключом будет кортеж (<номер строки>, <байт начала строки>),
#    а значением - записываемая строка. Для получения номера байта начала строки используйте метод tell()
#    перед записью.
def custom_write(file_name, strings):
    result = dict()

    try:
        file = open(file_name, 'w', encoding = 'utf-8')
    except:
        return result

    for line_number, string in enumerate(strings):
        result[(line_number + 1, file.tell())] = string
        file.write(f'{string}\n')

    return result

info = [
    'Text for tell.',
    'Используйте кодировку utf-8.',
    'Because there are 2 languages!',
    'Спасибо!'
    ]

result = custom_write('test.txt', info)
for elem in result.items():
  print(elem)
