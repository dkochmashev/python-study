import builtins
import platform

# Создайте функцию custom_write(file_name, strings), которая принимает аргументы
#    file_name - название файла для записи,
#    strings - список строк для записи.
# Функция должна:
# 1. Записывать в файл file_name все строки из списка strings, каждая на новой строке.
# 2. Возвращать словарь strings_positions, где ключом будет кортеж (<номер строки>, <байт начала строки>),
#    а значением - записываемая строка. Для получения номера байта начала строки используйте метод tell()
#    перед записью.

class OSIndependentLineWriter:
    '''
    Класс для записи строк в файл с использованием CRLF для переноса строк
    независимо от используемой операционной системы.
    '''
    NEWLINE = '\n' if platform.system() == 'Windows' else '\r\n'

    def __init__(self, file_handle):
        self.__file_handle = file_handle

    def write(self, string):
        return self.__file_handle.write(f'{string}{self.NEWLINE}')

    def tell(self):
        return self.__file_handle.tell()

    def close(self):
        return self.__file_handle.close()

def open(*args, **kwargs):
    return OSIndependentLineWriter(builtins.open(*args, **kwargs))

def custom_write(file_name, strings):
    result = dict()

    try:
        file = open(file_name, 'w', encoding = 'utf-8')
    except:
        return result

    for line_number, string in enumerate(strings):
        result[(line_number + 1, file.tell())] = string
        file.write(string)
    file.close()

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
