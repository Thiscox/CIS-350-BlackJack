from blackjack import BlackjackGame
from player import Player
from deck import Deck
from card import Card
from display import Display
from button import Button
from hand import Hand
import pygame
import unittest


class PlayerTests(unittest.TestCase):
    def test_player_init_person(self):
        p = Player(True)
        self.assertEqual(p.is_person, True)

    def test_player_init_dealer(self):
        p = Player(False)
        self.assertEqual(p.is_person, False)

    def test_hit_bad_input(self):
        p = Player(True)
        p.hit("hello")
        self.assertEqual(len(p.hand.current_hand), 0)
    
    def test_hit_good_input(self):
        p = Player(True)
        c = Card("spades", "9")
        p.hit(c)
        self.assertEqual(len(p.hand.current_hand), 1)

    def test_stand(self):
        p = Player(True)
        p.stand()
        self.assertEqual(p.is_standing, True)

    def test_hand_no_cards(self):
        p = Player(True)
        ph = p.get_hand()
        self.assertEqual(len(ph.current_hand), 0)

    def test_hand_has_cards(self):
        p = Player(True)
        c_1 = Card("clubs", "7")
        c_2 = Card("hearts", "2")
        p.hit(c_1)
        p.hit(c_2)
        ph = p.get_hand()
        self.assertEqual(len(ph.current_hand), 2)


class DeckTests(unittest.TestCase):
    def test_deck_init(self):
        d = Deck()
        self.assertEqual(len(d.current_deck), 52)

    def test_reset_deck(self):
        d = Deck()
        d.deal_card()
        d.deal_card()
        d.reset_deck()
        self.assertEqual(len(d.current_deck), 52)

    def deal_card(self):
        d = Deck()
        self.assertEqual(type(d.deal_card), type(Card))

class CardTests(unittest.TestCase):
    def test_card_init(self):
        c = Card("spades", "9")
        self.assertEqual(c.suit, "spades")
        self.assertEqual(c.rank, "9")
        self.assertEqual(c.blackjack_val, 9)

    def test_get_blackjack_value(self):
        c = Card("spades", "9")
        self.assertEqual(c.get_blackjack_value(), 9)

    def test_str_method(self):
        c = Card("spades", "9")
        self.assertEqual(str(c), "9 of spades")
        

class DisplayTests(unittest.TestCase):
    def test_display_init(self):
        d = Display(1200, 700)
        self.assertEqual(d.screen.get_size(), (1200, 700))
        

    def test_reset_screen(self):
        d = Display(1200, 700)
        d.reset_screen()
        self.assertEqual(type(d.screen), pygame.surface.Surface)


class ButtonTests(unittest.TestCase):
    def test_button_init(self):
        d = Display(1200, 700)
        b = Button("hello", 20, 20, 20, 20, d)
        self.assertEqual("hello", b.text)

class HandTests(unittest.TestCase):
    def test_hand_init(self):
        h = Hand()
        self.assertEqual(len(h.current_hand), 0)
        self.assertEqual(h.total_hand_value, 0)

    def test_hand_draw(self):
        h = Hand()
        c = Card("spades", "ace")
        h.draw_card(c)
        self.assertEqual(len(h.current_hand), 1)
    
    def test_hand_reset(self):
        h = Hand()
        c = Card("spades", "ace")
        h.draw_card(c)
        h.reset_hand()
        self.assertEqual(len(h.current_hand), 0)

    def test_hand_value(self):
        h = Hand()
        c = Card("spades", "ace")
        h.draw_card(c)
        self.assertEqual(h.get_hand_value(), 11)

    def test_false_blackjack(self):
        h = Hand()
        c = Card("spades", "ace")
        h.draw_card(c)
        self.assertEqual(h.is_blackjack(), False)

    def test_true_blackjack(self):
        h = Hand()
        c = Card("spades", "ace")
        h.draw_card(c)
        c_1 = Card("spades", "10")
        h.draw_card(c_1)
        self.assertEqual(h.is_blackjack(), True)

    def test_false_bust(self):
        h = Hand()
        c = Card("spades", "ace")
        h.draw_card(c)
        c_1 = Card("spades", "10")
        h.draw_card(c_1)
        self.assertEqual(h.is_bust(), False)

    def test_true_bust(self):
        h = Hand()
        c = Card("spades", "ace")
        h.draw_card(c)
        c_1 = Card("spades", "10")
        h.draw_card(c_1)
        c_2 = Card("clubs", "3")
        h.draw_card(c_2)
        self.assertEqual(h.is_bust(), True)

