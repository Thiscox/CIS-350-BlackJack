from card import Card
from deck import Deck

class Hand:
    def __init__(self):
        self.current_hand = []
        self.total_hand_value = 0

    def draw_card(self, card):

        # Adds the given card to the hand and calculates the now total of the hand

        self.current_hand.append(card)
        if card.get_blackjack_value() == 11 and self.total_hand_value+11 > 21:
            self.total_hand_value += 1
        else:
            self.total_hand_value += card.get_blackjack_value()

    def reset_hand(self):
        self.current_hand = []
        self.total_hand_value = 0

    def get_hand_value(self):
        return self.total_hand_value
    
    def is_blackjack(self):
        return (self.total_hand_value == 21)
    
    def is_bust(self):
        return (self.total_hand_value > 21)
            