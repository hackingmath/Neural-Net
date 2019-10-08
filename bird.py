#Shiffman
#Neuro-Evolution Flappy Bird

import pygame
#import nn_coding_train as nn
import neuralNetwork as nn
import matrix
from pipe import Pipe
import random

width,height = 600,600
YELLOW = (255,255,0)
screen = pygame.display.set_mode((width,height))

class Bird(object):
    def __init__(self,brain=None):
        self.y = height/2
        self.x = 64
        self.w = 32
        self.gravity = 0.8
        self.lift = -16
        self.velocity = 0

        self.score = 0
        self.fitness = 0
        if brain:
            self.brain = brain.copy()
        self.brain = nn.NeuralNetwork(5,6,1,0.3)
        self.inputs = [0]*5
        self.output = []

    def get_score(self):
        return self.score

    def show(self):
        self.score += 1
        self.velocity += self.gravity

        self.y += self.velocity
        if self.y > height:
            self.y = height
            self.vel = 0
            
        if self.y < 0:
            self.y = 0
            self.vel = 0
        pygame.draw.ellipse(screen, YELLOW, [self.x,self.y,self.w,self.w])

    def up(self):
        if self.velocity > 0:
            self.velocity += self.lift

    def think(self,pipes):
        global inputs
        #Find the closest pipe
        closest = pipes[0]
        closestD = closest.x + closest.w - self.x
        for pipe in pipes:
            d = pipe.x + pipe.w - self.x
            if d < closestD and d > 0:
                closest = pipe
                closestD = d

        self.inputs = [0]*5
        self.inputs[0] = self.y / height
        self.inputs[1] = closest.top / height
        self.inputs[2] = closest.bottom / height
        self.inputs[3] = closest.x / width
        self.inputs[4] = self.velocity / 10
        self.output = self.brain.query(self.inputs) #called "predict" in my DIY NN
        if self.output[0] > 0.5:#self.output.data[1]:
            self.up()

    def offscreen(self):
        return ((self.y+self.w > height) or (self.y <= 0))

    def calcFitness(self,birds):
        total = sum([bird.get_score() for bird in birds])
        self.fitness = self.get_score() / total
        

