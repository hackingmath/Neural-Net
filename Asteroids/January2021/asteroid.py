import pygame
import polar_cartesian as pc
from random import randint, uniform
from math import sin,cos,pi
import numpy as np

width,height = 600,600


def standard_form(v1, v2):
    x1, y1 = v1
    x2, y2 = v2
    a = y2 - y1
    b = x1 - x2
    c = x1 * y2 - y1 * x2
    return a, b, c


def intersection(u1, u2, v1, v2):
    a1, b1, c1 = standard_form(u1, u2)
    a2, b2, c2 = standard_form(v1, v2)
    m = np.array(((a1, b1), (a2, b2)))
    c = np.array((c1, c2))
    return np.linalg.solve(m, c)


def length_segment(s):
    a, b = s[0], s[1]
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)**0.5


def distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)**0.5


def do_segments_intersect(s1, s2):
    u1, u2 = s1
    v1, v2 = s2
    #print(s1, s2)
    d1, d2 = length_segment(s1), length_segment(s2)
    try:
        x, y = intersection(u1, u2, v1, v2)
        #print("intersection:", d1, d2, x, y)
        if (distance(u1, (x, y)) <= d1 and
                distance(u2, (x, y)) <= d1 and
                distance(v1, (x, y)) <= d2 and
                distance(v2, (x, y)) <= d2):
            #print("dist_s1_intn", s1, (x, y))
            return distance(s1[0], (x, y))
    except np.linalg.linalg.LinAlgError:
        return False

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
                try:
                    asteroids.remove(self)
                except ValueError:
                    pass
                bullets.remove(b)
                self.level += 1
                if self.level in [2,3]:
                    for i in range(2):
                        new_a = Asteroid(self.size/2)
                        new_a.x,new_a.y = self.x,self.y
                        new_a.level = self.level
                        asteroids.append(new_a)

    def does_intersect(self,other_segment):
        point_count = len(self.points)
        segments = [(self.points[i], self.points[(i + 1) % point_count])
                    for i in range(point_count)]
        for segment in segments:
            return do_segments_intersect(other_segment, segment)

