import random
#Colors Code 
#Use these links to figure out how to use color
#https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124 & https://realpython.com/python-wordle-clone/#keep-track-of-previous-guesses-and-color-them


GREEN = "\033[92m"
YELLOW = "\033[93m"
GREY = "\033[90m"
RESET = "\033[0m"

#Player Class
class Player:
    def __init__(self, name):
        self.name = name
        self.guesses = []

    def submit_guess(self, guess):
        self.guesses.append(guess)
    
    def number_guesses(self):
        return len(self.guesses)
    
    def word_guesses(self):
        return self.guesses
    
#Wordbank Class
class Wordchoice:
    def __init__(self):
        self.words = ["apple", "grape", "green", "bread", "welch", "light", "house", "clean"]

    def get_random_word(self):
        return random.choice(self.words)
    
#Game Class
class Game:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.word_bank = WordChoice()
        self.secret_word = self.word_bank.random_word().lower()
        self.max_guesses = 6
        self.attempts = 0

    def start_game(self):
        print("Welcome", self.player.name)
        print("Guess 5-Letter Word!")
        print("You will have", self.max_guesses, "attempts.\n")

        while not self.gameover():
            guess = input("Enter guess: ").lower()

            self.player.submit_guess(guess)
            self.attempts += 1

            if guess ==self.secret_word:
                print("You Win!")
                return
            
            self.result(feedback)
        
        print("Game Over! Word was:", self.secret_word)

    def guess_checker(self, guess):
        result = ["_"] * 5
        secret = list(self.secret_word)

        if len(guess) != 5 or not guess.isalpha():
            return "Invalid Guess: guess must be a 5 letter word"
        
        for i in range(5):
            if guess[i] == secret[i]:
                result[i] = guess[i].upper()
                secret[i] = None
            
        for i in range(5):
            if guess[i] == self.secret_word[i]:
                result += guess[i].upper()
            elif guess[i] in self.secret_word:
                result += guess[i]
            else:
                result += "_"
        
        return "".join(result)
    
    def result(self, feedback):
        print("Result:", feedback)
        print("Past Guesses:", self.player.word_guesses())
        print()

    def gameover(self):
        return self.attempts >= self.max_guesses


class WordChoice():
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
        if word in self.word_list:
            self.word_list.remove(word)

    def check_word(self, word):
        return word in self.word_list

name = input("Enter your name: ")
game = Game(name)
game.start_game()
