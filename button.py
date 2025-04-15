import pygame

class Button:
    def __init__(self, text, x, y, width, height, display):

        # Just Assigning necessary variables

        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.display = display
        self.clicked = False
        self.display = display

        # Creating the font object for the text object made later

        self.smallfont = pygame.font.SysFont('./BowlbyOneSC-Regular.ttf', 35) 

        # Render the text of the button to the center of the actual button

        self.txt = self.smallfont.render(self.text, True , (0, 0, 0)) 
        self.txt_rect = self.txt.get_rect(center=(self.x + (self.width/2), self.y + (self.height/2)))

        # Draw the button rectangle, then place the text on the rectangle and update the screen

        pygame.draw.rect(self.display.screen, (190, 190, 190), [self.x, self.y, self.width, self.height], border_radius=50)
        self.display.screen.blit(self.txt, self.txt_rect)
        pygame.display.update()

    def check_hovering(self):
        mouse = pygame.mouse.get_pos()

        if (self.x <= mouse[0] <= self.x + self.width) and (self.y <= mouse[1] <= self.y + self.height):
            return True
        
    def hovering_color(self):

        # If the mouse is hovering over the button, render the button 
        # to a darker color to give it the visual feel of it being hovered over

        if self.check_hovering():
            pygame.draw.rect(self.display.screen, (100, 100, 100), [self.x, self.y, self.width, self.height], border_radius=50)
            self.display.screen.blit(self.txt, self.txt_rect)
            pygame.display.update()
        else:
            pygame.draw.rect(self.display.screen, (150, 150, 150), [self.x, self.y, self.width, self.height], border_radius=50)
            self.display.screen.blit(self.txt, self.txt_rect)
            pygame.display.update()




    