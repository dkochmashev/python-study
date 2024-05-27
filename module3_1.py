# Проверяет вхождение слов друг в друга
def are_single_root_words(word1, word2):
    comp_word1 = word1.lower()
    comp_word2 = word2.lower()
    return comp_word1.count(comp_word2) or comp_word2.count(comp_word1)

# Объявите функцию single_root_words и напишите в ней параметры root_world и *other_words.
def single_root_words(root_word, *other_words):    # В ТЗ было ни много ни мало - "root_world" !
    # Создайте внутри функции пустой список same_words, который пополнится нужными словами.
    same_words = list()
    # При помощи цикла for переберите предполагаемо подходящие слова.
    for word in other_words:
        # Пропишите корректное относительно задачи условие, при котором добавляются слова в результирующий список same_words.
        if are_single_root_words(root_word, word):
            same_words.append(word)
    # После цикла верните образованный функцией список same_words.
    return same_words

# Вызовите функцию single_root_words и выведете на экран(консоль) возвращённое ей занчение.
print(single_root_words('rich', 'richiest', 'orichalcum', 'cheers', 'richies'))
print(single_root_words('Disablement', 'Able', 'Mable', 'Disable', 'Bagel'))
