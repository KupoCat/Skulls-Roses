from .Game import Game
from unittest import TestCase

MOCK_GAME_SIZE = 4
MOCK_PLAYED_CARDS = 5


class GameTest(TestCase):
    def setUp(self):
        self.game = Game(number_of_players=MOCK_GAME_SIZE, random_players=True)

    def test_init(self):
        self.assertEqual(self.game.number_of_players, MOCK_GAME_SIZE)

    def test_round(self):
        play = self.game.players[0].play()
        self.assertEqual(play, 0)

    def test_win_points(self):
        winner = self.game.get_winner()
        self.assertEqual(winner.points, 2)

    def test_win_last_man_standing(self):
        self.assertEqual(len(self.game.players), 0)
        self.assertEqual(self.game.number_of_players, 1)

    def test_eliminate_player(self):
        player_number = self.game.eliminate_player(0)
        self.assertEqual(player_number, 0)
        self.assertEqual(len(self.game.players), MOCK_GAME_SIZE - 1)
        self.assertEqual(self.game.number_of_players, MOCK_GAME_SIZE - 1)

    def test_successful_choice(self):
        ...

    def test_bet_failure(self):
        ...
    