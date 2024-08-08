from pathlib import Path
from time import sleep
from datetime import datetime
from threading import Thread

FILE_NAME_TEMPLATE = 'example<N>.txt'
WORD_AMOUNTS = (10, 30, 200, 100)

def write_words(word_count, file_name):
    if not int(word_count):
        return
    with open(file_name, "w", encoding='utf-8') as file:
        for word_number in range(1, int(word_count) + 1):
            file.write(f'Какое-то слово № {word_number}\n')
            sleep(0.1)
        print(f'Завершилась запись в файл {file_name}')
    # Файлы выглядят как задано, время потратили, теперь можно и подчистить хвосты
    Path.unlink(file_name)

def dispatch(exec_type, args, file_name_suffix=1):
    time_start = datetime.now()
    thread_pool = []

    for word_count in args:
        file_name = FILE_NAME_TEMPLATE.replace('<N>', str(file_name_suffix))

        if exec_type == 'seq':
            # Последовательный запуск заданий
            write_words(word_count, file_name)
        elif exec_type == 'par':
            # Параллельный запуск заданий
            thread_instance = Thread(target=write_words, args=(word_count, file_name))
            thread_instance.start()
            thread_pool.append(thread_instance)
        file_name_suffix += 1

    # При последовательном запуске (seq) список thread_pool будет пустым
    for thread_instance in thread_pool:
        thread_instance.join()

    print(f'Работа потоков {datetime.now() - time_start}')


dispatch('seq', WORD_AMOUNTS)
dispatch('par', WORD_AMOUNTS, 5)
