from Card import Card
import random


class Player:
    DEFAULT_HAND_SIZE = 4

    def __init__(self, player_num: int):
        self.player_num = player_num
        self.hand = list()
        for _ in range(Player.DEFAULT_HAND_SIZE - 1):
            self.hand.append(Card(isSkull=False))
        self.hand.append(Card(isSkull=True))
        self.played_cards = list()
        self.points = 0

    def has_skull(self):
        return any(card.isSkull for card in self.hand)

    def choose_card(self) -> int:
        return self.legal_input(range(0, len(self.hand)), 'Play card:', int)

    def decide_to_bet(self) -> bool:
        return self.legal_input("Do you want to bet? (Yes/No)", ['y', 'yes', 'Yes', 'n', 'No'], bool)

    def play_card(self):
        played_card = self.hand[self.choose_card()]  # TODO: export strings
        self.hand.remove(played_card)
        self.played_cards.append(played_card)
        return played_card

    def play(self, played_cards: int, is_random=False) -> int:
        if len(self.hand) == 0 or (is_random and bool(random.getrandbits(1))) or self.decide_to_bet():
            return self.bet(played_cards)
        else:
            self.play_card()
            return 0

    def bet(self, played_cards: int) -> int:
        return self.legal_input(range(1, played_cards), 'Choose bet', int)

    def discard(self):
        removed_index = self.choose_card()
        self.hand.pop(removed_index)

    def pick_reveal(self, num_of_players: int):
        while self.played_cards:
            return self.player_num
        return self.choose_player(num_of_players)

    def choose_player(self, num_of_players) -> int:
        legal_players = list(range(1, num_of_players))
        legal_players.remove(self.player_num)
        return self.legal_input(legal_players, 'Choose other player', int)

    def reset_round(self):
        while self.played_cards:
            self.hand.append(self.played_cards.pop())

    def legal_input(self, seq, msg, return_type):
        legal = False
        re = None
        while not legal:
            re = input(msg)
            legal = re in seq
        return return_type(re)

    def raise_bet(self, current_bet: int, played_cards: int):
        return self.legal_input(list(range(current_bet+1, played_cards)) + [0], 'Raise from 2?', int)

    def award_point(self):
        self.points += 1

class RandomPlayer(Player):
    def legal_input(self, seq, msg, return_type):
        return return_type(random.choice(seq))
