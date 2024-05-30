def calculate_structure_sum(data_structure):
    """
    Реализует универсальное решение ужасно умного "ученика урбана" для подсчёта суммы всех чисел и длин всех строк.
    :param data_structure:
    :return: число, представляющее условную сумму всех элементов структуры
    """

    # Вначале обрабатываем "неитерируемые" типы (int, float)
    # bool не указываем, т.к. он неявно преобразуется в int
    if isinstance(data_structure, int) \
        or isinstance(data_structure, float):
        return data_structure
    # str, согласно ТЗ, требует особого отношения
    elif isinstance(data_structure, str):
        return len(data_structure)

    sum = 0

    # Для dict суммой является (сумма для ключа + сумма для значения)
    if isinstance(data_structure, dict):
        for key, value in data_structure.items():
            sum += calculate_structure_sum(key) + calculate_structure_sum(value)
    # Остальные "итерируемые" типы обрабатываются одноообразно
    elif iter(data_structure):
        for item in data_structure:
            sum += calculate_structure_sum(item)

    return sum

# Проверочная структура
data_structure = [
    [1, 2, 3],
    {'a': 4, 'b': 5},
    (6, {'cube': 7, 'drum': 8}),
    "Hello",
    ((), [{(2, 'Urban', ('Urban2', 35))}]),
    range(8),
    frozenset({1, 2, 3}),
    bytes(range(1,2)),
    bytearray({65, 66, 67})
]

# Вывод результата проверки
print(calculate_structure_sum(data_structure))
