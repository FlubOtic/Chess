import pygame
from board import Board
# To check if player can make a move during check, check if king is seen after the move. So check if moving a pice will block the king from being seen. If there isn't any moves then it is checkmate
def main():
    pygame.init()

    BOARD_SIZE = pygame.display.Info().current_h/1.75
    HUD_SIZE_H = BOARD_SIZE/8
    HUD_SIZE_W = BOARD_SIZE/2 - HUD_SIZE_H

    SCREEN_WIDTH = BOARD_SIZE #+ HUD_SIZE_W
    SCREEN_HEIGHT = BOARD_SIZE + HUD_SIZE_H
    SQUARE = BOARD_SIZE/8

    PLAYER_COLOR_1 = (238,238,210)
    PLAYER_COLOR_2 = (118,150,86)

    player1 = "White"
    player2 = "Black"

    screen = pygame.display.set_mode((int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))
    pygame.display.set_caption("Chess by FlubOtic")
    screen.fill(PLAYER_COLOR_1)

    board = Board(BOARD_SIZE, SQUARE, screen)

    gameWon = False
    gameRunning = True
    
    board.DrawSquares(PLAYER_COLOR_1, PLAYER_COLOR_2, HUD_SIZE_H, SCREEN_HEIGHT)
    board.SpawnPieces()

    playerTurn = player1

    while gameRunning == True:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
                pygame.quit()
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not board.selected:
                    board.SelectPiece(pygame.mouse.get_pos(), playerTurn)
                elif board.MovePiece(pygame.mouse.get_pos()): 
                        if playerTurn == player1: 
                            playerTurn = player2  
                        else: 
                            playerTurn = player1
                            

        screen.fill((142,168,111))
        
        board.DrawSquares(PLAYER_COLOR_1, PLAYER_COLOR_2, HUD_SIZE_H, SCREEN_HEIGHT)
        board.DrawPieces()
        board.DrawScore(HUD_SIZE_H)
        

if __name__ == "__main__":
    main()

