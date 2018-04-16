from Game import Game
from unittest import TestCase

MOCK_GAME_SIZE = 4
class GameTest(TestCase):
    def setUp(self):
        self.Game = Game(number_of_players = 4)
    def test_init(self):
        ...
    def test_round(self):
        ...
    def test_win(self):
        ...
    def test_lose(self):
        ...
    def test_bet_successfull(self):
        ...
    
    def test_bet_failure(self):
        ...
    