import pygame
import os

import pieces
from pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook


class Board():
    def __init__(self, BOARD, SQUARE, screen):
        self.IMAGES = os.path.dirname(__file__) + "\\Images\\"
        self.player1 = "White"
        self.player2 = "Black"

        self.player1Score = 0
        self.player2Score = 0

        self.player1Moves = 0
        self.player2Moves = 0

        self.selectedPiece = None
        self.selected = False

        self.promotion = [False, None]
        
        self.squares = [[[self.player1, None] for y in range(8)] for x in range(8)] 

        self.BOARD = BOARD
        self.SQUARE = SQUARE

        self.screen = screen

        self.player1Pieces = []
        self.player2Pieces = []

        self.castled = False

    def MovePiece(self, mousePos):
        self.player1Seen = [[False for y in range(8)] for x in range(8)] 
        self.player2Seen = [[False for y in range(8)] for x in range(8)] 

        self.player1Seen = self.SquaresSeen(self.player1Pieces, self.player1Seen)
        self.player2Seen = self.SquaresSeen(self.player2Pieces, self.player2Seen)

        for x in range(8):
            for y in range(8):
                if self.squaresGUI[x][y].collidepoint(mousePos):
                    if (self.squares[x][y][1] == None or self.squares[x][y][1].color is not self.selectedPiece.color or self.selectedPiece.name == "King") and self.selectedPiece.isAvailable([x, y]):
                        self.selectedPiece.Move([x, y])
                        self.selectedPiece.outlined = False
                        self.selectedPiece = None
                        self.selected = False
                        if self.squares[x][y][1].promotion:
                            self.Promotion(self.squares[x][y][1])
                        return True
                    elif self.castled:
                        self.castled = False
                        self.selectedPiece.outlined = False
                        self.selectedPiece = None
                        self.selected = False
                        return True
                    elif (self.squares[x][y][1] == None or self.squares[x][y][1].color is not self.selectedPiece.color) and not self.selectedPiece.isAvailable([x,y]):
                        self.selectedPiece.outlined = False
                        self.selectedPiece = None
                        self.selected = False
                        return False
                    elif self.squares[x][y][1].color is self.selectedPiece.color:
                        self.selectedPiece.outlined = False
                        self.selectedPiece = self.squares[x][y][1]
                        self.selectedPiece.outlined = True
                        self.selected = True
                        return False      

    def SquaresSeen(self, pieces, seen):
        for i, piece in enumerate(pieces):
            for x in range(8):
                for y in range(8):
                    if not seen[x][y] and piece.See()[x][y]:
                        seen[x][y] = True
        return seen

    def SelectPiece(self, mousePos, curPlayer):
        if not self.promotion[0]:
            for x in range(8):
                for y in range(8):
                    if self.squaresGUI[x][y].collidepoint(mousePos) and self.squares[x][y][1] != None:
                        if self.squares[x][y][1].color == curPlayer:
                            self.selectedPiece = self.squares[x][y][1]
                            self.selectedPiece.outlined = True
                            self.selected = True
                        elif self.squares[x][y][1].color != curPlayer and self.selected:
                            self.selectedPiece.outlined = False
                            self.selectedPiece = None
                            self.selected = False
        else:
            for i, rect in enumerate(self.proRect):
                if self.proRect[i].collidepoint(mousePos):
                    self.promotion[1].Die()
                    if self.proRect[i] == self.proRect[0]:
                        self.squares[self.promotion[1].location[0]][self.promotion[1].location[1]][1] = Queen(self.screen, self.promotion[1].color, self.promotion[1].location, 
                                                                                                            self.promotion[1].locationGUI, self, self.SQUARE)
                        self.promotion = [False, None]
                    elif self.proRect[i] == self.proRect[1]:
                        self.squares[self.promotion[1].location[0]][self.promotion[1].location[1]][1] = Rook(self.screen, self.promotion[1].color, self.promotion[1].location, 
                                                                                                            self.promotion[1].locationGUI, self, self.SQUARE)
                        self.promotion = [False, None]
                    elif self.proRect[i] == self.proRect[2]:
                        self.squares[self.promotion[1].location[0]][self.promotion[1].location[1]][1] = Bishop(self.screen, self.promotion[1].color, self.promotion[1].location, 
                                                                                                            self.promotion[1].locationGUI, self, self.SQUARE)
                        self.promotion = [False, None]
                    elif self.proRect[i] == self.proRect[3]:
                        self.squares[self.promotion[1].location[0]][self.promotion[1].location[1]][1] = Knight(self.screen, self.promotion[1].color, self.promotion[1].location, 
                                                                                                            self.promotion[1].locationGUI, self, self.SQUARE)
                        self.promotion = [False, None]
                        
                        

    def DrawSquares(self, PLAYER_COLOR_1, PLAYER_COLOR_2, HUD_H, SCREEN_HEIGHT):
        isBlack = False
        for x, s in enumerate(self.squares):
            for y, ss in enumerate(self.squares[x]):
                if isBlack:
                    self.squares[x][y][0] = self.player2
                    isBlack = False
                else:
                    isBlack = True
            isBlack = True if isBlack == False else False 

        self.squaresGUI = [[0 for y in range(8)] for x in range(8)] 
        self.squaresGUIpos = [[0 for y in range(8)] for x in range(8)]
        for x in range(8):
            for y in range(8):
                if self.squares[x][y][0] == "White":
                    self.squaresGUI[x][y] = pygame.draw.rect(self.screen, PLAYER_COLOR_1, pygame.Rect(x * self.SQUARE, SCREEN_HEIGHT - HUD_H/2 - self.SQUARE - y * self.SQUARE, self.SQUARE, self.SQUARE))
                else:
                    self.squaresGUI[x][y] = pygame.draw.rect(self.screen, PLAYER_COLOR_2, pygame.Rect(x * self.SQUARE, SCREEN_HEIGHT - HUD_H/2 - self.SQUARE - y * self.SQUARE, self.SQUARE, self.SQUARE))
                self.squaresGUIpos[x][y] = (self.squaresGUI[x][y][0] + self.SQUARE/2, self.squaresGUI[x][y][1] + self.SQUARE/2)


    def UpdateScore(self, point, color):
        if color == self.player1:
            self.player1Score -= point
        else:
            self.player2Score -= point

    def SpawnPieces(self):
        for x in range(8):
            self.squares[x][1][1] = Pawn(self.screen, self.player1, [x, 1], self.squaresGUIpos[x][1], self, self.SQUARE)
        self.squares[0][0][1] = Rook(self.screen, self.player1, [0, 0], self.squaresGUIpos[0][0], self, self.SQUARE)
        self.squares[7][0][1] = Rook(self.screen, self.player1, [7, 0], self.squaresGUIpos[7][0], self, self.SQUARE)
        self.squares[1][0][1] = Knight(self.screen, self.player1, [1, 0], self.squaresGUIpos[1][0], self, self.SQUARE)
        self.squares[6][0][1] = Knight(self.screen, self.player1, [6, 0], self.squaresGUIpos[6][0], self, self.SQUARE)
        self.squares[2][0][1] = Bishop(self.screen, self.player1, [2, 0], self.squaresGUIpos[2][0], self, self.SQUARE)
        self.squares[5][0][1] = Bishop(self.screen, self.player1, [5, 0], self.squaresGUIpos[5][0], self, self.SQUARE)
        self.squares[4][0][1] = King(self.screen, self.player1, [4, 0], self.squaresGUIpos[4][0], self, self.SQUARE)
        self.squares[3][0][1] = Queen(self.screen, self.player1, [3, 0], self.squaresGUIpos[3][0], self, self.SQUARE)

        for x in range(8):
            self.squares[x][6][1] = Pawn(self.screen, self.player2, [x, 6], self.squaresGUIpos[x][6], self, self.SQUARE)
        self.squares[0][7][1] = Rook(self.screen, self.player2, [0, 7], self.squaresGUIpos[0][7], self, self.SQUARE)
        self.squares[7][7][1] = Rook(self.screen, self.player2, [7, 7], self.squaresGUIpos[7][7], self, self.SQUARE)
        self.squares[1][7][1] = Knight(self.screen, self.player2, [1, 7], self.squaresGUIpos[1][7], self, self.SQUARE)
        self.squares[6][7][1] = Knight(self.screen, self.player2, [6, 7], self.squaresGUIpos[6][7], self, self.SQUARE)
        self.squares[2][7][1] = Bishop(self.screen, self.player2, [2, 7], self.squaresGUIpos[2][7], self, self.SQUARE)
        self.squares[5][7][1] = Bishop(self.screen, self.player2, [5, 7], self.squaresGUIpos[5][7], self, self.SQUARE)
        self.squares[4][7][1] = King(self.screen, self.player2, [4, 7], self.squaresGUIpos[4][7], self, self.SQUARE)
        self.squares[3][7][1] = Queen(self.screen, self.player2, [3, 7], self.squaresGUIpos[3][7], self, self.SQUARE)

    def DrawPieces(self):
        for x in range(8):
            for y in range(8):
                if self.squares[x][y][1] is not None:
                    self.squares[x][y][1].Draw()
        if self.promotion[0]:
            for i, img in enumerate(self.proImgs):
                self.screen.blit(img, self.proRect[i])

    def DrawScore(self, HUD_H):
        scoreFont = pygame.font.Font(os.path.dirname(__file__) + "\\ArchivoBlack-Regular.ttf", int(30*self.screen.get_height()/694))
        if self.player1Score - self.player2Score >= 0:
            player1Text = scoreFont.render("+" + str(self.player1Score - self.player2Score), True, (255, 255, 255))

            textRect1 = player1Text.get_rect()
            textRect1.center = (self.screen.get_width()/21, self.screen.get_height() - HUD_H/4)
            self.screen.blit(player1Text, textRect1)

            player2Text = scoreFont.render("+0", True, (255, 255, 255))

            textRect2 = player2Text.get_rect()
            textRect2.center = (self.screen.get_width()/21, HUD_H/4)
            self.screen.blit(player2Text, textRect2)
            return
        if self.player2Score - self.player1Score >= 0:
            player2Text = scoreFont.render("+" + str(self.player2Score - self.player1Score), True, (255, 255, 255))
            
            textRect2 = player2Text.get_rect()
            textRect2.center = (self.screen.get_width()/21, HUD_H/4)
            self.screen.blit(player2Text, textRect2)

            player1Text = scoreFont.render("+0", True, (255, 255, 255))

            textRect1 = player1Text.get_rect()
            textRect1.center = (self.screen.get_width()/21, self.screen.get_height() - HUD_H/4)
            self.screen.blit(player1Text, textRect1)
            return
        
    def Promotion(self, pawn):
        self.promotion = [True, pawn]
        self.proImgs = [None, None, None, None]
        self.proRect = [None, None, None, None]
        scale = [None, None, None, None]


        self.proImgs[0] = pygame.image.load(self.IMAGES + self.promotion[1].color + "_Queen.png")
        self.proImgs[1] = pygame.image.load(self.IMAGES + self.promotion[1].color + "_Rook.png")
        self.proImgs[2] = pygame.image.load(self.IMAGES + self.promotion[1].color + "_Bishop.png")
        self.proImgs[3] = pygame.image.load(self.IMAGES + self.promotion[1].color + "_Knight.png")

        imgSize = 1
        for i, img in enumerate(self.proImgs):
            scale[i] = min(self.SQUARE / img.get_width(), self.SQUARE / img.get_height()) * imgSize
            self.proImgs[i] = pygame.transform.smoothscale(self.proImgs[i], (round(self.proImgs[i].get_width() * scale[i]), round(self.proImgs[i].get_height() * scale[i])))
            self.proRect[i] = self.proImgs[i].get_rect()
            self.proRect[i].center = ((self.screen.get_width()/5) * (i + 1), self.screen.get_height()/2)