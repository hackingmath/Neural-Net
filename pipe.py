#Dan Shiffman
#Neuro-Evolution Flappy Bird

import random 
import pygame

GREEN = (0,255,0)
width = 600
height = 600

screen = pygame.display.set_mode((width,height))

class Pipe(object):
    def __init__(self):
        self.spacing = 125
        self.top = random.randint(height/6.0,0.75*height)
        self.bottom = height - (self.top + self.spacing)
        self.x = width
        self.w = 80 #width of pipe
        self.speed = 4


    def hits(self,bird):
        if bird.y < self.top or bird.y + bird.w > height - self.bottom:
            if  self.x < bird.x < (self.x + self.w):
                self.highlight = True
                return True
        return False

    def show(self):
        self.x -= self.speed
        pygame.draw.rect(screen, GREEN, [self.x,0,self.w,self.top])
        pygame.draw.rect(screen, GREEN, [self.x,height-self.bottom,self.w,self.bottom])

    def offscreen(self):
        return self.x < -self.w