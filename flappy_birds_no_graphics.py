#Dan Shiffman
#Neuro-Evolution Flappy Bird

import numpy
import time
from pipe import Pipe
from bird import Bird
import ga
import random

NUM_BIRDS = 1000

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
    if generation % 50 == 0:
        print("Generation:", generation)


size = (width,height)
for i in range(int(NUM_BIRDS/4)):
    birds.append(Bird())

#set up clock

FPS = 60 #frames per second
counter = 0

#loop until user clicks the close button
done = False

while not done:
    counter += 1

    if not pipes:
        pipes.append(Pipe())
    if len(pipes) == 1:
        if pipes[0].x < width/2:
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
                print("High Score:", highScore)


    if bestBird and pipeScore == 100:
        print("best:",bestBird.brain.wih,bestBird.brain.who)
        with open("bestbirds.txt",'w') as f:
            f.write("best:")
            f.write(str(bestBird.brain.wih)+ '\n'+str(bestBird.brain.who)+ '\n')
            f.write("end.")
    '''if birds:
        print("inputs: ",birds[0].x - pipes[0].x)'''


    