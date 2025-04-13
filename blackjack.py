import random
import pygame
from display import Display
from deck import Deck
from player import Player
from button import Button
import sys
import os


class BlackjackGame:
    def __init__(self):

        # Initialize the Deck and both the Player and Dealer classes

        self.deck = Deck()
        self.player = Player(True)
        self.dealer = Player(False)

        self.outcome = ""

        self.money_total = 0
        self.rounds_total = 0
        
        # Variable to keep track of whether or not the game is being played
        self.play_game = True
        
        self.init_ui()
        pygame.init()
        self.new_game()
    
    def deal_start_cards(self):
        #BLACKJAKE AMIRAITE
        # Make a new deck

        self.deck.reset_deck()

        # Draws two cards per player to start off

        self.player.hand.draw_card(self.deck.deal_card())
        self.player.hand.draw_card(self.deck.deal_card())
        self.dealer.hand.draw_card(self.deck.deal_card())
        self.dealer.hand.draw_card(self.deck.deal_card())
    
    def init_ui(self):
        pass

    #Scores the current hands and decides who wins then resets the game
    def score_round(self, display):
        
        print(self.player.hand.get_hand_value())
        print(self.dealer.hand.get_hand_value())

        #Figure out all of the betting(player wins or loses)
        if self.dealer.hand.get_hand_value() > 21:
            self.outcome = "win"
            self.money_total += 100
            self.win_display(display)
        elif self.player.hand.get_hand_value() == self.dealer.hand.get_hand_value():
            self.outcome = "tie"
            self.tie_display(display)
        elif self.player.hand.get_hand_value() > self.dealer.hand.get_hand_value():
            self.outcome = "win"
            self.money_total += 100
            self.win_display(display)
        elif self.player.hand.get_hand_value() < self.dealer.hand.get_hand_value():
            self.outcome = "lose"
            self.money_total -= 100
            self.lose_display(display)

    def dealer_turn(self):
        
        # If the dealer has either blackjack or bust, they "stand" (don't take any more turns)

        if self.dealer.hand.is_blackjack() or self.dealer.hand.is_bust():
            self.dealer.stand()

        #If dealer hand has value less than 21 and greater than 16 they stand
        if self.dealer.hand.get_hand_value() >= 17 and self.dealer.hand.get_hand_value() < 21:
            self.dealer.stand()

        # If the dealer has a hand value less than 17, they hit

        if self.dealer.hand.get_hand_value() < 17:
            self.dealer.hit(self.deck.deal_card())

    def render_cards(self, display):

        # Render the player's hand

        for i in range(len(self.player.hand.current_hand)):

            # Establish rank and suit variables (for better readability)

            rank = self.player.hand.current_hand[i].rank
            suit = self.player.hand.current_hand[i].suit

            # Load image from file and scale it down 

            current_card = pygame.image.load(f"img\cards\{rank}_of_{suit}.png")
            current_card = pygame.transform.scale(current_card, (120, 160))

            # Calculate x value of card, center it, then draw it

            current_card_rect = current_card.get_rect(center=((200 + (135 * i)), 525))
            display.screen.blit(current_card, current_card_rect)

        # Render the dealer's hand

        for i in range(len(self.dealer.hand.current_hand)):

            # Establish rank and suit variables (for better readability)

            rank = self.dealer.hand.current_hand[i].rank
            suit = self.dealer.hand.current_hand[i].suit

            # Load image from file and scale it down 

            current_card = pygame.image.load(f"img\cards\{rank}_of_{suit}.png")
            current_card = pygame.transform.scale(current_card, (120, 160))

            # Calculate x value of card, center it, then draw it

            current_card_rect = current_card.get_rect(center=((200 + (135 * i)), 200))
            display.screen.blit(current_card, current_card_rect)

    def render_scores(self, display):

        # Set up font object

        smallfont = pygame.font.Font('./BowlbyOneSC-Regular.ttf', 30) 

        # Draw both backdrops for the player and dealer value text

        pygame.draw.rect(display.screen, (0, 0, 0), [180, 15, 440, 80], border_radius=50)
        pygame.draw.rect(display.screen, (0, 0, 0), [180, 615, 440, 80], border_radius=50)

        pygame.draw.rect(display.screen, (50, 50, 50), [200, 25, 400, 60], border_radius=50)
        pygame.draw.rect(display.screen, (50, 50, 50), [200, 625, 400, 60], border_radius=50)

        
        # Render out the font and center it at the backdrops 

        dealer_txt = smallfont.render(f"Dealer Value: {self.dealer.hand.get_hand_value()}", True , (255, 255, 255))
        dealer_txt_rect = dealer_txt.get_rect(center=(400, 55))

        player_txt = smallfont.render(f"Player Value: {self.player.hand.get_hand_value()}", True , (255, 255, 255))
        player_txt_rect = player_txt.get_rect(center=(400, 655))

        # Update the screen with the text objects

        display.screen.blit(player_txt, player_txt_rect)
        display.screen.blit(dealer_txt, dealer_txt_rect)

        pygame.display.update()
    
    def render_money(self, display):
       
        # Set up font object

        smallfont = pygame.font.Font('./BowlbyOneSC-Regular.ttf', 20) 
        
        # Draw backdrop

        pygame.draw.rect(display.screen, (0, 0, 0), [640, 20, 220, 70], border_radius=50)
        pygame.draw.rect(display.screen, (50, 50, 50), [650, 25, 200, 60], border_radius=50)

        # Render the amount of money the player has and center with backdrop

        money_txt = smallfont.render(f"Money: {self.money_total}", True , (255, 255, 255))
        money_txt_rect = money_txt.get_rect(center=(745, 55))

        # Update the screen with the text objects

        display.screen.blit(money_txt, money_txt_rect)

    def play_again_render(self, display):
        
        # Create both the play and exit button and create boolean
        # to keep together the while loop

        play_button = Button("Play Again", 320, 350, 250, 100, display)
        exit_button = Button("Exit Game", 620, 350, 250, 100, display)
        made_choice = False

        while not made_choice:
            
            # Wait for player to make choice

            play_button.hovering_color()
            exit_button.hovering_color()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    # If the player clicks on "Play Again", 
                    # Restart the game and reset the display

                    if play_button.check_hovering():
                        made_choice = True
                        display.reset_screen()
                        self.new_game()
                        self.render_deck(d)

                    elif exit_button.check_hovering():

                        # Exit the game if they click exit
                        self.save_game()

                        sys.exit()

    def render_deck(self, display):

        for i in range(5):

            current_card = pygame.image.load(f"img/back-side.png")
            current_card = pygame.transform.scale(current_card, (120, 160))
            current_card_rect = current_card.get_rect(center=((800, 375 - (i * 10))))
            display.screen.blit(current_card, current_card_rect)

    def title_screen_cards(self, display, x, offset, card_scroll):

        card_scroll_rect = card_scroll.get_rect(center=((x, (800 + offset))))
        display.screen.blit(card_scroll, card_scroll_rect)
        

    def render_text_background(self, text, display, text_size):
        
        smallfont = pygame.font.SysFont('./BowlbyOneSC-Regular.ttf', text_size, bold=True) 

        txt_ul = smallfont.render(text, True, (0, 0, 0)) 
        txt_ul_rect = txt_ul.get_rect(center=(595, 245))

        display.screen.blit(txt_ul, txt_ul_rect)

        txt_ur = smallfont.render(text, True, (0, 0, 0)) 
        txt_ur_rect = txt_ur.get_rect(center=(605, 245))

        display.screen.blit(txt_ur, txt_ur_rect)

        txt_ll = smallfont.render(text, True, (0, 0, 0)) 
        txt_ll_rect = txt_ll.get_rect(center=(595, 255))

        display.screen.blit(txt_ll, txt_ll_rect)

        txt_lr = smallfont.render(text, True, (0, 0, 0)) 
        txt_lr_rect = txt_lr.get_rect(center=(605, 255))

        display.screen.blit(txt_lr, txt_lr_rect)
        

        pygame.display.update()

    def win_display(self, display):

        smallfont = pygame.font.SysFont('./BowlbyOneSC-Regular.ttf', 100, bold=True) 

        self.render_text_background("You Win!", display, 100)

        txt = smallfont.render("You Win!", True, (255, 255, 255)) 
        txt_rect = txt.get_rect(center=(600, 250))

        display.screen.blit(txt, txt_rect)
        pygame.display.update()

    def lose_display(self, display):

        smallfont = pygame.font.SysFont('./BowlbyOneSC-Regular.ttf', 100, bold=True) 

        self.render_text_background("You Lose!", display, 100)

        txt = smallfont.render("You Lose!", True, (255, 255, 255)) 
        txt_rect = txt.get_rect(center=(600, 250))

        display.screen.blit(txt, txt_rect)
        pygame.display.update()

    def tie_display(self, display):

        smallfont = pygame.font.SysFont('./BowlbyOneSC-Regular.ttf', 100, bold=True) 

        self.render_text_background("Tie!", display, 100)

        txt = smallfont.render("Tie!", True, (255, 255, 255)) 
        txt_rect = txt.get_rect(center=(600, 250))

        display.screen.blit(txt, txt_rect)
        pygame.display.update()

    def draw_title_text(self, display):
        smallfont = pygame.font.SysFont('./BowlbyOneSC-Regular.ttf', 150, bold=True) 

        self.render_text_background("Blackjack", display, 150)

        txt = smallfont.render("Blackjack", True, (255, 255, 255)) 
        txt_rect = txt.get_rect(center=(600, 250))

        display.screen.blit(txt, txt_rect)
        pygame.display.update()

    def new_game(self):
        self.player.hand.reset_hand()
        self.player.is_standing = False
        self.dealer.hand.reset_hand()
        self.dealer.is_standing = False
        self.deal_start_cards()

    def new_save(self):
        self.money_total = 1000

    def load_save(self):
        with open("./save_file.txt", "r") as file:
            self.money_total = int(file.read())

    def save_game(self):
        with open("./save_file.txt", "w") as file:
            file.write(str(self.money_total))

    def intro_screen(self, display):

        pygame.draw.rect(display.screen, (41, 196, 18), [0, 0, 1200, 700])
        self.draw_title_text(display)

        card_scroll_first = pygame.image.load("img/card-back-scroll.png")
        card_scroll_second = pygame.image.load("img/card-back-scroll.png")

        first_card_offset = 0
        second_card_offset = 0

        new_game_button = Button("New Save", 320, 400, 250, 100, display)
        load_game_button = Button("Load Save", 620, 400, 250, 100, display)

        while self.play_game:

            self.title_screen_cards(display, 120, first_card_offset, card_scroll_first)
            self.title_screen_cards(display, 1080, second_card_offset, card_scroll_second)
            first_card_offset -= 0.5
            second_card_offset += 0.5

            for event in pygame.event.get():
                
                new_game_button.hovering_color()
                load_game_button.hovering_color()
                

                if event.type == pygame.QUIT:
                    self.play_game = False
                    return False

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if new_game_button.check_hovering():
                        self.new_save()
                        return True
                    
                    elif load_game_button.check_hovering():
                        self.load_save()
                        return True
        
    

