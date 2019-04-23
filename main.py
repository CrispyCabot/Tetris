import pygame
import os
from pygame.locals import K_q, K_UP, K_DOWN, K_LEFT, K_RIGHT, \
                        QUIT, K_ESCAPE, K_r, K_p, K_w, K_a, K_s, K_d
import time
from config import width, height, size, columns, PATH
from shape import Shape
from random import randint
from button import Button

pygame.init()

win = pygame.display.set_mode((width+400, height), pygame.RESIZABLE)
pygame.display.set_caption('Tetris')

font = pygame.font.SysFont('', 36)
smallFont = pygame.font.SysFont('', 24)
bigFont = pygame.font.SysFont('', 66)

logo = pygame.image.load(PATH+os.path.join('data', 'logo.png'))

clock = pygame.time.Clock()

settings = {
        'randColor': False,
        'randShape': False,
        'screenSize': '',
        'maxSize': 10
    }

screenOptions = {
        'small': False,
        'medium': True,
        'large': False
}

def main(): #return true restarts it, return false to exit
    global settings, width, height, size, win
    gameScreen = 'home'
    playing = True
    paused = False
    shape = randShape()
    nextShape = randShape(settings)
    nextShape.side(True)

    settings['screenSize'] = getScreenSize()

    shapeDelay = 20
    shapeDelayMax = 20

    moveDelay = 5
    moveDelayMax = 5

    score = 0
    
    spots = []
    colors = []

    homeButtons = []
    loc = pygame.Rect(10,10,200,100)
    loc.center = ((width+400)/2, height/2-75)
    homeButtons.append(Button(loc, 'Play', (255,20,20), (255,255,255), 64))
    loc = pygame.Rect(10,10,200,50)
    loc.center = ((width+400)/2, height/2)
    homeButtons.append(Button(loc, 'Settings', (150,150,150), (255,255,255), 26))
    loc = pygame.Rect(10,10,100,50)
    loc.bottomleft = (0,height)
    homeButtons.append(Button(loc, 'Quit', (255,100,100), (255,255,255), 24))

    gameOverButtons = []
    loc = pygame.Rect(10,10,200,100)
    loc.center = ((width+400)/2, height/2-75)
    gameOverButtons.append(Button(loc, 'Home', (255,20,20), (255,255,255), 64))
    loc = pygame.Rect(10,10,200,50)
    loc.center = ((width+400)/2, height/2)
    gameOverButtons.append(Button(loc, 'Settings', (150,150,150), (255,255,255), 26))
    loc = pygame.Rect(10,10,100,50)
    loc.bottomleft = (0,height)
    gameOverButtons.append(Button(loc, 'Quit', (255,100,100), (255,255,255), 24))

    settingsBtns = []
    loc = pygame.Rect(10,10,200,100)
    loc.center = ((width+400)/2, 100)
    settingsBtns.append(Button(loc, 'Random Colors', (255,20,20), (0,0,0), 26))
    loc = pygame.Rect(10,10,100,50)
    loc.bottomleft = (0,height)
    settingsBtns.append(Button(loc, 'Back', (255,200,100), (0,0,0), 20))
    loc = pygame.Rect(10,10,200,100)
    loc.center = ((width+400)/2, 200)
    settingsBtns.append(Button(loc, 'Crazy Shapes', (255,20,20), (0,0,0), 26))
    loc = pygame.Rect(10,10,200,100)
    loc.center = ((width+400)/2, 300)
    settingsBtns.append(Button(loc, 'Max Shape Size: '+str(settings['maxSize']), (100,100,255), (255,255,255), 22))
    loc = pygame.Rect(10,10,200,100)
    loc.center == ((width+400)/2, 400)
    #settingsBtns.append(Button(loc, 'Screen Size: '+settings['screenSize'], (100,100,100), (0,0,0), 26))
    if settings['randShape']:
        settingsBtns[2].col1 = (20,255,20)
    if settings['randColor']:
        settingsBtns[0].col1 = (20,255,20)

    clickDelay = 0

    backScreen = 'home'

    tStart = time.time()
    while playing:
        clickDelay += 1
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
                        if (event.key == 273 or event.key == 119) and shape.type != 'square': #Up arrow
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
                    shape.move('back')
                    appendSpots(spots, shape, colors)
                    shape = nextShape
                    nextShape = randShape(settings)
                    nextShape.side(True)
                    shape.side(False)
                    if shape.check(spots, 'down'):
                        gameScreen = 'gameOver'
                keys = pygame.key.get_pressed()
                if keys[K_q] or keys[K_ESCAPE]:
                    return False
                if keys[K_p]:
                    paused = True
                if keys[K_r]:
                    return True
                moved = False
                if (keys[K_DOWN] or keys[K_s]) and moveDelay <= 0:
                    shape.move('down')
                    moved = True
                    if shape.check(spots, 'down'):
                        shape.move('back')
                        appendSpots(spots, shape, colors)
                        shape = nextShape
                        shape.side(False)
                        nextShape = randShape(settings)
                        nextShape.side(True)
                        if shape.check(spots, 'down'):
                            gameScreen = 'gameOver'
                if (keys[K_LEFT] or keys[K_a]) and moveDelay <= 0: #left
                    if not shape.check(spots, 'left'):
                        shape.move('left')
                        moved = True
                if (keys[K_RIGHT] or keys[K_d]) and moveDelay <= 0: #right
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
                removes.sort()
                for x in removes:
                    for i in spots:
                        if i[1] < x:
                            i[1] += size
                drawGame(settings, shape, spots, colors, score, nextShape)
        elif gameScreen == 'home':
            drawBackground()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
            clock.tick(30)
            loc = logo.get_rect()
            loc.center = ((width+400)/2, height/2-200)
            win.blit(logo, loc)
            for i in homeButtons:
                i.update(win)
            if homeButtons[0].clicked() and clickDelay > 10: #play
                clickDelay = 0
                gameScreen = 'game'
            if homeButtons[1].clicked() and clickDelay > 10: #settings
                gameScreen = 'settings'
                backScreen = 'home'
                clickDelay = 0
            if homeButtons[2].clicked() and clickDelay > 10: #quit
                return False
            pygame.display.update()
        elif gameScreen == 'gameOver':
            drawBackground()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
            clock.tick(30)
            text = bigFont.render('Game Over', True, (255,0,0))
            loc = text.get_rect()
            loc.center = ((width+400)/2, height/2-175)
            win.blit(text, loc)
            text = bigFont.render('Score: '+str(score), True, (0,255,0))
            loc = text.get_rect()
            loc.center = ((width+400)/2, height/2+100)
            win.blit(text, loc)
            for i in gameOverButtons:
                i.update(win)
            pygame.display.update()
            if gameOverButtons[0].clicked() and clickDelay > 10: #play
                return True
            if gameOverButtons[1].clicked() and clickDelay > 10: #settings
                gameScreen = 'settings'
                backScreen = 'gameOver'
                clickDelay = 0
            if gameOverButtons[2].clicked() and clickDelay > 10: #quit
                return False
        elif gameScreen == 'settings':
            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
            clock.tick(30)
            drawBackground()
            for i in settingsBtns:
                i.update(win)
            if settingsBtns[0].clicked() and clickDelay > 10: #rand color
                clickDelay = 0
                settings['randColor'] = not(settings['randColor'])
                if settings['randColor']:
                    settingsBtns[0].col1 = (20,255,20)
                else:
                    settingsBtns[0].col1 = (255,20,20)
            if settingsBtns[1].clicked() and clickDelay > 10: #back
                gameScreen = backScreen
                clickDelay = 0
            if settingsBtns[2].clicked() and clickDelay > 10: #rand shape
                clickDelay = 0
                settings['randShape'] = not(settings['randShape'])
                shape = randShape(settings)
                if settings['randShape']:
                    settingsBtns[2].col1 = (20,255,20)
                else:
                    settingsBtns[2].col1 = (255,20,20)
            if settingsBtns[3].clicked() and clickDelay > 10: #max shape size
                clickDelay = 0
                settings['maxSize'] += 1
                if settings['maxSize'] > 15:
                    settings['maxSize'] = 4
                settingsBtns[3].text = 'Max Shape Size: '+str(settings['maxSize'])
            pygame.display.update()

