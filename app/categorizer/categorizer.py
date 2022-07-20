import re


def read_categories_config(filename):
    categories_f = open(filename, encoding="UTF-8")
    categories = []
    category = []
    currentCategory = ""

    for line in categories_f.readlines():
        if line == '\n':
            categories.append([currentCategory, category[:]])
            category.clear()
            continue

        line = line.replace('\n', '')
        if line.startswith(':'):
            currentCategory = line.replace(':', '')
            continue
        category.append(line)
    categories_f.close()
    return categories


custom_categories = read_categories_config("categorizer/Categories.cat")


def get_message_categories(message):
    message = str(message)
    out_categories = []
    for i in custom_categories:
        for j in i[1]:
            if re.search(j, message) is not None:
                out_categories.append(i[0])
                break
    return out_categories
