import multiprocessing
from datetime import datetime

def read_info(name):
    all_data = []
    with open(name) as file:
        all_data.extend(file.readlines())

filenames = [f'./module10_5/file {number}.txt' for number in range(1, 5)]

# Линейный вызов
# start_time = datetime.now()
# for name in filenames:
#     read_info(name)
# print(datetime.now() - start_time, '(линейный)')
# 0:00:04.245662 (линейный)

# Многопроцессный
if __name__ == '__main__':
    with multiprocessing.Pool(processes=8) as pool:
        start_time = datetime.now()
        pool.map(read_info, filenames)
        print(datetime.now() - start_time, '(многопроцессный)')
# 0:00:02.165934 (многопроцессный)