def getScreenSize():
    for i, value in screenOptions.items():
        if value:
            return i
bgCounter = 0
def drawBackground():
    global bgCounter
    bgCounter += 1
    if bgCounter > 1:
        bgCounter = 0
        for x in range(0,height,20):
            for i in range(0,width+400,20):
                pygame.draw.rect(win, (randint(0,50), randint(0,50), randint(0,255)), pygame.Rect(i, x, 20,20))

def drawEnd():
    text = font.render("Game Over", True, (255,0,0), (0,0,0))
    loc = text.get_rect()
    loc.center = (width/2, height/2)
    win.blit(text, loc)
    pygame.display.update()

def drawGame(settings, shape, spots, colors, score, nextShape):
    win.fill((255,255,255))
    if settings['randColor']:
        for i in spots:
            color = (randint(0,255), randint(0,255), randint(0,255))
            pygame.draw.rect(win, color, pygame.Rect(i[0], i[1], size, size))
            pygame.draw.rect(win, (0,0,0), pygame.Rect(i[0], i[1], size, size), 1)
        shape.col = (randint(0,255), randint(0,255), randint(0,255))
        nextShape.col = (randint(0,255), randint(0,255), randint(0,255))
        shape.draw(win)
    else:
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

def appendSpots(spots, shape, colors):
    for i in shape.spots:
        spots.append([int(i[0]), int(i[1])])
        colors.append(shape.col)

def randShape(sets={}):
    types = ['L', 'long', 'backL', 'Z', 'backZ', 'square', 'T']
    try:
        if sets['randShape']:
            return Shape('rand', sets)
    except:
        print('error in rand shape')
    return Shape(types[randint(0,len(types)-1)], sets)

while main():
    main()