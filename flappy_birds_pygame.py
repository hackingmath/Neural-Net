#Dan Shiffman
#Neuro-Evolution Flappy Bird

import pygame
from pygame.locals import *
import numpy
import time
from pipe import Pipe
from bird import Bird
import ga
import random

NUM_BIRDS = 500

pipes = []
birds = []
savedBirds = []
bestBirds = []
bestBird = None
generation = 0
counter = 0
bestScore = 0

width = 600
height = 600

#define constants
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
CYAN = (0,255,255)
VIOLET = (148,0,211)

def restart():
    global pipes,birds,generation,savedBirds
    pipes = [Pipe()]
    '''
    #All this code has been superceded by the GA module
    birds = bestBirds[::]
    savedBirds.sort(key=Bird.get_score)
    l = len(savedBirds)
    if l > 10:
        for i in range(1,10):
            newBird = savedBirds[-i] #highest score
            for i in range(int(NUM_BIRDS/4.0)):
                mutant = Bird(newBird.brain)
                mutant.brain.mutate(0.1)
                birds.append(mutant)

    for bird in savedBirds:
        newBird = bird
        for i in range(int(NUM_BIRDS / 4.0)):
            mutant = Bird(newBird.brain)
            mutant.brain.mutate(0.1)
            birds.append(mutant)

    for i in range(int(NUM_BIRDS)):
        birds.append(Bird())

    savedBirds = []
    if len(birds) > NUM_BIRDS:
        birds = birds[:NUM_BIRDS]'''
    ga.nextGeneration(NUM_BIRDS,savedBirds,birds)
    savedBirds = []
    generation += 1
    time.sleep(1)

size = (width,height)
for i in range(int(NUM_BIRDS/4)):
    birds.append(Bird())

#set up display
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 24)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Flappy Birds!')
FPS = 60 #frames per second
clock = pygame.time.Clock()

counter = 0

#loop until user clicks the close button
done = False

while not done:
    for event in pygame.event.get():
        if event.type == QUIT: #if pygame window is closed by user
            done = True
        if event.type == KEYDOWN:
            if event.key == K_SPACE: bird.up()

    #fill the screen with background color
    screen.fill(BLACK)
    #print("birds:",len(birds))
    counter += 1

    if not pipes:
        pipes.append(Pipe())
    if not birds:
        restart()
    for bird in birds:
        bird.think(pipes)
        if bird.score > bestScore:
            bestScore = bird.score
            bestBird = bird
            #bestBirds.append(bird)
            savedBirds.append(bird)
        bird.show()
        if bird.offscreen():
            savedBirds.append(bird)
            birds.remove(bird)

    for pipe in pipes:
        pipe.show()
        if not birds:
            restart()
        for b in birds:
            if pipe.hits(b):
                savedBirds.append(b)
                birds.remove(b)


        if pipe.offscreen():
            pipes.remove(pipe)
        '''if len(pipes) == 1 and pipe.x < width/2:
            pipes.append(Pipe())'''

    generation_surface = myfont.render('Generation: '+str(generation), False, (255,0,0))
    score_surface = myfont.render('Fitness: '+str(bestScore), False, (255, 0, 0))
    num_surface = myfont.render('Birds: ' + str(len(birds)), False, (255, 0, 0))
    print("saved:",len(savedBirds))
    '''if birds:
        print("inputs: ",birds[0].x - pipes[0].x)'''
    screen.blit(generation_surface, (400, 0))
    screen.blit(score_surface, (400, 30))
    screen.blit(num_surface, (400, 60))
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
    