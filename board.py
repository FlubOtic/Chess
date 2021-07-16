from pieces import Piece, Pawn, Rook, Knight, Bishop, King, Queen
import pygame
import pieces

class Board():
    def __init__(self):
        self.player1 = "White"
        self.player2 = "Black"

    def drawSquares(self, screen, PLAYER_COLOR_1, PLAYER_COLOR_2, SQUARE, SCREEN_HEIGHT):
        self.squares = [[[self.player1, pieces.Piece] for y in range(8)] for x in range(8)] 
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
        for x in range(8):
            for y in range(8):
                if self.squares[x][y][0] == "White":
                    self.squaresGUI[x][y] = pygame.draw.rect(screen, PLAYER_COLOR_1, pygame.Rect(x * SQUARE, SCREEN_HEIGHT - SQUARE - y * SQUARE, SQUARE, SQUARE))
                else:
                    self.squaresGUI[x][y] = pygame.draw.rect(screen, PLAYER_COLOR_2, pygame.Rect(x * SQUARE, SCREEN_HEIGHT - SQUARE - y * SQUARE, SQUARE, SQUARE))
                self.squaresGUI[x][y] = (self.squaresGUI[x][y][0] + SQUARE/2, self.squaresGUI[x][y][1] + SQUARE/2)
                    

    def spawnPieces(self, screen):
        for x in range(8):
            self.squares[x][1][1] = Pawn(screen, self.player1, [x, 1], self.squaresGUI[x][1], "White_Pawn.png")
        self.squares[0][0][1] = Rook(screen, self.player1, [0, 0], self.squaresGUI[0][0], "White_Rook.png")
        self.squares[7][0][1] = Rook(screen, self.player1, [7, 0], self.squaresGUI[7][0], "White_Rook.png")
        self.squares[1][0][1] = Knight(screen, self.player1, [1, 0], self.squaresGUI[1][0], "White_Knight.png")
        self.squares[6][0][1] = Knight(screen, self.player1, [6, 0], self.squaresGUI[6][0], "White_Knight.png")
        self.squares[2][0][1] = Bishop(screen, self.player1, [2, 0], self.squaresGUI[2][0], "White_Bishop.png")
        self.squares[5][0][1] = Bishop(screen, self.player1, [5, 0], self.squaresGUI[5][0], "White_Bishop.png")
        self.squares[4][0][1] = King(screen, self.player1, [4, 0], self.squaresGUI[4][0], "White_King.png")
        self.squares[3][0][1] = Queen(screen, self.player1, [3, 0], self.squaresGUI[3][0], "White_Queen.png")

        for x in range(8):
            self.squares[x][6][1] = Pawn(screen, self.player1, [x, 6], self.squaresGUI[x][6], "Black_Pawn.png")
        self.squares[0][7][1] = Rook(screen, self.player1, [0, 7], self.squaresGUI[0][7], "Black_Rook.png")
        self.squares[7][7][1] = Rook(screen, self.player1, [7, 7], self.squaresGUI[7][7], "Black_Rook.png")
        self.squares[1][7][1] = Knight(screen, self.player1, [1, 7], self.squaresGUI[1][7], "Black_Knight.png")
        self.squares[6][7][1] = Knight(screen, self.player1, [6, 7], self.squaresGUI[6][7], "Black_Knight.png")
        self.squares[2][7][1] = Bishop(screen, self.player1, [2, 7], self.squaresGUI[2][7], "Black_Bishop.png")
        self.squares[5][7][1] = Bishop(screen, self.player1, [5, 7], self.squaresGUI[5][7], "Black_Bishop.png")
        self.squares[4][7][1] = King(screen, self.player1, [4, 7], self.squaresGUI[4][7], "Black_King.png")
        self.squares[3][7][1] = Queen(screen, self.player1, [3, 7], self.squaresGUI[3][7], "Black_Queen.png")

        

        


