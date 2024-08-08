def all_variants(text):
    '''
    Генератор фрагметов переданной строки. Формирует фрагментв переданной строки длиной от 1
    до размера переданной строки, со смещением в 1 символ.
    Например, фрагменты для переданной строка 'abc' будут 'a','b','c','ab','bc','abc'.
    :param text: переданная строка
    :return: None
    '''
    for chunk_size in range(1, len(text) + 1):
        for start_pos in range(0, len(text) - chunk_size + 1):
            yield text[start_pos:start_pos + chunk_size]

a = all_variants("abc")
for i in a:
    print(i)
