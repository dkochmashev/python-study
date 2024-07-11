import re

# Запуск дополнительных тестов
# Если требуется проверка задания строго по ТЗ, установите значение в False
EXTRA_TESTS = True

# Напишите класс WordsFinder, объекты которого создаются следующим образом:
# WordsFinder('file1.txt, file2.txt', 'file3.txt', ...).
# Объект этого класса должен принимать при создании неограниченного количество
# названий файлов и записывать их в атрибут file_names в виде списка или кортежа.

class WordsFinder:
    def __init__(self, *file_names):
        self.__file_list = list()
        self.__file_index = dict()      # file_name : file_id
        self.__words_index = dict()     # search_string = {file1_id, file2_id, ...}
                                        # * search_string - строка поиска - исходное слово в нижнем регистре
        self.__file_words = dict()      # file_id = {search_string = [[pos1, original_word1], [pos2, original_word2], ...]
                                        # * original_word - исходный вид слова в файле (без преобразования к нижнему регистру для поиска)
        self.__create_file_index(*file_names)

    def __create_file_index(self, *file_names):
        for file_name in file_names:
            file_id = self.__read_file_words(file_name)
            # Если file_id имеет положительное значение, значит файл открыт и он не пустой
            if file_id:
                self.__file_list.append(file_name)
                self.__file_index[file_name] = file_id

    def __read_file_words(self, file_name):
        try:
            file = open(file_name, encoding='utf-8')
        except:
            pass
        else:
            with file:
                file_id = self.__get_next_file_id(file_name)
                # Нумерация позиций слов в файле начинается с 1
                file_word_pos = 1
                for word in filter(None, re.split(r'\W-\W|[ \t\r\n,.=!?;:]', file.read())):
                    # Строка поиска - это искомое слово в нижнем регистре
                    search_string = word.lower()

                    if search_string not in self.__words_index:
                        self.__words_index[search_string] = {file_id}
                    else:
                        self.__words_index[search_string].add(file_id)

                    if file_id not in self.__file_words:
                        self.__file_words[file_id] = dict()

                    if search_string not in self.__file_words[file_id]:
                        self.__file_words[file_id][search_string] = [[file_word_pos, word]]
                    else:
                        self.__file_words[file_id][search_string].append([file_word_pos, word])

                    file_word_pos += 1
                # Если файл не пустой, возвращаем file_id, иначе - 0
                return file_id if file_word_pos > 1 else 0

        # При ошибке открытия/чтения файла возвращаем 0
        return 0

    def __get_next_file_id(self, file_name):
        return len(self.__file_list) + 1

    def __get_file_id(self, file_name):
        return self.__file_index.get(file_name)

    def __get_file_name(self, file_id):
        return self.__file_list[file_id - 1] \
            if file_id >= 1 and len(self.__file_list) >= file_id \
            else None

    def __get_file_words(self, file_id, original_spelling = False):
        if file_id in self.__file_words:
            result = list()
            for search_string in self.__file_words[file_id]:
                file_word_positions = self.__file_words[file_id][search_string]
                for pos, original_word in file_word_positions:
                    result.append((pos, original_word if original_spelling else search_string))
        return [word for pos, word in sorted(result)]

    def __get_file_word_first_pos(self, file_id, word):
        search_string = word.lower()
        return self.__file_words.get(file_id).get(search_string)[0][0]

    def __get_file_word_count(self, file_id, word):
        search_string = word.lower()
        return len(self.__file_words.get(file_id).get(search_string))

    def __get_matched_files(self, word):
        search_string = word.lower()
        matched_files = self.__words_index.get(search_string)
        return (file_id for file_id in matched_files) if matched_files else ()

    def get_all_words(self, original_spelling = False):
        '''
        Возвращает все слова в файлах.
        :param original_spelling: установить в True, если нужно представить слова в оригинальном виде
        :return: словарь, где ключ - название файла, значение - список слов данного файла
        '''
        results = dict()
        for file_id in self.__file_words:
            results[self.__get_file_name(file_id)] = self.__get_file_words(file_id, original_spelling)
        return results

    def find(self, word):
        '''
        Возвращает первую позицию искомого слова в файлах.
        :param word: искомое слово
        :return: словарь, где ключ - название файла, значение - позиция первого такого слова в списке слов этого файла.
        '''
        results = dict()
        for file_id in self.__get_matched_files(word):
            results[self.__get_file_name(file_id)] = self.__get_file_word_first_pos(file_id, word)
        return results

    def count(self, word):
        '''
        Возвращает кол-во искомого слова в файлах.
        :param word: искомое слово
        :return: словарь, где ключ - название файла, значение - количество слова word в списке слов этого файла.
        '''
        results = dict()
        for file_id in self.__get_matched_files(word):
            results[self.__get_file_name(file_id)] = self.__get_file_word_count(file_id, word)
        return results


finder2 = WordsFinder('test_file.txt')
print(finder2.get_all_words()) # Все слова
print(finder2.find('TEXT')) # 3 слово по счёту
print(finder2.count('teXT')) # 4 слова teXT в тексте всего

if EXTRA_TESTS:
    print(finder2.get_all_words(True)) # Все слова в оригинальном виде
    finder3 = WordsFinder(
        '/Windows/System32/drivers/etc/КРАКОЗЯБРА',
        '/Windows/System32/drivers/etc/networks',
        '/Windows/System32/drivers/etc/hosts',
        '/Windows/System32/drivers/etc/protocol',
        '/Windows/System32/drivers/etc/services'
    )
    for search_word in ['trademark', 'Software', 'software', 'copyRIGHT', 'example', 'USE', 'localhost', 'tcp', 'http', 'pptp']:
        print(search_word, finder3.count(search_word))
