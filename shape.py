from config import width, height, size
import pygame
import math

middle = width/2
class Shape:
    def __init__(self, typ):
        self.type = typ
        self.spots = []
        if self.type == 'long':
            self.spots = [
                        [middle-size,0],
                        [middle-size,size],
                        [middle-size,size*2],
                        [middle-size,size*3]
            ]
        if self.type == 'L':
            self.spots = [
                        [middle-size, 0],
                        [middle-size, size],
                        [middle-size, size*2],
                        [middle, size*2]
            ]
        if self.type == 'backL':
            self.spots = [
                        [middle-size, 0],
                        [middle-size, size],
                        [middle-size, size*2],
                        [middle-size*2, size*2]
            ]
    def draw(self, win):
        for i in self.spots:
            pygame.draw.rect(win, (255,0,0), pygame.Rect(i[0], i[1], size, size))
            pygame.draw.rect(win, (0,0,0), pygame.Rect(i[0], i[1], size, size), 1)

    def check(self, spots, dir):
        for i in self.spots:
            if dir == 'down':
                if i[1]+size >= height:
                    return True
                if [i[0], i[1]+size] in spots:
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