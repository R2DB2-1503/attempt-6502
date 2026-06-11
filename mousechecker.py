import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1800, 1000))
pygame.display.set_caption("mousecheck")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Cascadia Code", 24)
WHITE = (255, 255, 255)
GRAY = (64, 64, 64)
GREEN = (127, 255, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(GRAY)

    x, y = pygame.mouse.get_pos()
    text_string = f"X: {x}, Y: {y}"
    text_surface = font.render(text_string, True, GREEN)

    screen.blit(text_surface, (20, 20))
    for i in range (0,(18)+2):
        pygame.draw.line(screen, WHITE, (0,i*100), (1800,i*100), width=1)
        pygame.draw.line(screen, WHITE, (i*100,0), (i*100,1000), width=1)
    pygame.draw.line(screen, WHITE, (1799,0), (1799,999), width=1)
    pygame.display.flip()
    
    clock.tick(60)
