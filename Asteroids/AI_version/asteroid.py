import pygame
import polar_cartesian as pc
from random import randint, uniform
from math import sin,cos,pi

width,height = 600,600

class Asteroid():
    def __init__(self,size = 50):

        self.x,self.y = randint(0,width),randint(0,height)
        self.size = size
        self.level = 1
        self.sides = randint(6,9)
        self.heading = uniform(0.0,2*pi)
        self.points = [pc.to_cartesian((uniform(0.5*self.size,
                                             1.0*self.size),
                                     2*pi*i/self.sides)) \
                       for i in range(self.sides)]
        self.screen_points = [[self.x + pt[0],
                               self.y+pt[1]]
                              for pt in self.points]

    def move(self):
        self.x += 0.5*cos(self.heading)
        self.y += 0.5*sin(self.heading)
        #wrap
        if self.y < 0:
            self.y = height
        if self.x < 0:
            self.x = width
        if self.y > height:
            self.y = 0
        if self.x > width:
            self.x = 0

        self.screen_points = [[int(self.x + pt[0]), int(self.y + pt[1])] for pt in self.points]

    def check_bullets(self,ship,asteroids,bullets):
        for b in bullets:
            if pc.distance(self,b) < self.size:
                if self.level == 1:
                    ship.score += 20
                elif self.level == 2:
                    ship.score += 50
                elif self.level == 3:
                    ship.score += 100
                #print("Score:", ship.score)
                asteroids.remove(self)
                bullets.remove(b)
                self.level += 1
                if self.level in [2,3]:
                    for i in range(2):
                        new_a = Asteroid(self.size/2)
                        new_a.x,new_a.y = self.x,self.y
                        new_a.level = self.level
                        asteroids.append(new_a)


