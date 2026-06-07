import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1600, 700))
pygame.display.set_caption("Mouse Position Tracker")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Cascadia Code", 24)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    x, y = pygame.mouse.get_pos()
    text_string = f"Mouse Position: X: {x}, Y: {y}"
    text_surface = font.render(text_string, True, GREEN)

    screen.blit(text_surface, (20, 20))

    pygame.display.flip()
    
    clock.tick(60)
