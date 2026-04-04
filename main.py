import random

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
    

class Game:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.word_bank = WordChoice()
        self.secret_word = self.word_bank.random_word().lower()
        self.max_guesses = 6
        self.attempts = 0

    def start_game(self):
        print("Welcome", self.player.name)

        while not self.gameover():
            guess = input(f"Enter guess ({self.attempts+1}/6): ").lower()

            feedback = self.guess_checker(guess)

            if "Invalid" in feedback:
                print(feedback)
                continue

            self.player.submit_guess(guess)
            self.attempts += 1

            if guess == self.secret_word:
                print(f"You Win! {self.secret_word} guessed in {self.attempts} attempts")
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
            if result[i] == "_" and guess[i] in secret:
                result[i] = guess[i]
                secret[secret.index(guess[i])] = None
        
        return "".join(result)
    
    def result(self, feedback):
        print("Result:", feedback)

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
