from pygame import draw
import board
import pygame
import os



class Piece():
    def __init__(self, screen, color, location, locationGUI, image, board, SQUARE):
        IMAGES = os.path.dirname(__file__) + "\\Images\\"

        self.board = board
        self.screen = screen

        self.color = color
        self.moves = 0
        self.alive = True
        self.outlined = False
        self.enpassant = [False, 0]
    
        self.location = location
        self.locationGUI = locationGUI

        self.img = pygame.image.load(IMAGES + image)
        imgSize = 0.8
        scale = min(SQUARE / self.img.get_width(), SQUARE / self.img.get_height()) * imgSize
        self.img = pygame.transform.smoothscale(self.img, (round(self.img.get_width() * scale), round(self.img.get_height() * scale)))

        self.rect = self.img.get_rect()
        self.rect.center = (self.locationGUI[0], self.locationGUI[1])

        self.promotion = False

    def Move(self, movLocation):
        self.board.squares[self.location[0]][self.location[1]][1] = None
        if self.board.squares[movLocation[0]][movLocation[1]][1] != None:
            self.board.squares[movLocation[0]][movLocation[1]][1].Die()
        self.board.squares[movLocation[0]][movLocation[1]][1] = self

        self.location = movLocation
        self.locationGUI = self.board.squaresGUIpos[movLocation[0]][movLocation[1]]

        self.rect.center = (self.locationGUI[0], self.locationGUI[1])

        self.moves += 1
        if self.color == "White":
            self.board.player1Moves += 1
        else:
            self.board.player2Moves += 1

    def OppositeColor(self):
        if self.color == "White": 
            return "Black"
        else: 
            return "White"

    def Draw(self):
        if self.alive:
            self.screen.blit(self.img, self.rect)

            if self.outlined:
                pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)

        
class Pawn(Piece):
    def __init__(self, screen, color, location, locationGUI, board, SQUARE):
        self.name = "Pawn"
        image = color + "_" + self.name + ".png"
        self.value = 1
        if color == "White":
            board.player1Score += self.value
            board.player1Pieces.append(self)
        else:
            board.player2Score += self.value
            board.player2Pieces.append(self)
        super().__init__(screen, color, location, locationGUI, image, board, SQUARE)

    def Die(self):
            self.board.UpdateScore(self.value, self.color)
            self.alive = False
            self.board.squares[self.location[0]][self.location[1]][1] = None

    def isAvailable(self, avLocation):
        if self.board.squares[avLocation[0]][avLocation[1]][1] == None:
            if self.color == "White":
                for x in range(8):
                    if [x, 7] == avLocation:
                        self.promotion = True
                        print("true")
                        break
                if self.moves == 0: 
                    if avLocation == [self.location[0], self.location[1] + 1]:
                        return True
                    if avLocation == [self.location[0], self.location[1] + 2]:
                        self.enpassant = [True, self.board.player1Moves + 1]
                        return True
                elif self.moves > 0:
                    if avLocation == [self.location[0], self.location[1] + 1]:
                        return True
                if self.board.squares[avLocation[0]][avLocation[1] - 1][1] != None:  
                    if self.board.squares[avLocation[0]][avLocation[1] - 1][1] == self.board.squares[self.location[0] - 1][self.location[1]][1] or self.board.squares[avLocation[0]][avLocation[1] - 1][1] == self.board.squares[self.location[0] + 1][self.location[1]][1]:
                        if self.board.squares[avLocation[0]][avLocation[1] - 1][1].name == self.name and self.board.squares[avLocation[0]][avLocation[1] - 1][1].color == self.OppositeColor():
                            if self.board.squares[avLocation[0]][avLocation[1] - 1][1].enpassant[0] and self.board.player2Moves == self.board.squares[avLocation[0]][avLocation[1] - 1][1].enpassant[1]:
                                self.board.squares[avLocation[0]][avLocation[1] - 1][1].Die()
                                return True
                self.promotion = False
                print("FAlse")
            elif self.color == "Black":
                for x in range(8):
                    if [x, 0] == avLocation:
                        self.promotion = True
                        break
                if self.moves == 0:
                    if avLocation == [self.location[0], self.location[1] - 1]:
                        return True
                    elif avLocation == [self.location[0], self.location[1] - 2]:
                        self.enpassant = [True, self.board.player2Moves + 1]
                        return True
                elif self.moves > 0:
                    if avLocation == [self.location[0], self.location[1] - 1]:
                        return True
                if self.board.squares[avLocation[0]][avLocation[1] + 1][1] != None:        
                    if self.board.squares[avLocation[0]][avLocation[1] + 1][1] == self.board.squares[self.location[0] - 1][self.location[1]][1] or self.board.squares[avLocation[0]][avLocation[1] + 1][1] == self.board.squares[self.location[0] + 1][self.location[1]][1]:
                        if self.board.squares[avLocation[0]][avLocation[1] + 1][1].name == self.name and self.board.squares[avLocation[0]][avLocation[1] + 1][1].color == self.OppositeColor():
                            if self.board.squares[avLocation[0]][avLocation[1] + 1][1].enpassant[0] and self.board.player1Moves == self.board.squares[avLocation[0]][avLocation[1] + 1][1].enpassant[1]:
                                self.board.squares[avLocation[0]][avLocation[1] + 1][1].Die()
                                return True
                self.promotion = False
        elif self.board.squares[avLocation[0]][avLocation[1]][1].color == self.OppositeColor():
            if self.color == "White" and (avLocation == [self.location[0] - 1, self.location[1] + 1] or avLocation == [self.location[0] + 1, self.location[1] + 1]):
                for x in range(8):
                    if [x, 7] == avLocation:
                        self.promotion = True
                        print("true")
                        break
                return True
            elif self.color == "Black" and (avLocation == [self.location[0] - 1, self.location[1] - 1] or avLocation == [self.location[0] + 1, self.location[1] - 1]):
                for x in range(8):
                    if [x, 0] == avLocation:
                        self.promotion = True
                        break
                return True
            self.promotion = False

