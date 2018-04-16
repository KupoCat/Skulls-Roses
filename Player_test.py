import unittest
from Player import Player

DEFAULT_HAND_SIZE = Player.DEFAULT_HAND_SIZE


class PlayerTest(unittest.TestCase):
    MOCK_PLAYER_NUM = 1
    MOCK_BOARD_SIZE = 3  # Currently played cards
    MOCK_PLAYER_COUNT = 4 

    def setUp(self):
        self.player = Player(player_num=PlayerTest.MOCK_PLAYER_NUM)

    def test_player_num(self):
        self.player.player_num = PlayerTest.MOCK_PLAYER_NUM

    def test_starting_hand(self):
        self.assertEqual(len(self.player.hand), DEFAULT_HAND_SIZE)
        self.assertTrue(self.player.has_skull)

        def count_skulls(player):
            return len([card for card in self.player.hand if card.isSkull])
        self.assertEqual(count_skulls(self.player), 1,
                         msg="Player has more than one skull")
        self.assertEqual(len(self.player.played_cards), 0)

    def test_card_play(self):
        played_card = self.player.play_card(isRandom=True)
        self.assertEqual(len(self.player.hand), DEFAULT_HAND_SIZE - 1)
        self.assertEqual(len(self.player.played_cards), 1)
        self.assertEqual(self.player.played_cards[0], played_card)

    def test_play_all_cards(self):
        for _ in range(DEFAULT_HAND_SIZE):
            self.player.play_card(isRandom=True)
        self.assertRaises(IndexError, self.player.play_card, isRandom=True)
        self.assertEqual(len(self.player.played_cards), DEFAULT_HAND_SIZE)
        self.assertTrue(any(card.isSkull for card in self.player.played_cards))

    def test_bets(self):
        bet = self.player.play(
            played_cards=PlayerTest.MOCK_BOARD_SIZE, always_bet=True)
        self.assertTrue(bet > 0, """player didn't bet""")  # Did bet
        self.assertTrue(bet <= PlayerTest.MOCK_BOARD_SIZE,
                        "Player bet more than legal")
        self.assertEqual(len(self.player.played_cards),
                         DEFAULT_HAND_SIZE, 'betting player played ')

    def test_raise(self):
        mock_already_bet = 2
        player_raise = self.player.raise_bet(
            current_bet=mock_already_bet, always_raise=True)
        self.assertTrue(player_raise > mock_already_bet)

    def test_corner_bets(self):
        for _ in range(DEFAULT_HAND_SIZE):
            bet = self.player.play_card(isRandom=True)
        bet_samples = (self.player.play(isRandom=True)
                       for _ in range(DEFAULT_HAND_SIZE))  # Sampling for isRandom
        self.assertTrue(all(bet > 0 for bet in bet_samples),
                        'Handless player did not bet')

    def test_open_self(self):
        self.player.play_card(isRandom=True)
        player_opened = self.player.pick_reveal(isRandom=True)
        self.assertEqual(player_opened, self.player.player_num)

    def test_open_others(self):
        player_opened = self.player.pick_reveal(isRandom=True)
        self.assertTrue(
            player_opened != self.player_num and player_opened <= PlayerTest.MOCK_PLAYER_COUNT)
    
    def test_discard(self):
        self.player.discard(isRandom=True)
        self.assertEqual(len(self.player.hand),DEFAULT_HAND_SIZE - 1)
    
    def test_reset(self):
        for _ in range(DEFAULT_HAND_SIZE):
            self.player.play_card(isRandom=True)
        self.player.reset_round()
        self.test_starting_hand()

        

        