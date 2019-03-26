import pygame
from pygame.locals import K_q, K_UP, K_DOWN, K_LEFT, K_RIGHT, \
                        QUIT
import time
from config import width, height, size
from shape import Shape
from random import randint

pygame.init()

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tetris')

clock = pygame.time.Clock()

def redraw(shape, spots):
    win.fill((255,255,255))
    for i in spots:
        pygame.draw.rect(win, (255,0,0), pygame.Rect(i[0], i[1], size, size))
        pygame.draw.rect(win, (0,0,0), pygame.Rect(i[0], i[1], size, size), 1)
    shape.draw(win)
    pygame.display.update()
def main():
    playing = True
    shape = Shape('L')

    delay = 5
    delayMax = 2

    tickRate = 10
    
    spots = []

    tStart = time.time()
    while playing:
        clock.tick(tickRate)

        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == 273: #Up arrow
                    shape.move('up')
                '''
                if event.key == 276: #left
                    if not shape.check(spots, 'left'):
                        shape.move('left')
                if event.key == 275: #right
                    if not shape.check(spots, 'right'):
                        shape.move('right')
                '''

        if delay <= 0:
            shape.move('down')
            delay = delayMax
        delay -= 1

        if time.time() - tStart > 5:
            tickRate += 1
            tStart = time.time()
        if shape.check(spots, 'down'):
            for i in shape.spots:
                spots.append(i)
            shape = randShape()
        keys = pygame.key.get_pressed()
        if keys[K_q]:
            playing = False
        if keys[K_DOWN]:
            shape.move('down')
        if keys[K_LEFT]: #left
            if not shape.check(spots, 'left'):
                shape.move('left')
        if keys[K_RIGHT]: #right
            if not shape.check(spots, 'right'):
                shape.move('right')

        redraw(shape, spots)
    pygame.quit()

def randShape():
    types = ['L', 'long', 'backL']
    return Shape(types[randint(0,len(types)-1)])

main()