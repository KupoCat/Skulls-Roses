from Player import Player,RandomPlayer
from itertools import cycle,dropwhile
class Game:
    WINNING_POINTS = 2
    def __init__(self,number_of_players,random_players=False):
        self.number_of_players = number_of_players
        player_class = RandomPlayer if random_players else Player
        self.players = [player_class(player_num=num) for num in range(1, number_of_players+1)]
        self.__players_cycle = cycle(self.players)
        self.current_player = self.players[0]
    
    def start_round(self,starting_player=None):
        for player in self.players:
            player.play_card()
        starting_player = starting_player if starting_player else self.players[0]
        self.__players_cycle = self.__cycle_starting_from(self.players,starting_player)
    
    def get_player(self, player_num: int)->Player:
        return next(player for player in self.players if player.player_num == player_num)
    
    def turn(self):
        return self.current_player.play()

    def next_player(self):
       return next(self.__players_cycle) 
    
    @staticmethod
    def __cycle_starting_from(seq, value):
        """Return a cycling iterator on seq starting from value"""
        return dropwhile(lambda x: x is not value, cycle(seq)) # https://stackoverflow.com/questions/8940737/cycle-through-list-starting-at-a-certain-element
        
    def get_winner(self):
        if len(self.players) == 1:
            return self.players[0]
        winners = [player for player in self.players if player.points >= Game.WINNING_POINTS]
        assert len(winners) <= 1
        return winners[0] if winners else None
    
    def round(self):
        current_bid = None
        while not current_bid:
            self.current_player = next(self.__players_cycle)
            current_bid = self.turn()
        final_bid, final_bidder = self.raise_round(highest_bet=current_bid, leading_player=self.current_player)
        self.reveal_round(final_bid, final_bidder)
        self.reset_round()
        return final_bidder
    
    def run(self):
        while not self.get_winner:
            self.round()

    def reset_round(self):
        #TODO: check and eliminate dead players
        for player in self.players:
            player.reset_round()

    
    def reveal_round(self, bid:int, bidder:Player):
        unrevealed_cards = {
            player.player_num: player.played_cards[:] for player in self.players} #Don't from player.played_cards because it mutates it and cards will be gone
        for _ in range(bid):
            revealed_player = bidder.pick_reveal()
            revealed_card = unrevealed_cards[revealed_player].pop() #TODO: stopped here
            if revealed_card.isSkull:
                is_random = revealed_player is bidder
                bidder.discard(is_random=is_random)
                break
        else: #break wasn't called
            bidder.award_point()

    def raise_round(self,highest_bet,leading_player):
        raising_players = self.players[:]
        raising_players_cycle = self.__cycle_starting_from(raising_players,leading_player)
        # next(raising_players_cycle) # Skip the leading player the first time
        while len(raising_players) > 1:
            current_raising_player = next(raising_players_cycle)
            new_bet = current_raising_player.raise_bet(highest_bet, self.played_cards)
            if new_bet == 0:
                raising_players.remove(current_raising_player)
            highest_bet = max(highest_bet,new_bet)
        return highest_bet, raising_players[0]
    
    @property
    def played_cards(self):
        return sum(len(player.played_cards) for player in self.players)
