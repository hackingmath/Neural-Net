'''Dan Shiffman's Neuroevolution video'''

import random
from bird import Bird

def nextGeneration(n,s,birds):
    calculateFitness(s)
    for i in range(n):
        birds.append(pickOne(s))

def pickOne(savedBirds,rate=0.3):
    index = 0
    r = random.random() #or is this simply a choice between 0 and 1?
    while r > 0:
        r = r - savedBirds[index].fitness
        index += 1

    index -= 1
    bird = savedBirds[index]
    child = Bird(bird.brain)
    child.brain.mutate(rate)
    return child

def calculateFitness(savedBirds):
    _sum = 0
    for bird in savedBirds:
        _sum += bird.score

    for bird in savedBirds:
        bird.fitness = bird.score / _sum