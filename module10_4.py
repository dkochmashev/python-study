from time import sleep
from random import randint
from threading import Thread
from queue import Queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))


class Cafe:
    def __init__(self, *tables):
        self.tables = tables
        self.queue = Queue()

    def get_free_table(self):
        for table in self.tables:
            if table.guest is None:
                return table
        return None

    def guest_arrival(self, *guests):
        for guest in guests:
            if table := self.get_free_table():
                table.guest = guest
                print(f"{guest.name} сел(-а) за стол номер {table.number}")
                guest.start()
            else:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while True:
            for table in self.tables:
                guest = table.guest
                if guest:
                    if guest.is_alive():
                        continue
                    print(f"{guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None

                if self.queue.empty():
                    return

                guest = self.queue.get()
                table.guest = guest
                print(f"{guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
                guest.start()


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
