# Запуск дополнительных тестов
# Если требуется проверка задания строго по ТЗ, установите значение в False
EXTRA_TESTS = False

class Product:
    def __init__(self, name, weight, category):
        # Атрибут name - название продукта (строка).
        self.name = str(name)
        # Атрибут weight - общий вес товара (дробное число) (5.4, 52.8 и т.п.).
        self.weight = float(weight)
        # Атрибут category - категория товара (строка).
        self.category = str(category)

    # Метод __str__, который возвращает строку в формате '<название>, <вес>, <категория>'.
    # Все данные в строке разделены запятой с пробелами.
    def __str__(self):
        return f'{self.name}, {self.weight}, {self.category}'

class Shop:
    # Инкапсулированный атрибут __file_name = 'products.txt'.
    __file_name = 'products.txt'

    def __init__(self):
        self.__products = dict()
        # На данном этапе в памяти нет объектов и содержимое файла еще неизвестно
        # Отмечаем, что они друг другу не соответствуют
        self.__sync_with_file = False
        self.__merge_with_file()

    def __merge_with_file(self):
        try:
            file = open(self.__file_name, 'r')
        except:
            return False

        for product_line in file.readlines():
            product = Product(*product_line.replace('\n', '').split(', '))
            # Добавляем объект из файла, предварительно отключая автосохранение содержимого в файл
            self.add(product, auto_write = False)
        file.close()

        # Указываем, что содержимое файла в памяти
        self.__sync_with_file = True
        return True

    def write_to_file(self):
        # Не пишем в файла, если его содержимое уже в памяти
        if self.__sync_with_file:
            return True

        try:
            file = open(self.__file_name, 'w')
        except:
            print('Невозможно сохранить данные в файл')
            return False

        for product_name, product in self.__products.items():
            file.write(f'{product}\n')
        file.close()

        # Указываем, что содержимое памяти соответствует содержимому файла
        self.__sync_with_file = True
        return True

    # Метод get_products(self), который считывает всю информацию из файла __file_name,
    # закрывает его и возвращает единую строку со всеми товарами из файла __file_name.
    def get_products(self):
        # Не читаем из файла, если его содержимое уже в памяти
        if not self.__sync_with_file:
            self.__merge_with_file()
        return '\n'.join(str(product) for product in self.__products.values())

    # Метод add(self, *products), который принимает неограниченное количество объектов
    # класса Product. Добавляет в файл __file_name каждый продукт из products, если его
    # ещё нет в файле (по названию). Если такой продукт уже есть, то не добавляет и
    # выводит строку 'Продукт <название> уже есть в магазине' .
    def add(self, *products, auto_write = True):
        for product in products:
            if product.name not in self.__products:
                self.__products[product.name] = product
            else:
                print(f'Продукт {product.name} уже есть в магазине')

        if auto_write:
            self.write_to_file()

s1 = Shop()
if EXTRA_TESTS:
    print(s1.get_products())
p1 = Product('Potato', 50.5, 'Vegetables')
p2 = Product('Spaghetti', 3.4, 'Groceries')
p3 = Product('Potato', 5.5, 'Vegetables')

print(p2) # __str__

s1.add(p1, p2, p3)

print(s1.get_products())
