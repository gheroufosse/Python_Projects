from json import load

def read_values_from_json(path,key):
    # Create a empty list and full it with the data of the .json file
    values = []
    with open(path) as p:
        data = load(p)
        for i in data[key]:
            values.append(i)

    return values


# words_list = read_values_from_json(
#     '/Users/gauthierheroufosse/Documents/Calculus/Python/OpenClassRoom/Python_projects/Hangman/word_list.json', 'words')
# print(words_list[4])

