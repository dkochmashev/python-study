import os
import time

# 1. Используйте os.walk для обхода каталога, путь к которому указывает переменная directory
for root, dirs, files in os.walk('.'):
    parent_dir = os.path.abspath(root)
    for file in files:
        # 2. Примените os.path.join для формирования полного пути к файлам.
        filepath = os.path.join(parent_dir, file)
        # 3. Используйте os.path.getmtime и модуль time для получения и отображения времени последнего изменения файла.
        filetime = os.path.getmtime(filepath)
        formatted_time = time.strftime("%d.%m.%Y %H:%M", time.localtime(filetime))
        # 4. Используйте os.path.getsize для получения размера файла.
        filesize = os.path.getsize(filepath)
        # 5. Используйте os.path.dirname для получения родительской директории файла.
        # Видимо тут по задумке должно быть так:
        #   parent_dir = os.path.dirname(filepath)
        # Только я не понял зачем делать это для каждого файла в одной и той же директории,
        # когда можно это сделать один раз перед циклом...
        print(f'Обнаружен файл: {file}, Путь: {filepath}, Размер: {filesize} байт, Время изменения: {formatted_time}, Родительская директория: {parent_dir}')
