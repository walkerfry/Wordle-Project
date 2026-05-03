import pgzrun
import random

WIDTH = 500
HEIGHT = 800

GREEN = (106, 170, 100)
YELLOW = (201, 180, 88)
GREY = (120, 124, 126)
WHITE = (255, 255, 255)

class Player:
    def __init__(self, name):
        self.name = name
        self.guesses = []

    def submit_guess(self, colored_guess):
        self.guesses.append(colored_guess)

    def number_guesses(self):
        return len(self.guesses)

    def word_guesses(self):
        return self.guesses

class WordChoice:
    def __init__(self):
        self.word_list = self.load_words()

    def load_words(self):
        with open("wordlist.txt", "r") as file:
            return file.read().splitlines()

    def random_word(self):
        return random.choice(self.word_list).upper()

class Game:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.word_bank = WordChoice()
        self.secret_word = self.word_bank.random_word()
        self.max_guesses = 6
        self.attempts = 0
        self.message = ""
        self.correct_guess = False
    
    def guess_checker(self, guess):
        if len(guess) != 5 or not guess.isalpha():
            return None
        
        result = [None] * 5
        secret = list(self.secret_word)

        # Green letters
        for i in range(5):
            if guess[i] == secret[i]:
                result[i] = (guess[i].upper(), GREEN)
                secret[i] = None

        # Yellow / Grey
        for i in range(5):
            if result[i] is None:
                if guess[i] in secret:
                    result[i] = (guess[i].upper(), YELLOW)
                    secret[secret.index(guess[i])] = None
                else:
                    result[i] = (guess[i].upper(), GREY)

        return result

    def gameover(self):
        return self.attempts >= self.max_guesses or self.correct_guess
    
    def restart(self):
        global game, current_guess
        game = Game("Player")
        current_guess = ""
def draw(): #ai assistance for some visuals
    screen.clear()
    screen.draw.text("WORDLE", center=(WIDTH // 2, 25),  fontsize=40)

    for row in range(6):
        for col in range(5):
            x = col * 85 + 50
            y = row * 85 + 50
            screen.draw.rect(Rect((x, y), (60, 60)), GREY)

    for row, guess in enumerate(game.player.guesses): #assistance
            for col, (letter, color) in enumerate(guess):
                x = col * 85 + 50
                y = row * 85 + 50
                screen.draw.filled_rect(Rect((x, y), (60, 60)), color)
                screen.draw.text(letter, (x+20, y+15), fontsize=40, color="white")

        # Draw current guess
    if not game.gameover():
        for col, letter in enumerate(current_guess): #assistance
            x = col * 85 + 50
            y = len(game.player.guesses) * 85 + 50

            screen.draw.text(letter, (x+20, y+15), fontsize=40, color="white")
    if game.gameover():
        screen.draw.text("Press (R) to play again or (ESC) to exit", center=(WIDTH // 2, 650),  fontsize=30)
    if game.message:
        screen.draw.text(game.message, center=(WIDTH // 2, 600),  fontsize=35)

current_guess = ""
game = Game("Player")

def on_key_down(key):
    global current_guess

    if key == keys.ESCAPE:
        exit()

    if key == keys.R and game.gameover():
            game.restart()
            return
    
    if not game.gameover():
        if key == keys.BACKSPACE:
            current_guess = current_guess[:-1]

        elif key == keys.RETURN:
            if len(current_guess) == 5 and not game.gameover():
                feedback = game.guess_checker(current_guess)

                if feedback is None:
                    game.message = ("Guess must be 5 letters.")
                    return

                game.player.submit_guess(feedback)
                game.attempts += 1

                if current_guess == game.secret_word:
                    game.correct_guess = True
                    game.message = (f"You Win! {game.secret_word} guessed in {game.attempts} attempts")
                elif game.attempts >= game.max_guesses:
                    game.message = (f"Game Over! The word was {game.secret_word}")
                             
                current_guess = ""

        else:
            if len(current_guess) < 5:
                letter = key.name
                if len(letter) == 1 and letter.isalpha():
                    current_guess += letter.upper()
    
pgzrun.go()
