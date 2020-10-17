import pygame
import time
from math import pi, sqrt, cos, sin, atan2
import neuralNetwork as nn
import polar_cartesian as pc

# define constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
VIOLET = (148, 0, 211)

class Ship():
    def __init__(self,size,width,height,graphics):
        self.size = size
        self.rotation_angle = 0
        self.x, self.y = width / 2, height / 2
        vertices = [(0.5,0),(-0.25,-0.25),(-0.25,0.25)]
        #convert x-y vertices to polar
        self.points = [pc.to_polar(v) for v in vertices]
        #scale up ship by self.size
        self.points = [[self.size*r,theta] for [r,theta] in self.points]
        self.color = GREEN
        self.score = 0
        self.lives = 3
        self.dpoints = [] #points for testing distance measurements
        self.create_asteroids = False
        self.graphics = graphics

    def update(self,asteroids,asteroid_count):
        for a in asteroids:
            if pc.distance(self,a) < a.size:
                self.lives -= 1
                time.sleep(2)
                self.create_asteroids = True

    def draw(self):
        #rotate vertices,convert to x-y format
        cartesian_points = [pc.to_cartesian([r,theta+self.rotation_angle]) for [r,theta] in self.points]
        self.screen_points = [[int(self.x + pt[0]),int(self.y+pt[1])] for pt in cartesian_points]



    def check_asteroids(self,x,y,asteroids):
        for a in asteroids:
            if pc.distance_pts(x, y, a.x, a.y) < a.size:

                return x,y

    def measure(self,asteroids):
        """Draw lines radiating outward to measure distances to objects"""

        self.dpoints = []
        for i in range(8):
            dist = 0
            while dist < 500:
                dist += 1
                x,y = self.x + dist*cos(self.rotation_angle + 2*pi*i/8),\
                      self.y + dist*sin(self.rotation_angle + 2*pi*i/8)
                intersect = self.check_asteroids(x,y,asteroids)
                if intersect:
                    self.dpoints.append(intersect)
                    break

    def think(self):
