from threading import Thread
from time import sleep

DEFAULT_ENEMIES = 100

class Knight(Thread):
    def __init__(self, name, power, enemies = DEFAULT_ENEMIES):
        super().__init__()
        self.name = str(name)
        self.power = int(power)
        self.enemies = enemies
        self.fighting_days = 0
        self.start()

    def __spell_fighting_days(self):
        # Сию летопись будем писать благородным языком!
        if self.fighting_days < 0:
            raise ValueError
        if self.fighting_days == 1:
            return f'{self.fighting_days} день'
        elif 2 <= self.fighting_days <= 4:
            return f'{self.fighting_days} дня'
        return f'{self.fighting_days} дней'

    def run(self):
        print(f"{self.name}, на нас напали!")
        while self.enemies:
            self.fight()
            print(f"{self.name} сражается {self.__spell_fighting_days()}..., осталось {self.enemies} воинов.")
        print(f"{self.name} одержал победу спустя {self.__spell_fighting_days()}!")

    def fight(self):
        sleep(1)
        self.fighting_days += 1
        self.enemies -= self.power
        if self.enemies < 0:
            # Если рыцарь перестарался...
            self.enemies = 0


first_knight = Knight('Sir Lancelot', 10)
second_knight = Knight("Sir Galahad", 20)

# Дождемся завершения великих дел...
while first_knight.is_alive() or second_knight.is_alive():
    sleep(0.1)

print("Все битвы закончились!")
