import pygame
import numpy

class Button:
    def __init__(self, rect, t, col1, col2, fontSize):
        self.rect = rect
        self.text = t
        self.col1 = col1 #min of 20 value in all of these
        self.col2 = col2
        self.font = pygame.font.SysFont('', fontSize)
        self.font2 = pygame.font.SysFont('', fontSize+8)
    def update(self, win):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x,y):
            pygame.draw.rect(win, tuple(numpy.subtract(self.col1, (20,20,20))), self.rect)
            text = self.font2.render(self.text, True, self.col2)
        else:
            pygame.draw.rect(win, self.col1, self.rect)
            text = self.font.render(self.text, True, self.col2)
        loc = text.get_rect()
        loc.center = self.rect.center
        win.blit(text, loc)
    def clicked(self):
        x, y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(x,y):
            return True
        return False