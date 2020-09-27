# Dan Shiffman
# Neuro-Evolution Flappy Bird

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
pipeScore = 0  # how many pipes have gone by
highScore = 0
pipeSpacing = 0.5 #percent of the width

width = 600
height = 600


def restart():
    global pipes, birds, generation, savedBirds, pipeScore
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
    ga.nextGeneration(NUM_BIRDS, savedBirds, birds, bestBirds)

    savedBirds = []
    generation += 1
    if generation % 50 == 0:
        print("Generation:", generation)


size = (width, height)
for i in range(int(NUM_BIRDS / 4)):
    birds.append(Bird())

# set up clock

FPS = 300  # frames per second
counter = 0

# loop until user clicks the close button
done = False

while not done:
    counter += 1

    if not pipes:
        pipes.append(Pipe())
    if len(pipes) == 1:
        if pipes[0].x < width * pipeSpacing:
            pipes.append(Pipe())
    if not birds:
        restart()
    for bird in birds:
        bird.think(pipes)
        if bird.score > bestScore:
            bestScore = bird.score
            bestBird = bird
            bestBirds.append(bird)
            bestBirds.sort(key=Bird.get_score, reverse=True)
            bestBirds = bestBirds[:10]  # only keep best 10 (PG)
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
            if pipe in pipes:
                pipes.remove(pipe)
            pipeScore += 1
            if pipeScore > highScore:
                highScore = pipeScore
                print("High Score:", highScore)
        #pipeSpacing = 0.5*0.9**(pipeScore//10)
        pipeSpacing = 0.25 * (1.1 ** (pipeScore // 10))

    if bestBird and pipeScore == 100:
        #print("best:", bestBird.brain.wih, bestBird.brain.who)
        with open("bestbirds.txt", 'w') as f:
            f.write("best:")
            f.write(str(bestBird.brain.wih) + '\n' + str(bestBird.brain.who) + '\n')
            f.write("end.")
    '''if birds:
        print("inputs: ",birds[0].x - pipes[0].x)'''

"""Sept 26, 2020
best: [[ 0.15903079  0.24787288 -0.3315933   0.51771032  0.17827848]
 [ 0.3658817  -0.11755093  0.00651274  1.09753461 -0.17477396]
 [-0.0856602  -0.1979054   0.32692659 -0.10954562 -0.47494797]
 [-0.03520064  0.23258557  0.29916583  0.23236534  0.04920222]
 [ 1.05274567 -0.14290662 -0.2830915   0.28772121  0.59523862]
 [ 0.38097828  0.34277721 -0.75593239  0.11427605 -0.75119124]] [[-1.05608464  0.30405842  1.29108259  0.62701698  0.64785661  0.27023949]]
 
 
 Sept. 27, 2020
 best: [[ 0.45753267 -0.43874432  0.23728658 -1.05519945 -0.69027315]
 [ 0.30570402 -0.17059207 -0.1825754  -1.01196564 -0.50501756]
 [ 0.25609236 -0.69173785 -0.61663018 -0.58723115 -0.25499926]
 [ 0.25513649  0.19747379  1.95186778  0.4591265   0.42361957]
 [ 0.01149327  0.98324487  1.27070892 -0.62919273 -1.99312427]
 [ 1.62941622 -1.68495166 -0.12463148 -0.41390205  0.96477484]] [[-0.66663905  0.01239793 -0.59580265  0.02345286  0.08488607  0.68990777]]
 """