class Rook(Piece):
    def __init__(self, screen, color, location, locationGUI, board, SQUARE):
        self.name = "Rook"
        image = color + "_" + self.name + ".png"
        self.value = 5
        if color == "White":
            board.player1Score += self.value
            board.player1Pieces.append(self)
        else:
            board.player2Score += self.value
            board.player2Pieces.append(self)

        super().__init__(screen, color, location, locationGUI, image, board, SQUARE)

    def Die(self):
            self.board.UpdateScore(self.value, self.color)
            self.alive = False
            self.board.squares[self.location[0]][self.location[1]][1] = None

    def isAvailable(self, avLocation):
        for i in range(8):
            if self.location[1] + i < len(self.board.squares[0]) and i > 0:
                if self.board.squares[self.location[0]][self.location[1] + i][1] != None:
                    if self.board.squares[self.location[0]][self.location[1] + i][1].color == self.color:
                        break
                if (self.location[0], self.location[1] + i) == (avLocation[0], avLocation[1]):
                    return True
        for i in range(8):
            if self.location[1] - i >= 0 and i > 0:
                if self.board.squares[self.location[0]][self.location[1] - i][1] != None:
                    if self.board.squares[self.location[0]][self.location[1] - i][1].color == self.color:
                        break
                if (self.location[0], self.location[1] - i) == (avLocation[0],avLocation[1]):
                    return True
        for i in range(8):
            if self.location[0] + i < len(self.board.squares) and i > 0:
                if self.board.squares[self.location[0] + i][self.location[1]][1] != None:
                    if self.board.squares[self.location[0] + i][self.location[1]][1].color == self.color: 
                        break
                if (self.location[0] + i, self.location[1]) == (avLocation[0], avLocation[1]):
                    return True
        for i in range(8):
            if self.location[0] - i >= 0 and i > 0:
                if self.board.squares[self.location[0] - i][self.location[1]][1] != None:
                    if self.board.squares[self.location[0] - i][self.location[1]][1].color == self.color:
                        break
                if (self.location[0] - i, self.location[1]) == (avLocation[0],avLocation[1]):
                    return True

