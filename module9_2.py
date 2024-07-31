first_strings = ['Elon', 'Musk', 'Programmer', 'Monitors', 'Variable']
second_strings = ['Task', 'Git', 'Comprehension', 'Java', 'Computer', 'Assembler']

first_result = [len(item) for item in first_strings if len(item) >= 5]
second_result = [
    (first_item, second_item) \
        for first_item in first_strings \
            for second_item in second_strings \
                if len(first_item) == len(second_item)
]
third_result = {
    item: len(item) \
        for item in first_strings + second_strings \
            if not len(item) % 2
}

print(first_result)
print(second_result)
print(third_result)
