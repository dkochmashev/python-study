from threading import Thread, Lock
from random import randint
from time import sleep

class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = Lock()

    def deposit(self):
        for i in range(100):
            delta = randint(50, 500)
            self.balance += delta
            print(f"Пополнение #{i}: {delta}. Баланс: {self.balance}")
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            sleep(0.001)

    def take(self):
        for i in range(100):
            delta = randint(50, 500)
            print(f"Запрос #{i} на {delta}")
            if self.balance >= delta:
                self.balance -= delta
                print(f"Снятие #{i}: {delta}. Баланс: {self.balance}")
            else:
                print(f"Запрос #{i} отклонён, недостаточно средств")
                self.lock.acquire()

bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = Thread(target=Bank.deposit, args=(bk,))
th2 = Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
