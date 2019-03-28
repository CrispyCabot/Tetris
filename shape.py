from config import width, height, size
import pygame
import math
from random import randint

middle = width/2
class Shape:
    def __init__(self, typ):
        self.type = typ
        self.spots = []
        self.col = (0,0,0)
        if self.type == 'long':
            self.col = (255,255,0)
            self.spots = [
                        [middle-size,0],
                        [middle-size,size],
                        [middle-size,size*2],
                        [middle-size,size*3]
            ]
        if self.type == 'L':
            self.col = (0,0,255)
            self.spots = [
                        [middle-size, 0],
                        [middle-size, size],
                        [middle-size, size*2],
                        [middle, size*2]
            ]
        if self.type == 'backL':
            self.col = (255,0,0)
            self.spots = [
                        [middle-size, 0],
                        [middle-size, size],
                        [middle-size, size*2],
                        [middle-size*2, size*2]
            ]
        if self.type == 'square':
            self.col = (100,200,255)
            self.spots = [
                        [middle-size, 0],
                        [middle-size, size],
                        [middle, 0],
                        [middle, size]
            ]
        if self.type == 'Z':
            self.col = (255,0,255)
            self.spots = [
                        [middle-size*2, 0],
                        [middle-size, 0],
                        [middle-size, size],
                        [middle, size]
            ]
        if self.type == 'backZ':
            self.col = (100,220,85)
            self.spots = [
                        [middle, 0],
                        [middle-size, 0],
                        [middle-size, size],
                        [middle-size*2, size]
            ]
        if self.type == 'T':
            self.col = (100,100,100)
            self.spots = [
                        [middle-size*2, 0],
                        [middle-size, 0],
                        [middle, 0],
                        [middle-size, size]
            ]
    def draw(self, win):
        for i in self.spots:
            pygame.draw.rect(win, self.col, pygame.Rect(i[0], i[1], size, size))
            pygame.draw.rect(win, (0,0,0), pygame.Rect(i[0], i[1], size, size), 1)

    def side(self, val):
        if val:
            for i in self.spots:
                i[0] += width/2+size*3
                i[1] += height/3
        else:
            for i in self.spots:
                i[0] -= width/2+size*3
                i[1] -= height/3
                i[0] = int(i[0])
                i[1] = int(i[1])
    def check(self, spots, dir):
        for i in self.spots:
            if dir == 'down': #checks if it is currently hit, not future
                if i[1] >= height:
                    return True
                if [i[0], i[1]] in spots:
                    return True
                #x check
                if i[0] >= width or i[0] < 0:
                    return True
            if dir == 'left':
                if i[0]-size < 0:
                    return True
                if [i[0]-size, i[1]] in spots:
                    return True
            if dir == 'right':
                if i[0]+size >= width:
                    return True
                if [i[0]+size, i[1]] in spots:
                    return True
        return False

    def move(self, dir):
        if dir == 'right':
            for i in self.spots:
                i[0] += size
        if dir == 'left':
            for i in self.spots:
                i[0] -= size
        if dir == 'up':
            mid = int(len(self.spots)/2)
            mid = self.spots[mid]
            for i in self.spots:
                i[0], i[1] = rotate((mid[0], mid[1]), (i[0], i[1]), math.pi/2)
        if dir == 'down':
            for i in self.spots:
                i[1] += size
        if dir == 'back':
            for i in self.spots:
                i[1] -= size

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy