import pygame

pygame.init()

screen = pygame.display.set_mode((int(pygame.display.Info().current_h/1.6), int(pygame.display.Info().current_h/1.6)))

img = pygame.image.load(r"C:\Users\znmca\VSCode\Chess\Images\White_Pawn.png")
scale = min(screen.get_width()/2 / img.get_width(), screen.get_height()/2 / img.get_height())
img = pygame.transform.smoothscale(img, 
          (round(img.get_width() * scale), round(img.get_height() * scale))) 

rect = img.get_rect(center = screen.get_rect().center)

gameRunning = True
while gameRunning == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False

    screen.fill((127,127,127))
    screen.blit(img, rect)
    pygame.display.flip()

pygame.quit()
exit()