class Knight(Piece):
    def __init__(self, screen, color, location, locationGUI, board, SQUARE):
        self.name = "Knight"
        image = color + "_" + self.name + ".png"
        self.value = 3
        if color == "White":
            board.player1Score += self.value
            board.player1Pieces.append(self)
        else:
            board.player2Score += self.value
            board.player2Pieces.append(self)

        super().__init__(screen, color, location, locationGUI, image, board, SQUARE)

    def Die(self):
            self.board.UpdateScore(self.value, self.color)
            self.alive = False
            self.board.squares[self.location[0]][self.location[1]][1] = None
            
    def isAvailable(self, avLocation):
        if self.board.squares[avLocation[0]][avLocation[1]][1] == None or self.board.squares[avLocation[0]][avLocation[1]][1].color == self.OppositeColor():
            if avLocation == [self.location[0] + 1, self.location[1] + 2]:
                return True
            elif avLocation == [self.location[0] + 2, self.location[1] + 1]:
                return True
            elif avLocation == [self.location[0] + 2, self.location[1] - 1]:
                return True
            elif avLocation == [self.location[0] + 1, self.location[1] - 2]:
                return True
            elif avLocation == [self.location[0] - 1, self.location[1] - 2]:
                return True 
            elif avLocation == [self.location[0] - 2, self.location[1] - 1]:
                return True
            elif avLocation == [self.location[0] - 2, self.location[1] + 1]:
                return True
            elif avLocation == [self.location[0] - 1, self.location[1] + 2]:
                return True                       
        

class Bishop(Piece):
    def __init__(self, screen, color, location, locationGUI, board, SQUARE):
        self.name = "Bishop"
        image = color + "_" + self.name + ".png"
        self.value = 3
        if color == "White":
            board.player1Score += self.value
            board.player1Pieces.append(self)
        else:
            board.player2Score += self.value
            board.player2Pieces.append(self)

        super().__init__(screen, color, location, locationGUI, image, board, SQUARE)

    def Die(self):
            self.board.UpdateScore(self.value, self.color)
            self.alive = False
            self.board.squares[self.location[0]][self.location[1]][1] = None

    def isAvailable(self, avLocation):
        for i in range(8):
            if self.location[0] + i < len(self.board.squares) and self.location[1] + i < len(self.board.squares[0]) and i > 0:
                if self.board.squares[self.location[0] + i][self.location[1] + i][1] != None:
                    if self.board.squares[self.location[0] + i][self.location[1] + i][1].color == self.color:
                        break
                if (self.location[0] + i, self.location[1] + i) == (avLocation[0], avLocation[1]):
                    return True
        for i in range(8):
            if self.location[0] - i >= 0 and self.location[1] - i >= 0 and i > 0:
                if self.board.squares[self.location[0] - i][self.location[1] - i][1] != None:
                    if self.board.squares[self.location[0] - i][self.location[1] - i][1].color == self.color:
                        break
                if (self.location[0] - i, self.location[1] - i) == (avLocation[0],avLocation[1]):
                    return True
        for i in range(8):
            if self.location[0] + i < len(self.board.squares) and self.location[1] - i >= 0 and i > 0:
                if self.board.squares[self.location[0] + i][self.location[1] - i][1] != None:
                    if self.board.squares[self.location[0] + i][self.location[1] - i][1].color == self.color: 
                        break
                if (self.location[0] + i, self.location[1] - i) == (avLocation[0], avLocation[1]):
                    return True
        for i in range(8):
            if self.location[0] - i >= 0 and self.location[1] + i < len(self.board.squares[0]) and i > 0:
                if self.board.squares[self.location[0] - i][self.location[1] + i][1] != None:
                    if self.board.squares[self.location[0] - i][self.location[1] + i][1].color == self.color:
                        break
                if (self.location[0] - i, self.location[1] + i) == (avLocation[0],avLocation[1]):
                    return True

