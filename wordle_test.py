import unittest
from main import Game
from main import GREEN, YELLOW, GREY


class TestWordle(unittest.TestCase):

    def setUp(self):
        self.game = Game("Tester")
        self.game.secret_word = "apple"

    def test_correct_guess_all_green(self):
        result = self.game.guess_checker("apple")
        self.assertEqual(result, [GREEN, GREEN, GREEN, GREEN, GREEN])

    def test_invalid_guess_length(self):
        result = self.game.guess_checker("abc")
        self.assertEqual(result, "Invalid guess")

    def test_invalid_guess_non_alpha(self):
        result = self.game.guess_checker("ab12!")
        self.assertEqual(result, "Invalid guess")

    def test_some_yellow_letters(self):
        result = self.game.guess_checker("pleap")
        self.assertIn(YELLOW, result)

    def test_some_grey_letters(self):
        result = self.game.guess_checker("zzzzz")
        self.assertEqual(result, [GREY, GREY, GREY, GREY, GREY])

    def test_duplicate_letters(self):
        self.game.secret_word = "apple"
        result = self.game.guess_checker("ppppp")

        self.assertEqual(result.count(GREEN) + result.count(YELLOW), 2)


if __name__ == "__main__":
    unittest.main()