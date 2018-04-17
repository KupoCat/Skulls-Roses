from Game import Game
from unittest import TestCase
from unittest.mock import MagicMock,call
from Card import Card
MOCK_GAME_SIZE = 4
MOCK_PLAYED_CARDS = 5


class GameTest(TestCase):
    def setUp(self):
        self.game = Game(number_of_players=MOCK_GAME_SIZE, random_players=True)
        self.game.start_round()

    def test_init(self):
        self.assertEqual(self.game.number_of_players, MOCK_GAME_SIZE)
        
    def test_start_round(self):
        self.assertListEqual([len(player.played_cards) for player in self.game.players], [1]*MOCK_GAME_SIZE)

    def test_turn(self):
        tested_player = self.game.current_player
        tested_player.play = MagicMock(return_value = 0)
        self.game.turn()
        tested_player.play.assert_called()
        # self.assertEqual(self.game.current_player, self.game.get_player(2)) # game.round() should keep track of who's turn it is
    
    def test_betting_round(self):
        tested_player = self.game.get_player(1)
        tested_player.play = MagicMock(return_value=2)
        self.game.raise_round = MagicMock(return_value=[0,0])
        self.game.reveal_round = MagicMock() # not tested
        self.game.round()
        self.game.raise_round.assert_called_with(highest_bet=2, leading_player=tested_player)
    
    def test_passing_raise_round(self):
        tested_player = self.game.get_player(1)
        passing_players = [player for player in self.game.players if player is not tested_player]
        for player in passing_players:
            player.raise_bet = MagicMock(return_value=0)
        self.game.raise_round(highest_bet=2,leading_player=tested_player)
        for player in passing_players:
            player.raise_bet.assert_called_with(current_bet=2)
    
    def test_raising_raise_round(self):
        starting_player = self.game.get_player(1)
        starting_bet = 1
        raising_player = self.game.get_player(2)
        raising_player.raise_bet = MagicMock(return_value=starting_bet+1)
        self.game.raise_round = MagicMock()
        self.game.raise_round(highest_bet=starting_bet,leading_player=starting_player)
        self.game.raise_round.assert_called_with(highest_bet=starting_bet+1, lead_player=raising_player)

    def test_round(self):
        self.game.turn = MagicMock()
        self.game.round()
        self.game.turn.assert_has_calls([call()]*4)

    def test_win_points(self):
        winning_player = self.game.get_player(1)
        winning_player.points = MagicMock(return_value=Game.WINNING_POINTS)
        winner = self.game.get_winner()
        self.assertEqual(winner.points, Game.WINNING_POINTS)

    def test_win_last_man_standing(self):
        self.assertEqual(len(self.game.players), 0)
        self.assertEqual(self.game.number_of_players, 1)

    def test_eliminate_player(self):
        self.game.eliminate_player(self.game.get_player(1))
        self.assertEqual(len(self.game.players), MOCK_GAME_SIZE - 1)
        self.assertEqual(self.game.number_of_players, MOCK_GAME_SIZE - 1)

    def test_reveal_rose(self):
        self.game.get_player(2).played_cards = MagicMock(return_value=[Card(isSkull=False)])
        revealing_player = self.game.get_player(1)
        revealing_player.choose_player = MagicMock(return_value=2)
        revealing_player.award_point = MagicMock()
        self.game.reset_round = MagicMock()
        self.game.reveal_round(revealing_player=revealing_player,bet=1)
        revealing_player.award_point.assert_called()
        self.game.reset_round.assert_called()

    def test_reveal_skull(self):
        self.game.get_player(2).played_cards = MagicMock(return_value=[Card(isSkull=True)])
        revealing_player = self.game.get_player(1)
        revealing_player.choose_player = MagicMock(return_value=2)
        revealing_player.remove_card = MagicMock()
        self.game.reveal_round(revealing_player=revealing_player,bet=1)
        revealing_player.remove_card.assert_called()

    def test_reset_round(self):
        for player in self.game.players:
            player.reset_round = MagicMock()
        self.game.reset_round()
        for player in self.game.players:
            player.reset_round.assert_called()