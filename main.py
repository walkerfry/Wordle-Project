
#Colors Code 
#Use these links to figure out how to use color
#https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124 & https://realpython.com/python-wordle-clone/#keep-track-of-previous-guesses-and-color-them

import random

# Colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
GREY = "\033[90m"
RESET = "\033[0m"


# Player Class
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


# Word Bank Class
class WordChoice:
    def __init__(self):
        self.word_list = self.load_words()

    def load_words(self):
        with open("wordlist.txt", "r") as file:
            return file.read().splitlines()

    def random_word(self):
        return random.choice(self.word_list).lower()


# Game Class
class Game:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.word_bank = WordChoice()
        self.secret_word = self.word_bank.random_word()
        self.max_guesses = 6
        self.attempts = 0

    def start_game(self):
        print("Welcome,", self.player.name)
        print("Guess the 5-letter word!")
        print("You have", self.max_guesses, "attempts.\n")

        while not self.gameover():
            guess = input("Enter guess: ").lower()

            feedback = self.guess_checker(guess)

            if feedback == "Invalid guess":
                print("Guess must be 5 letters.")
                continue

            self.player.submit_guess(guess)
            self.attempts += 1

            print(feedback)

            if guess == self.secret_word:
                print("You Win!")
                return

        print("Game Over! Word was:", self.secret_word)

    def guess_checker(self, guess):
        if len(guess) != 5:
            return "Invalid guess"

        result = [""] * 5
        secret = list(self.secret_word)

        # Green letters
        for i in range(5):
            if guess[i] == secret[i]:
                result[i] = GREEN + guess[i].upper() + RESET
                secret[i] = None

        # Yellow / Grey
        for i in range(5):
            if result[i] == "":
                if guess[i] in secret:
                    result[i] = YELLOW + guess[i].upper() + RESET
                    secret[secret.index(guess[i])] = None
                else:
                    result[i] = GREY + guess[i].upper() + RESET

        return " ".join(result)

    def gameover(self):
        return self.attempts >= self.max_guesses


# Run Game
name = input("Enter your name: ")
game = Game(name)
game.start_game()