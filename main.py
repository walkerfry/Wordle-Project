import pygame
import random

pygame.init()

#Screen
WIDTH, HEIGHT = 500, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle")

FONT = pygame.font.SysFont(None, 50)
SMALL_FONT = pygame.font.SysFont(None, 28)

GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
GREY = (58, 58, 60)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


#Player
#It stores all the guesses the player has made and keeps a record of which letters have already been used.
# When a guess is submitted, it saves the guess along with its colors and updates the used letters. 
#It also makes sure the best color is kept for each letter, so green overrides yellow and gray, and yellow overrides gray.
class Player:
    def __init__(self, name):
        self.name = name
        self.guesses = []
        self.used_letters = {}

    def submit_guess(self, guess, colors):
        self.guesses.append((guess, colors))

        for i in range(5):
            letter = guess[i]
            color = colors[i]

            if letter not in self.used_letters:
                self.used_letters[letter] = color
            else:
                if color == GREEN:
                    self.used_letters[letter] = GREEN
                elif color == YELLOW and self.used_letters[letter] != GREEN:
                    self.used_letters[letter] = YELLOW


#Word
class WordChoice:
    def __init__(self):
        with open("wordlist.txt") as f:
            self.word_list = f.read().splitlines()

    def random_word(self):
        return random.choice(self.word_list).lower()


#Game
#The guess_checker method compares your guess to the secret word and decides the colors for each letter—green for correct spot.
#Yellow for correct letter in the wrong spot, and gray if it’s not in the word. 
#The submit method takes your current guess, checks it, saves it, increases the number of attempts.
#Ends the game if you win or run out of tries.
class Game:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.word_bank = WordChoice()
        self.secret_word = self.word_bank.random_word()
        self.max_guesses = 6
        self.attempts = 0
        self.current_guess = ""
        self.game_over = False
        self.message = ""

    def guess_checker(self, guess):
        if len(guess) != 5 or not guess.isalpha():
            return None
        
        result = [GREY] * 5
        secret = list(self.secret_word)

        # GREEN
        for i in range(5):
            if guess[i] == secret[i]:
                result[i] = GREEN
                secret[i] = None

        # YELLOW
        for i in range(5):
            if result[i] == GREY and guess[i] in secret:
                result[i] = YELLOW
                secret[secret.index(guess[i])] = None

        return result

    def submit(self):
        if len(self.current_guess) != 5:
            self.message = "GUESS MUST BE A 5-LETTER WORD"
            return

        colors = self.guess_checker(self.current_guess)
        self.player.submit_guess(self.current_guess, colors)
        self.attempts += 1

        if self.current_guess == self.secret_word or self.attempts >= self.max_guesses:
            self.game_over = True

        self.current_guess = ""

game = Game("Player")

#Draw
#This function draws everything on the screen. 
# It clears the screen, shows the title, and draws the grid for the guesses. 
# It then fills in the boxes with the player’s past guesses and colors them based on correctness. 
# It also shows the current guess as you type and displays the letters you’ve already used at the bottom. 
# If the game is over, it shows a win message or the correct word. 
# It updates the screen.
def draw():
    screen.fill(BLACK)

    title = FONT.render("WORDLE", True, WHITE)
    screen.blit(title, (170, 10))

    for row in range(6):
        for col in range(5):
            x = col * 80 + 50
            y = row * 80 + 60
            pygame.draw.rect(screen, GREY, (x, y, 60, 60), 2)

    for row, (word, colors) in enumerate(game.player.guesses):
        for col in range(5):
            x = col * 80 + 50
            y = row * 80 + 60

            pygame.draw.rect(screen, colors[col], (x, y, 60, 60))
            letter = FONT.render(word[col].upper(), True, WHITE)
            screen.blit(letter, (x + 15, y + 10))

    for i, letter in enumerate(game.current_guess):
        x = i * 80 + 50
        y = len(game.player.guesses) * 80 + 60
        text = FONT.render(letter.upper(), True, WHITE)
        screen.blit(text, (x + 15, y + 10))

    x, y = 20, 580
    for letter, color in sorted(game.player.used_letters.items()):
        text = SMALL_FONT.render(letter.upper(), True, color)
        screen.blit(text, (x, y))
        x += 25

    if game.message:
        msg = SMALL_FONT.render(game.message, True, WHITE)
        rect = msg.get_rect(center=(WIDTH//2, 620))
        screen.blit(msg, rect)
        
    if game.game_over:
        msg = "YOU WIN!" if game.player.guesses and game.player.guesses[-1][0] == game.secret_word else f"WORD: {game.secret_word}"
        text = SMALL_FONT.render(msg, True, WHITE)
        screen.blit(text, (200, 620))

    pygame.display.flip()

#Loop
#This is the main loop that keeps the game running. 
#It keeps updating the screen and checks what the player is doing. 
#You can type letters to make a guess, use backspace to delete, and press enter to submit it.
running = True
while running:
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game.game_over:

            if event.key == pygame.K_BACKSPACE:
                game.current_guess = game.current_guess[:-1]

            elif event.key == pygame.K_RETURN:
                game.submit()

            else:
                if len(game.current_guess) < 5 and event.unicode.isalpha():
                    game.current_guess += event.unicode.lower()
                    game.message = ""

pygame.quit()

#AI Assist
#We used AI to help set up the screen and the draw function.
#It also helped us organize our code better into classes and clean up the structure. 

#Gitwork Flow
#We used the gitwork flow to make changes, mainly within the main.py file.
#Had challenges at time pulling the right branch into the main branch to remian stable
#Pulling helped us to make sure we were working on the most updated version of code
