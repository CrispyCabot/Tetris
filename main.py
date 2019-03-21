import pygame
from pygame.locals import K_q, K_UP, K_DOWN, K_LEFT, K_RIGHT, \
                        QUIT
import time

pygame.init()

width = 400
height = 700

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tetris')

clock = pygame.time.Clock()

def redraw():
    win.fill((255,255,255))
    pygame.display.update()
def main():
    playing = True

    while playing:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
        keys = pygame.key.get_pressed()
        if keys[K_q]:
            playing = False

        redraw()
    
    pygame.quit()

main()