def overwrite_file(filename, content, directory=''):
    if '.txt' not in filename:
        filename = filename + '.txt'

    filename = directory + filename

    text_file = open(filename, "w")
    text_file.write(content)
    text_file.close()


def unique_lines_as_list(text_string):
    seen = set()
    answer = []

    for line in text_string.splitlines():
        if (line not in seen) or '*' in line:
            seen.add(line)
            answer.append(line)

    return answer


def unique_lines_as_string(text_string):
    string = '\n'.join(unique_lines_as_list(text_string))
    return string


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def remove_dupl_pres_order(input_list):
    seen = set()
    seen_add = seen.add
    return [x for x in input_list if not (x in seen or seen_add(x))]
