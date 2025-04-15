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
        self.goal = 2000
        self.bet = 0

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

    
    def init_ui(self):
        pass

    #Scores the current hands and decides who wins then resets the game
    def score_round(self, display):
        
        print(self.player.hand.get_hand_value())
        print(self.dealer.hand.get_hand_value())

        #Figure out all of the betting(player wins or loses)
        if self.dealer.hand.get_hand_value() > 21:
            self.outcome = "win"
            self.money_total += self.bet
            self.win_display(display)
        elif self.player.hand.get_hand_value() == self.dealer.hand.get_hand_value():
            self.outcome = "tie"
            self.tie_display(display)
        elif self.player.hand.get_hand_value() > self.dealer.hand.get_hand_value():
            self.outcome = "win"
            self.money_total += self.bet
            self.win_display(display)
        elif self.player.hand.get_hand_value() < self.dealer.hand.get_hand_value():
            self.outcome = "lose"
            self.money_total -= self.bet
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

            current_card = pygame.image.load(f"img/cards/{rank}_of_{suit}.png")
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

            current_card = pygame.image.load(f"img/cards/{rank}_of_{suit}.png")
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

    def render_goal(self, display):

        # Set up font object

        smallfont = pygame.font.Font('./BowlbyOneSC-Regular.ttf', 20) 
        
        # Draw backdrop

        pygame.draw.rect(display.screen, (0, 0, 0), [640, 620, 220, 70], border_radius=50)
        pygame.draw.rect(display.screen, (50, 50, 50), [650, 625, 200, 60], border_radius=50)

        # Render goal and center with backdrop

        goal_txt = smallfont.render(f"Goal: {self.goal}", True , (255, 255, 255))
        goal_txt_rect = goal_txt.get_rect(center=(745, 655))

        # Update the screen with the text objects

        display.screen.blit(goal_txt, goal_txt_rect)

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

                    elif exit_button.check_hovering():

                        # Exit the game if they click exit
                        self.save_game()

                        sys.exit()


    def render_text_background(self, text, display):
        
        smallfont = pygame.font.SysFont('./BowlbyOneSC-Regular.ttf', 100, bold=True) 

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

        self.render_text_background("You Win!", display)

        txt = smallfont.render("You Win!", True, (255, 255, 255)) 
        txt_rect = txt.get_rect(center=(600, 250))

        display.screen.blit(txt, txt_rect)
        pygame.display.update()

    def lose_display(self, display):

        smallfont = pygame.font.SysFont('./BowlbyOneSC-Regular.ttf', 100, bold=True) 

        self.render_text_background("You Lose!", display)

        txt = smallfont.render("You Lose!", True, (255, 255, 255)) 
        txt_rect = txt.get_rect(center=(600, 250))

        display.screen.blit(txt, txt_rect)
        pygame.display.update()

    def tie_display(self, display):

        smallfont = pygame.font.SysFont('./BowlbyOneSC-Regular.ttf', 100, bold=True) 

        self.render_text_background("Tie!", display)

        txt = smallfont.render("Tie!", True, (255, 255, 255)) 
        txt_rect = txt.get_rect(center=(600, 250))

        display.screen.blit(txt, txt_rect)
        pygame.display.update()

    def bet_display(self, display):

        smallfont = pygame.font.SysFont('./BowlbyOneSC-Regular.ttf', 100, bold=True)
        smallfont2 = pygame.font.SysFont('./BowlbyOneSC-Regular.ttf', 50, bold=True)

        self.render_text_background("Make Your Bet!", display)

        pygame.draw.rect(display.screen, (0, 0, 0), [280, 320, 620, 100], border_radius=50)
        pygame.draw.rect(display.screen, (50, 50, 50), [290, 325, 600, 90], border_radius=50)

        txt = smallfont.render("Make Your Bet!", True, (255,255, 255),) 
        txt_rect = txt.get_rect(center=(600, 250))

        txt2 = smallfont2.render(f'Bet: {self.bet}', True, (255, 255, 255),) 
        txt_rect2 = txt.get_rect(center=(830, 360))

        display.screen.blit(txt, txt_rect)
        display.screen.blit(txt2, txt_rect2)
        pygame.display.update()

    def bet_render(self, display):
        
        # Create both the play and exit button and create boolean
        # to keep together the while loop

        sub1000 = Button("-1000", 310, 370, 75, 25, display)
        sub500 = Button("-500", 390, 370, 75, 25, display)
        sub100 = Button("-100", 470, 370, 75, 25, display)
        submit = Button("Bet", 550, 370, 75, 25, display)
        add100 = Button("+100", 630, 370, 75, 25, display)
        add500 = Button("+500", 710, 370, 75, 25, display)
        add1000 = Button("+1000", 790, 370, 75, 25, display)
        made_choice = False

        while not made_choice:
            
            # Wait for player to make choice

            sub1000.hovering_color()
            sub500.hovering_color()
            sub100.hovering_color()
            submit.hovering_color()
            add100.hovering_color()
            add500.hovering_color()
            add1000.hovering_color()

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:

                    # If the player clicks on "Play Again", 
                    # Restart the game and reset the display

                    if sub1000.check_hovering():
                        if self.bet-1000 >= 0:
                            self.bet -= 1000
                            self.bet_display(display)

                    elif sub500.check_hovering():
                        if self.bet-500 >= 0:
                            self.bet -= 500
                            self.bet_display(display)
                    
                    elif sub100.check_hovering():
                        if self.bet-100 >= 0:
                            self.bet -= 100
                            self.bet_display(display)

                    elif add100.check_hovering():
                        if self.bet+100 <= self.money_total:
                            self.bet += 100
                            self.bet_display(display)

                    elif add500.check_hovering():
                        if self.bet+500 <= self.money_total:
                            self.bet += 500
                            self.bet_display(display)
                    
                    elif add1000.check_hovering():
                        if self.bet+1000 <= self.money_total:
                            self.bet += 1000
                            self.bet_display(display)

                    elif submit.check_hovering():
                        made_choice = True
                        display.reset_screen()
                        self.new_game()

    def new_game(self):
        self.bet = 0
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

        new_game_button = Button("New Save", 320, 350, 250, 100, display)
        load_game_button = Button("Load Save", 620, 350, 250, 100, display)

        while self.play_game:

            for event in pygame.event.get():
                
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

        # Setting up hit and stand button for the GUI

        hit_button = Button("Hit", 980, 480, 150, 75, d)
        stand_button = Button("Stand", 980, 355, 150, 75, d)
        quit_button = Button("Quit", 980, 75, 150, 75, d)

        game.render_cards(d)
        game.render_money(d)
        game.bet_display(d)
        game.bet_render(d)
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
                game.render_goal(d)

                if game.money_total >= game.goal:
                    game.goal *= 2

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
                    game.money_total -= game.bet
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