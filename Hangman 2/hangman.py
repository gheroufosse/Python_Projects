# import os
# print(os.listdir())

from read_json_word_list import read_values_from_json
from get_valid_word import get_valid_word

def main():

    words_list = read_values_from_json('/Users/gauthierheroufosse/Documents/Calculus/Python/OpenClassRoom/Python_projects/Hangman/word_list.json', 'words')
    word_choose = get_valid_word(words_list)
    print(word_choose)


main()
