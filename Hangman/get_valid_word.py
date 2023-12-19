from random import choice

def get_valid_word(words):

    word = choice(words)
    while '_' or ' ' or '-' in word:
        word = choice(words)

    return word.upper()

