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
class Player:
    def __init__(self, name):
        self.name = name
        self.guesses = []
        self.used_letters = {}

    def submit_guess(self, guess, colors):
        self.guesses.append((guess, colors))

        # track used letters
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
class Game:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.word_bank = WordChoice()
        self.secret_word = self.word_bank.random_word()
        self.max_guesses = 6
        self.attempts = 0
        self.current_guess = ""
        self.game_over = False

    def guess_checker(self, guess):
        if len(guess) != 5 or not guess.isalpha():
            return "Invalid guess"
        
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
            return

        colors = self.guess_checker(self.current_guess)
        self.player.submit_guess(self.current_guess, colors)
        self.attempts += 1

        if self.current_guess == self.secret_word or self.attempts >= self.max_guesses:
            self.game_over = True

        self.current_guess = ""

game = Game("Player")

#Draw
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

    if game.game_over:
        msg = "YOU WIN!" if game.player.guesses and game.player.guesses[-1][0] == game.secret_word else f"WORD: {game.secret_word}"
        text = SMALL_FONT.render(msg, True, WHITE)
        screen.blit(text, (150, 620))

    pygame.display.flip()


#Loop
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

pygame.quit()