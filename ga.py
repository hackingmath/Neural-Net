'''Dan Shiffman's Neuroevolution video'''

import random
from bird import Bird

def nextGeneration(n,savedBirds,birds,bestBirds):
    savedBirds.extend(bestBirds)
    calculateFitness(savedBirds)
    savedBirds.sort(key=Bird.get_score, reverse=True)
    print(savedBirds[0].brain.who)
    for i in range(n):
        birds.append(pickOne(savedBirds))

def pickOne(savedBirds,rate=0.3):
    index = 0
    r = random.random() #or is this simply a choice between 0 and 1?
    while r > 0:
        r = r - savedBirds[index].fitness
        index += 1

    index -= 1
    bird = savedBirds[index]
    rate *= 150*bird.score
    child = Bird(bird.brain)
    child.brain.mutate(rate)
    return child

def calculateFitness(savedBirds):
    _sum = 0
    for bird in savedBirds:
        _sum += bird.score

    for bird in savedBirds:
        bird.fitness = bird.score / _sum