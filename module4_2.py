# Создайте новую функцию def test_function
def test_function():
    # Создайте другую функцию внутри функции inner_function,
    # функция должна печатать значение "Я в области видимости функции test_function"
    def inner_function():
        print("Я в области видимости функции test_function")
    inner_function()

test_function()

try:
    # Попробуйте вызывать inner_function вне функции test_function
    # и посмотрите на результат выполнения программы
    inner_function()    # Сформирует исключение NameError с описанием "name 'inner_function' is not defined"
except Exception as e:
    print(type(e), e)