class BlackJackTests(unittest.TestCase):
    def test_blackjack_init(self):
        b = BlackjackGame()
        self.assertEqual(type(b.deck), Deck)
        self.assertEqual(type(b.player), Player)
        self.assertEqual(type(b.dealer), Player)

    def test_blackjack_start(self):
        b = BlackjackGame()
        self.assertEqual(len(b.player.hand.current_hand), 2)
        self.assertEqual(len(b.dealer.hand.current_hand), 2)

    def test_blackjack_score_round_player_win(self):
        b = BlackjackGame()
        d = Display(1200, 700)
        b.player.hand.draw_card(Card("spades", "ace"))
        b.player.hand.draw_card(Card("hearts", "10"))
        b.dealer.hand.draw_card(Card("hearts", "jack"))
        b.dealer.hand.draw_card(Card("diamonds", "king"))
        b.dealer.hand.draw_card(Card("clubs", "4"))
        b.score_round(d)
        self.assertEqual(b.outcome, "win")

    def test_blackjack_score_round_player_lose(self):
        b = BlackjackGame()
        b.player = Player(True)
        b.dealer = Player(False)
        d = Display(1200, 700)
        b.player.hand.draw_card(Card("spades", "9"))
        b.dealer.hand.draw_card(Card("hearts", "jack"))
        b.dealer.hand.draw_card(Card("diamonds", "king"))
        b.score_round(d)
        self.assertEqual(b.outcome, "lose")

    def test_blackjack_score_round_player_tie(self):
        b = BlackjackGame()
        b.player = Player(True)
        b.dealer = Player(False)
        d = Display(1200, 700)
        b.player.hand.draw_card(Card("spades", "jack"))
        b.player.hand.draw_card(Card("clubs", "king"))
        b.dealer.hand.draw_card(Card("hearts", "jack"))
        b.dealer.hand.draw_card(Card("diamonds", "king"))
        b.score_round(d)
        self.assertEqual(b.outcome, "tie")

    def test_blackjack_dealer_turn_stand_bust(self):
        b = BlackjackGame()
        b.dealer.hand.draw_card(Card("spades", "10"))
        b.dealer.hand.draw_card(Card("clubs", "7"))
        b.dealer.hand.draw_card(Card("diamonds", "8"))
        b.dealer_turn()
        self.assertEqual(b.dealer.is_standing, True)

    def test_blackjack_dealer_turn_stand_blackjack(self):
        b = BlackjackGame()
        b.dealer.hand.draw_card(Card("spades", "10"))
        b.dealer.hand.draw_card(Card("clubs", "ace"))
        b.dealer_turn()
        self.assertEqual(b.dealer.is_standing, True)

    def test_blackjack_dealer_turn_stand_normal(self):
        b = BlackjackGame()
        b.dealer.hand.draw_card(Card("spades", "10"))
        b.dealer.hand.draw_card(Card("clubs", "7"))
        b.dealer_turn()
        self.assertEqual(b.dealer.is_standing, True)

    def test_blackjack_dealer_turn_hit(self):
        b = BlackjackGame()
        dealer = Player(False)
        dealer.hand.draw_card(Card("spades", "10"))
        b.dealer = dealer
        b.dealer_turn()
        self.assertEqual(b.dealer.is_standing, False)
        self.assertEqual(len(b.dealer.hand.current_hand), 2)

    def test_new_game(self):
        b = BlackjackGame()
        b.new_game()
        self.assertEqual(len(b.player.hand.current_hand), 2)
        self.assertEqual(len(b.dealer.hand.current_hand), 2)
        self.assertEqual(b.dealer.is_standing, False)
        self.assertEqual(b.player.is_standing, False)

if __name__ == "__main__":
    unittest.main()