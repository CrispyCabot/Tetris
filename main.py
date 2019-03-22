import pygame
from pygame.locals import K_q, K_UP, K_DOWN, K_LEFT, K_RIGHT, \
                        QUIT
import time
from config import width, height
from shape import Shape

pygame.init()

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tetris')

clock = pygame.time.Clock()

def redraw(shape, spots):
    win.fill((255,255,255))
    for i in spots:
        pygame.draw.rect(win, (255,0,0), pygame.Rect(i[0], i[1], 10, 10))
        pygame.draw.rect(win, (0,0,0), pygame.Rect(i[0], i[1], 10, 10), 1)
    shape.update(win)
    pygame.display.update()
def main():
    playing = True
    shape = Shape('long')
    
    spots = []
    while playing:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
        
        if shape.check(spots):
            for i in shape.spots:
                spots.append(i)
            shape = Shape('long')
        keys = pygame.key.get_pressed()
        if keys[K_q]:
            playing = False
        if keys[K_RIGHT]:
            shape.move('right')
        if keys[K_LEFT]:
            shape.move('left')
        if keys[K_UP]:
            shape.move('up')

        redraw(shape, spots)
    
    pygame.quit()

main()