class King(Piece):
    def __init__(self, screen, color, location, locationGUI, board, SQUARE):
        self.name = "King"
        image = color + "_" + self.name + ".png"
        self.value = 3
        if color == "White":
            board.player1Score += self.value
            board.player1Pieces.append(self)
        else:
            board.player2Score += self.value
            board.player2Pieces.append(self)

        super().__init__(screen, color, location, locationGUI, image, board, SQUARE)

    def Die(self):
            self.board.UpdateScore(self.value, self.color)
            self.alive = False
            self.board.squares[self.location[0]][self.location[1]][1] = None
    
    def isAvailable(self, avLocation):
        for i in range(2):
            if self.location[1] + i < len(self.board.squares[0]) and i > 0:
                if self.board.squares[self.location[0]][self.location[1] + i][1] != None:
                    if self.board.squares[self.location[0]][self.location[1] + i][1].color == self.color:
                        break
                if (self.location[0], self.location[1] + i) == (avLocation[0], avLocation[1]):
                    return True
        for i in range(2):
            if self.location[1] - i >= 0 and i > 0:
                if self.board.squares[self.location[0]][self.location[1] - i][1] != None:
                    if self.board.squares[self.location[0]][self.location[1] - i][1].color == self.color:
                        break
                if (self.location[0], self.location[1] - i) == (avLocation[0],avLocation[1]):
                    return True
        for i in range(2):
            if self.location[0] + i < len(self.board.squares) and i > 0:
                if self.board.squares[self.location[0] + i][self.location[1]][1] != None:
                    if self.board.squares[self.location[0] + i][self.location[1]][1].color == self.color: 
                        break
                if (self.location[0] + i, self.location[1]) == (avLocation[0], avLocation[1]):
                    return True
        for i in range(2):
            if self.location[0] - i >= 0 and i > 0:
                if self.board.squares[self.location[0] - i][self.location[1]][1] != None:
                    if self.board.squares[self.location[0] - i][self.location[1]][1].color == self.color:
                        break
                if (self.location[0] - i, self.location[1]) == (avLocation[0],avLocation[1]):
                    return True
        for i in range(2):
            if self.location[0] + i < len(self.board.squares) and self.location[1] + i < len(self.board.squares[0]) and i > 0:
                if self.board.squares[self.location[0] + i][self.location[1] + i][1] != None:
                    if self.board.squares[self.location[0] + i][self.location[1] + i][1].color == self.color:
                        break
                if (self.location[0] + i, self.location[1] + i) == (avLocation[0], avLocation[1]):
                    return True
        for i in range(2):
            if self.location[0] - i >= 0 and self.location[1] - i >= 0 and i > 0:
                if self.board.squares[self.location[0] - i][self.location[1] - i][1] != None:
                    if self.board.squares[self.location[0] - i][self.location[1] - i][1].color == self.color:
                        break
                if (self.location[0] - i, self.location[1] - i) == (avLocation[0],avLocation[1]):
                    return True
        for i in range(2):
            if self.location[0] + i < len(self.board.squares) and self.location[1] - i >= 0 and i > 0:
                if self.board.squares[self.location[0] + i][self.location[1] - i][1] != None:
                    if self.board.squares[self.location[0] + i][self.location[1] - i][1].color == self.color: 
                        break
                if (self.location[0] + i, self.location[1] - i) == (avLocation[0], avLocation[1]):
                    return True
        for i in range(2):
            if self.location[0] - i >= 0 and self.location[1] + i < len(self.board.squares[0]) and i > 0:
                if self.board.squares[self.location[0] - i][self.location[1] + i][1] != None:
                    if self.board.squares[self.location[0] - i][self.location[1] + i][1].color == self.color:
                        break
                if (self.location[0] - i, self.location[1] + i) == (avLocation[0],avLocation[1]):
                    return True

