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
pipeScore = 0 #how many pipes have gone by
highScore = 0

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
    global pipes,birds,generation,savedBirds,pipeScore
    pipes = [Pipe()]
    pipeScore = 0
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
    ga.nextGeneration(NUM_BIRDS, savedBirds,birds,bestBirds)

    savedBirds = []
    generation += 1
    time.sleep(1)

def Capture(display,name,pos,size): # (pygame Surface, String, tuple, tuple)
    """For saving screenshots"""
    image = pygame.Surface(size)  # Create image surface
    image.blit(display,(0,0),(pos,size))  # Blit portion of the display to the image
    pygame.image.save(image,name)  # Save the image to the disk

size = (width,height)
for i in range(int(NUM_BIRDS/4)):
    birds.append(Bird())

#set up display
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Consolas', 24)
scorefont = pygame.font.SysFont('Consolas',72)
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
            if event.key == K_SPACE:
                if FPS == 60:
                    FPS = 300 #faster for training
                else:
                    FPS = 60

    #fill the screen with background color
    screen.fill(CYAN)
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
            bestBirds.append(bird)
            bestBirds.sort(key=Bird.get_score,reverse=True)
            bestBirds = bestBirds[:10] #only keep best 10 (PG)
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
            pipeScore += 1
            if pipeScore > highScore:
                highScore = pipeScore
        '''if len(pipes) == 1 and pipe.x < width/2:
            pipes.append(Pipe())'''

    pipe_surface = scorefont.render(str(pipeScore), False, WHITE)
    generation_surface = myfont.render('Generation: '+str(generation), False, BLACK)
    score_surface = myfont.render('High Score: '+str(highScore), False, BLACK)
    num_surface = myfont.render('Birds: ' + str(len(birds)), False, BLACK)
    if bestBird:
        print("best:",bestBird.brain.wih,bestBird.brain.who)
    '''if birds:
        print("inputs: ",birds[0].x - pipes[0].x)'''

    screen.blit(generation_surface, (400, 480))
    screen.blit(score_surface, (400, 510))
    screen.blit(num_surface, (400, 540))
    screen.blit(pipe_surface,(500,50))
    pygame.display.update()
    if highScore > 9:
        if counter %5 == 0:
            Capture(screen, 'Capture{}.png'.format(counter), (0, 0), (600, 600))
    clock.tick(FPS)
pygame.quit()
    