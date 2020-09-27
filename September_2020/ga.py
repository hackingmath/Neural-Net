'''Dan Shiffman's Neuroevolution video'''

import random
from bird import Bird

def nextGeneration(n, savedBirds, birds, bestBirds):
    savedBirds.extend(bestBirds) #<><><><><><>#.#<><><><><><>#.#<><><><><><>#
    calculateFitness(savedBirds)
    savedBirds.sort(key=Bird.get_score, reverse=True) #<><><><><><>#.#<><><><><><>#.#<><><><><><>#
    for i in range(n - 50): #<><><><><><>#.#<><><><><><>#.#<><><><><><>#
        new_bird = pickOne(savedBirds)
        if random.random() < 0.5 and i > 0: # cross breed - not sure this works!
            new_bird.brain.wih = (new_bird.brain.wih + birds[-1].brain.wih) * 0.75
            new_bird.brain.who = (new_bird.brain.who + birds[-1].brain.who) * 0.25
        birds.append(new_bird)
    for i in range(50):
        birds.append(Bird()) # add 50 fresh blood

def pickOne(savedBirds, rate=0.3):
    index = 0
    r = random.random() * 0.5 # only select from first half of savedBirds
    while r > 0:
        r = r - savedBirds[index].fitness
        index += 1

    index -= 1
    bird = savedBirds[index]
    child = Bird(bird.brain)
    amount = 0.2 if index > 50 else 0.002 * index #<><><><><><>#.#<><><><><><>#.#<><><><><><>#
    child.brain.mutate(rate, amount)
    return child

def calculateFitness(savedBirds):
    _sum = 0
    for bird in savedBirds:
        _sum += bird.score

    for bird in savedBirds:
        bird.fitness = bird.score / _sum