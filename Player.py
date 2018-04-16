from Card import Card
import random
class Player:
    DEFAULT_HAND_SIZE = 4

    def __init__(self, player_num: int):
        self.play_num = player_num
        self.hand = list()
        for _ in range(Player.DEFAULT_HAND_SIZE - 1):
            self.hand.append(Card(isSkull=False))
        self.hand.append(Card(isSkull=True))
        self.played_cards = list()
        
    def has_skull(self):
        return any(card.isSkull for card in self.hand)
    
    def player_input(self,msg_string):
        return input(msg_string)

    def play_card(self,isRandom=False):
        if isRandom:
            played_card = random.choice(self.hand)
        else:
            played_card = self.hand[self.player_input('Played card:')] #TODO: export strings
        self.hand.remove(played_card)
        self.played_cards.append(played_card)
        return played_card