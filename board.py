from pieces import Piece, Pawn, Rook, Knight, Bishop, King, Queen
import pygame
import pieces

class Board():
    def __init__(self):
        self.player1 = "White"
        self.player2 = "Black"

        self.selectedPiece = None
        self.selected = False
        
        self.squares = [[[self.player1, None] for y in range(8)] for x in range(8)] 

    def Move(self, mousePos):
        for x in range(8):
            for y in range(8):
                if self.squaresGUI[x][y].collidepoint(mousePos):
                    self.selectedPiece.Move([x, y])
                    self.selectedPiece = None
                    self.selected = False

    def selectPiece(self, mousePos):
        for x in range(8):
            for y in range(8):
                if self.squaresGUI[x][y].collidepoint(mousePos):
                    self.selectedPiece = self.squares[x][y][1]
                    self.selected = True
                #else:
                    #self.selectedPiece = None
                    #self.selected = False

    def drawSquares(self, screen, PLAYER_COLOR_1, PLAYER_COLOR_2, SQUARE, SCREEN_HEIGHT):
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
                    self.squaresGUI[x][y] = pygame.draw.rect(screen, PLAYER_COLOR_1, pygame.Rect(x * SQUARE, SCREEN_HEIGHT - SQUARE - y * SQUARE, SQUARE, SQUARE))
                else:
                    self.squaresGUI[x][y] = pygame.draw.rect(screen, PLAYER_COLOR_2, pygame.Rect(x * SQUARE, SCREEN_HEIGHT - SQUARE - y * SQUARE, SQUARE, SQUARE))
                self.squaresGUIpos[x][y] = (self.squaresGUI[x][y][0] + SQUARE/2, self.squaresGUI[x][y][1] + SQUARE/2)

    def spawnPieces(self, screen):
        for x in range(8):
            self.squares[x][1][1] = Pawn(screen, self.player1, [x, 1], self.squaresGUIpos[x][1], "White_Pawn.png", self)
        self.squares[0][0][1] = Rook(screen, self.player1, [0, 0], self.squaresGUIpos[0][0], "White_Rook.png", self)
        self.squares[7][0][1] = Rook(screen, self.player1, [7, 0], self.squaresGUIpos[7][0], "White_Rook.png", self)
        self.squares[1][0][1] = Knight(screen, self.player1, [1, 0], self.squaresGUIpos[1][0], "White_Knight.png", self)
        self.squares[6][0][1] = Knight(screen, self.player1, [6, 0], self.squaresGUIpos[6][0], "White_Knight.png", self)
        self.squares[2][0][1] = Bishop(screen, self.player1, [2, 0], self.squaresGUIpos[2][0], "White_Bishop.png", self)
        self.squares[5][0][1] = Bishop(screen, self.player1, [5, 0], self.squaresGUIpos[5][0], "White_Bishop.png", self)
        self.squares[4][0][1] = King(screen, self.player1, [4, 0], self.squaresGUIpos[4][0], "White_King.png", self)
        self.squares[3][0][1] = Queen(screen, self.player1, [3, 0], self.squaresGUIpos[3][0], "White_Queen.png", self)

        for x in range(8):
            self.squares[x][6][1] = Pawn(screen, self.player2, [x, 6], self.squaresGUIpos[x][6], "Black_Pawn.png", self)
        self.squares[0][7][1] = Rook(screen, self.player2, [0, 7], self.squaresGUIpos[0][7], "Black_Rook.png", self)
        self.squares[7][7][1] = Rook(screen, self.player2, [7, 7], self.squaresGUIpos[7][7], "Black_Rook.png", self)
        self.squares[1][7][1] = Knight(screen, self.player2, [1, 7], self.squaresGUIpos[1][7], "Black_Knight.png", self)
        self.squares[6][7][1] = Knight(screen, self.player2, [6, 7], self.squaresGUIpos[6][7], "Black_Knight.png", self)
        self.squares[2][7][1] = Bishop(screen, self.player2, [2, 7], self.squaresGUIpos[2][7], "Black_Bishop.png", self)
        self.squares[5][7][1] = Bishop(screen, self.player2, [5, 7], self.squaresGUIpos[5][7], "Black_Bishop.png", self)
        self.squares[4][7][1] = King(screen, self.player2, [4, 7], self.squaresGUIpos[4][7], "Black_King.png", self)
        self.squares[3][7][1] = Queen(screen, self.player2, [3, 7], self.squaresGUIpos[3][7], "Black_Queen.png", self)

    def drawPieces(self, screen):
        for x in range(8):
            for y in range(8):
                if self.squares[x][y][1] is not None:
                    self.squares[x][y][1].Draw()

        

        


