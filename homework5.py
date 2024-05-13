# Работа со списками:

# - Создайте переменную my_list и присвойте ей список из нескольких элементов, например, фруктов.
my_list = ['apple', 'pear', 'banana', 'kiwi']
# - Выведите на экран список my_list.
print("List:", my_list)
# - Выведите на экран первый и последний элементы списка my_list.
print("First element:", my_list[0])
print("Last element:", my_list[-1])
# - Выведите на экран подсписок my_list с третьего до пятого элементов.
print("Sublist:", my_list[2:4])
# - Измените значение третьего элемента списка my_list.
my_list[2] = 'melon'
# - Выведите на экран измененный список my_list.
print("Modified list:", my_list)

# Работа со словарями:

# - Создайте переменную my_dict и присвойте ей словарь с парами ключ-значение, например, переводами некоторых слов.
my_dict = { "air" : "воздух", "water" : "вода", "fire" : "огонь", "stone" : "камень" }
# - Выведите на экран словарь my_dict.
print("Dictionary:", my_dict)
# - Выведите на экран значение для заданного ключа в my_dict.
print("Translation:", my_dict["air"])
# - Измените значение для заданного ключа или добавьте новый в my_dict.
my_dict.update({ "fire" : "пожар", "ground" : "земля" })
# - Выведите на экран измененный словарь my_dict.
print("Modified dictionary:", my_dict)
