from config import width, height
import pygame
middle = width/2
class Shape:
    def __init__(self, typ):
        self.type = typ
        self.spots = []
        if self.type == 'long':
            self.spots = [
                        [middle-10,0],
                        [middle-10,10],
                        [middle-10,20],
                        [middle-10,30]
            ]
    def update(self, win):
        for i in self.spots:
            pygame.draw.rect(win, (255,0,0), pygame.Rect(i[0], i[1], 10, 10))
            pygame.draw.rect(win, (0,0,0), pygame.Rect(i[0], i[1], 10, 10), 1)
            i[1] += 2

    def check(self, spots):
        for i in self.spots:
            if i[1]+10 > height:
                return True
            if i in spots:
                return True

    def move(self, dir):
        if dir == 'right':
            for i in self.spots:
                i[0] += 10
        if dir == 'left':
            for i in self.spots:
                i[0] -= 10
        if dir == 'up':
            mid = int(len(self.spots)/2)
            mid = self.spots[mid]
            for i in self.spots:
                if i[0] != mid[0]:
                    i[0] = mid[0]
                if i[1] != mid[1]:
                    i[1] = mid[1]