
import random

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
        self.word_bank = Wordchoice()
        self.secret_word = self.word_bank.get_random_word()
        self.max_guesses = 6
        self.attempts = 0

    def start_game(self):
        print("Welcome", self.player.name)
        print("Guess 5-Letter Word!")
        print("You will have", self.max_guesses, "attempts.\n")

        while not self.gameover():
            guess = input("Enter guess: ").lower()

            if len(guess) != 5:
                print("Enter 5-Letter word only!\n")
                continue
            
            self.player.submit_guess(guess)
            self.attempts += 1

            if guess == self.secret_word:
                print("You Win!")
                return
            
            self.result(self.guess_checker(guess))
        
        print("Game Over! Word was:", self.secret_word)

    def guess_checker(self, guess):
        result = ""

        for i in range(5):
            if guess[i] == self.secret_word[i]:
                result += guess[i].upper()
            elif guess[i] in self.secret_word:
                result += guess[i]
            else:
                result += "_"
        
        return result
    
    def result(self, feedback):
        print("Result:", feedback)
        print("Past Guesses:", self.player.word_guesses())
        print()

    def gameover(self):
        return self.attempts >= self.max_guesses
    
name = input("Enter your name: ")
game = Game(name)
game.start_game()

