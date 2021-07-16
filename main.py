import pygame
from board import Board

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

SQUARE = SCREEN_WIDTH/8

PLAYER_COLOR_1 = (238,238,210)
PLAYER_COLOR_2 = (118,150,86)

player1 = "White"
player2 = "Black"

def main():
    board = Board()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Chess by FlubOtic")
    screen.fill(PLAYER_COLOR_1)

    gameWon = False
    gameRunning = True
    
    board.drawSquares(screen, PLAYER_COLOR_1, PLAYER_COLOR_2, SQUARE, SCREEN_HEIGHT)
    board.spawnPieces(screen)

    while gameRunning == True:
        pygame.display.update()

        pygame.init()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
                pygame.quit()
                break
            elif event.type == pygame.MOUSEBUTTONUP:
                print("fff")
                if not board.selected:
                    board.selectPiece(pygame.mouse.get_pos())
                else:
                    board.Move(pygame.mouse.get_pos())

        screen.fill((255,255,255))
        
        board.drawSquares(screen, PLAYER_COLOR_1, PLAYER_COLOR_2, SQUARE, SCREEN_HEIGHT)
        board.drawPieces(screen)
        

if __name__ == "__main__":
    main()

