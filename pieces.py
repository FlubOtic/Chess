import pygame
import os

IMAGES = os.path.dirname(__file__) + "\\Images\\"

class Piece():
    def __init__(self, screen, color, location, locationGUI, image):
        self.color = color
        self.location = location
        self.locationGUI = locationGUI
        self.img = pygame.image.load(IMAGES + image)
        self.img = pygame.transform.smoothscale(self.img, (int(self.img.get_width()/4.75), int(self.img.get_height()/4.75)))
        self.rect = self.img.get_rect()
        self.rect.center = (locationGUI[0], locationGUI[1])
        screen.blit(self.img, self.rect)
        
class Pawn(Piece):
    def Move(self):
        print("")

class Rook(Piece):
    def Move(self):
        print("")

class Knight(Piece):
    def Move(self):
        print("")

class Bishop(Piece):
    def Move(self):
        print("")

class King(Piece):
    def Move(self):
        print("")

class Queen(Piece):
    def Move(self):
        print("")

        


      
        