class Queen(Piece):
    def __init__(self, screen, color, location, locationGUI, board, SQUARE):
        self.name = "Queen"
        image = color + "_" + self.name + ".png"
        self.value = 9
        if color == "White":
            board.player1Score += self.value
            board.player1Pieces.append(self)
        else:
            board.player2Score += self.value
            board.player2Pieces.append(self)

        super().__init__(screen, color, location, locationGUI, image, board, SQUARE)

    def Die(self):
            self.board.UpdateScore(self.value, self.color)
            self.alive = False
            self.board.squares[self.location[0]][self.location[1]][1] = None
    
    def isAvailable(self, avLocation):
        for i in range(8):
            if self.location[1] + i < len(self.board.squares[0]) and i > 0:
                if self.board.squares[self.location[0]][self.location[1] + i][1] != None:
                    if self.board.squares[self.location[0]][self.location[1] + i][1].color == self.color:
                        break
                if (self.location[0], self.location[1] + i) == (avLocation[0], avLocation[1]):
                    return True
        for i in range(8):
            if self.location[1] - i >= 0 and i > 0:
                if self.board.squares[self.location[0]][self.location[1] - i][1] != None:
                    if self.board.squares[self.location[0]][self.location[1] - i][1].color == self.color:
                        break
                if (self.location[0], self.location[1] - i) == (avLocation[0],avLocation[1]):
                    return True
        for i in range(8):
            if self.location[0] + i < len(self.board.squares) and i > 0:
                if self.board.squares[self.location[0] + i][self.location[1]][1] != None:
                    if self.board.squares[self.location[0] + i][self.location[1]][1].color == self.color: 
                        break
                if (self.location[0] + i, self.location[1]) == (avLocation[0], avLocation[1]):
                    return True
        for i in range(8):
            if self.location[0] - i >= 0 and i > 0:
                if self.board.squares[self.location[0] - i][self.location[1]][1] != None:
                    if self.board.squares[self.location[0] - i][self.location[1]][1].color == self.color:
                        break
                if (self.location[0] - i, self.location[1]) == (avLocation[0],avLocation[1]):
                    return True
        for i in range(8):
            if self.location[0] + i < len(self.board.squares) and self.location[1] + i < len(self.board.squares[0]) and i > 0:
                if self.board.squares[self.location[0] + i][self.location[1] + i][1] != None:
                    if self.board.squares[self.location[0] + i][self.location[1] + i][1].color == self.color:
                        break
                if (self.location[0] + i, self.location[1] + i) == (avLocation[0], avLocation[1]):
                    return True
        for i in range(8):
            if self.location[0] - i >= 0 and self.location[1] - i >= 0 and i > 0:
                if self.board.squares[self.location[0] - i][self.location[1] - i][1] != None:
                    if self.board.squares[self.location[0] - i][self.location[1] - i][1].color == self.color:
                        break
                if (self.location[0] - i, self.location[1] - i) == (avLocation[0],avLocation[1]):
                    return True
        for i in range(8):
            if self.location[0] + i < len(self.board.squares) and self.location[1] - i >= 0 and i > 0:
                if self.board.squares[self.location[0] + i][self.location[1] - i][1] != None:
                    if self.board.squares[self.location[0] + i][self.location[1] - i][1].color == self.color: 
                        break
                if (self.location[0] + i, self.location[1] - i) == (avLocation[0], avLocation[1]):
                    return True
        for i in range(8):
            if self.location[0] - i >= 0 and self.location[1] + i < len(self.board.squares[0]) and i > 0:
                if self.board.squares[self.location[0] - i][self.location[1] + i][1] != None:
                    if self.board.squares[self.location[0] - i][self.location[1] + i][1].color == self.color:
                        break
                if (self.location[0] - i, self.location[1] + i) == (avLocation[0],avLocation[1]):
                    return True