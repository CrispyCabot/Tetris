import pygame
from pygame.locals import K_q, K_UP, K_DOWN, K_LEFT, K_RIGHT, \
                        QUIT, K_ESCAPE, K_r, K_p
import time
from config import width, height, size, columns
from shape import Shape
from random import randint

pygame.init()

win = pygame.display.set_mode((width+400, height), pygame.RESIZABLE)
pygame.display.set_caption('Tetris')

font = pygame.font.SysFont('', 36)
smallFont = pygame.font.SysFont('', 24)

clock = pygame.time.Clock()

def drawGame(shape, spots, colors, score, nextShape):
    win.fill((255,255,255))
    for i in spots:
        color = colors[spots.index(i)]
        pygame.draw.rect(win, color, pygame.Rect(i[0], i[1], size, size))
        pygame.draw.rect(win, (0,0,0), pygame.Rect(i[0], i[1], size, size), 1)
    shape.draw(win)

    #Sidebar
    pygame.draw.rect(win, (0,0,0), pygame.Rect(width, 0, 400, height))
    text = smallFont.render('Score:  ' +str(score), True, (100,255,100))
    loc = text.get_rect()
    loc.topleft = (width+20, 20)
    win.blit(text, loc)
    nextShape.draw(win)
    pygame.display.update()

def main(): #return true restarts it, return false to exit
    gameScreen = 'game'
    playing = True
    paused = False
    shape = randShape()
    nextShape = randShape()
    nextShape.side(True)

    shapeDelay = 20
    shapeDelayMax = 20

    moveDelay = 5
    moveDelayMax = 5

    score = 0
    
    spots = []
    colors = []

    tStart = time.time()
    while playing:
        if gameScreen == 'game':
            clock.tick(60)

            if paused:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return False
                    if event.type == pygame.KEYDOWN:
                        paused = False
                win.fill((0,0,0))
                text = font.render('Paused', True, (255,255,255))
                loc = text.get_rect()
                loc.center = ((width+400)/2, height/2)
                win.blit(text, loc)
                text = smallFont.render('Press any key to continue', True, (255,255,255))
                loc = text.get_rect()
                loc.center = ((width+400)/2, height/2+100)
                win.blit(text, loc)
                pygame.display.update()
            else:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return False
                    if event.type == pygame.KEYDOWN:
                        if event.key == 273 and shape.type != 'square': #Up arrow
                            shape.move('up')
                            if shape.check(spots, 'down'):
                                shape.move('up')
                                shape.move('up')
                                shape.move('up')

                if shapeDelay <= 0:
                    shape.move('down')
                    shapeDelay = shapeDelayMax
                shapeDelay -= 1
                moveDelay -= 1

                if time.time() - tStart > 3:
                    tStart = time.time()
                    shapeDelayMax -= .1

                if shape.check(spots, 'down'):
                    print(shape.spots)
                    shape.move('back')
                    appendSpots(spots, shape, colors)
                    shape = nextShape
                    nextShape = randShape()
                    nextShape.side(True)
                    shape.side(False)
                    if shape.check(spots, 'down'):
                        gameScreen = 'end'
                keys = pygame.key.get_pressed()
                if keys[K_q] or keys[K_ESCAPE]:
                    return False
                if keys[K_p]:
                    paused = True
                if keys[K_r]:
                    return True
                moved = False
                if keys[K_DOWN] and moveDelay <= 0:
                    shape.move('down')
                    moved = True
                    if shape.check(spots, 'down'):
                        shape.move('back')
                        appendSpots(spots, shape, colors)
                        shape = nextShape
                        shape.side(False)
                        nextShape = randShape()
                        nextShape.side(True)
                        if shape.check(spots, 'down'):
                            gameScreen = 'end'
                if keys[K_LEFT] and moveDelay <= 0: #left
                    if not shape.check(spots, 'left'):
                        shape.move('left')
                        moved = True
                if keys[K_RIGHT] and moveDelay <= 0: #right
                    if not shape.check(spots, 'right'):
                        shape.move('right')
                        moved = True
                if moved:
                    moveDelay = moveDelayMax

                #Remove the full rows
                yVals = []
                for i in spots:
                    yVals.append(i[1])
                yUnique = list(dict.fromkeys(yVals))
                removes = []
                for i in yUnique:
                    if yVals.count(i) >= columns:
                        removes.append(i)
                removeAmt = len(removes)
                score += removeAmt*removeAmt
                for i in removes:
                    end = len(spots)
                    x = 0
                    while x < end:
                        y = spots[x][1]
                        if y == i:
                            spots.pop(x)
                            colors.pop(x)
                            end -= 1
                        else:
                            x += 1
                #move everything down
                for x in removes:
                    for i in spots:
                        if i[1] < x:
                            i[1] += size*removeAmt
                drawGame(shape, spots, colors, score, nextShape)
        elif gameScreen == 'end':
            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
            clock.tick(30)
            text = font.render('Game Over', True, (255,0,0), (0,0,0))
            drawEnd()
            keys = pygame.key.get_pressed()
            if keys[K_r]:
                gameScreen = 'game'
                return True
            if keys[K_q] or keys[K_ESCAPE]:
                return False

def drawEnd():
    text = font.render("Game Over", True, (255,0,0), (0,0,0))
    loc = text.get_rect()
    loc.center = (width/2, height/2)
    win.blit(text, loc)
    pygame.display.update()

def appendSpots(spots, shape, colors):
    for i in shape.spots:
        spots.append([int(i[0]), int(i[1])])
        colors.append(shape.col)

def randShape():
    types = ['L', 'long', 'backL', 'Z', 'backZ', 'square', 'T']
  #  return Shape('long')
    return Shape(types[randint(0,len(types)-1)])

while main():
    main()