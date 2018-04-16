from .Game import Game
from unittest import TestCase

MOCK_GAME_SIZE = 4
class GameTest(TestCase):
    def setUp(self):
        self.game = Game(number_of_players=MOCK_GAME_SIZE)

    def test_init(self):
        self.assertEqual(self.game.number_of_players, MOCK_game_SIZE)

    def test_round(self):
        ...

    def test_win_points(self):
        winner = self.game.get_winner()
        self.assertEqual(winner.points, 2)

    def test_win_last_man_standing(self):
        winner = self.game

    def test_lose(self):
        ...
    def test_bet_successfull(self):
        ...
    
    def test_bet_failure(self):
        ...
    