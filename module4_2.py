def test_function():
    def inner_function():
        print("Я в области видимости функции test_function")
    inner_function()

test_function()

try:
    inner_function()    # Сформирует исключение NameError с описанием "name 'inner_function' is not defined"
except Exception as e:
    print(type(e), e)
