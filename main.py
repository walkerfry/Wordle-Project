import random

class Wordchoice():
    def __init__(self):
        self.word_list = self.load_words()

    def load_words(self):
        with open("wordlist.txt", "r") as file:
            words = file.read().splitlines()
        return words
    
    def random_word(self):
        return random.choice(self.word_list)
    
    def add_word(self, word):
        self.word_list.append(word)

    def remove_word(self, word):
        self.word_list.remove(word)

    def check_word(self, word):
        return word in self.word_list

Walker = Wordchoice()
print(Walker.random_word())