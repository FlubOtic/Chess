from pygame import draw
import board
import pygame
import os

IMAGES = os.path.dirname(__file__) + "\\Images\\"

class Piece():
    def __init__(self, screen, color, location, locationGUI, image, board):
        self.board = board
        self.screen = screen
        self.color = color
        self.location = location
        self.locationGUI = locationGUI
        self.img = pygame.image.load(IMAGES + image)
        self.img = pygame.transform.smoothscale(self.img, (int(self.img.get_width()/4.75), int(self.img.get_height()/4.75)))
        self.rect = self.img.get_rect()
        self.rect.center = (self.locationGUI[0], self.locationGUI[1])
        self.screen.blit(self.img, self.rect)
    
    def Move(self, location):
        self.board.squares[self.location[0]][self.location[1]][1] = None
        self.board.squares[location[0]][location[1]][1] = self
        self.locationGUI = self.board.squaresGUIpos[location[0]][location[1]]

        self.rect.center = (self.locationGUI[0], self.locationGUI[1])

    def Draw(self):
        self.screen.blit(self.img, self.rect)

        
class Pawn(Piece):
    pass

class Rook(Piece):
    pass

class Knight(Piece):
    pass

class Bishop(Piece):
    pass

class King(Piece):
    pass

class Queen(Piece):
    pass

        


      
        