if __name__ == "__main__":

    # Set up the main display class and the main game class

    d = Display(1200, 700)
    game = BlackjackGame()

    if game.intro_screen(d):

        d.reset_screen()
        game.render_deck(d)

        # Setting up hit and stand button for the GUI

        hit_button = Button("Hit", 980, 480, 150, 75, d)
        stand_button = Button("Stand", 980, 355, 150, 75, d)
        quit_button = Button("Quit", 980, 75, 150, 75, d)

        game.render_cards(d)

        # Constant loop to keep the game running as long as the player doesn't exit out of the window.

        while d.running and game.play_game:
            
            # Player continues to hit until they stand. Then dealer does their turns.
            
            for event in pygame.event.get():    

                # This renders all of the buttons (with hovering functionality)
                # and renders the necessary text elements

                hit_button.hovering_color()
                stand_button.hovering_color()
                quit_button.hovering_color()
                game.render_scores(d)
                game.render_money(d)
                game.render_cards(d)

                if event.type == pygame.QUIT: 
                    game.save_game()
                    d.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    # If the mouse button is clicked while hovering over
                    # hit/stand/quit button, perform that actions

                    if hit_button.check_hovering():
                        game.player.hit(game.deck.deal_card())

                    elif stand_button.check_hovering():
                        game.player.stand()

                    elif quit_button.check_hovering():
                        game.save_game()
                        game.play_game = False

                #Checks if player stands or busts after every turn then goes to dealers turn if player stood
                if game.player.hand.is_bust():
                    print("Player busts/ new game")
                    game.money_total -= 100
                    game.render_cards(d)
                    game.lose_display(d)
                    game.render_scores(d)
                    game.render_money(d)
                    game.play_again_render(d)
                elif game.player.is_standing:
                    print("Dealer Turn")
                    while game.dealer.is_standing == False:
                        game.dealer_turn()
                        

                    if game.dealer.is_standing:
                        game.render_cards(d)
                        game.score_round(d)
                        game.render_scores(d)
                        game.render_money(d)
                        game.play_again_render(d)

            pygame.display.flip()