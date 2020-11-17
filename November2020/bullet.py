import pygame
from math import sin, cos

width,height = 600,600
class Bullet():
    def __init__(self, x, y, heading,graphics):
        self.x = x
        self.y = y
        self.heading = heading
        self.speed = 10
        self.life = 30
        self.graphics = graphics

    def update(self):
        # Moving
        self.x += self.speed * cos(self.heading)
        self.y += self.speed * sin(self.heading)


        if self.x > width:
            self.x = 0
        elif self.x < 0:
            self.x = width
        elif self.y > height:
            self.y = 0
        elif self.y < 0:
            self.y = height
        self.life -= 1
