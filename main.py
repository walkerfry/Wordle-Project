
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.guesses = 6

    def submit_guess(self, guess):
        self.guesses.append(guess)
    
    def number_guesses(self):
        return len(self.guesses)
    
    def word_guesses(self):
        return self.guesses
    

class Game:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.word_bank = Wordchoice()
        self.secret_word = self.word_bank.get_random_word()
        self.max_guesses = 6
        self.attempts = 0

    def start_game(self):
        print("Welcome", self.player.name)

        while not self.gameover():
            guess = input("Enter guess: ").lower()

            self.player.submit_guess(guess)
            self.attempts += 1

            if guess ==self.secret_word:
                print("You Win!")
                return
            
            self.result(self.guess_checker(guess))
        
        print("Game Over! Word was:", self.secret_word[i])

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

    def gameover(self):
        return self.attempts >= self.max_guesses
    
name = input("Enter your name: ")
game = Game(name)
game.start_game()

