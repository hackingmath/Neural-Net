# adapting flappy bird GA for Asteroids
# October 20, 2020
import random
from ship_ai_PF import Ship
import time

start = time.time()

def nextGeneration():
    global NUM_SHIPS,savedships,ships,bestships
    ships = bestships[::]
    calculateFitness()
    savedships.sort(key=Ship.get_score, reverse=True) #<><><><><><>#.#<><><><><><>#.#<><><><><><>#
    for i in range(NUM_SHIPS): #<><><><><><>#.#<><><><><><>#.#<><><><><><>#
        new_ship = pickOne(savedships)
        if random.random() < 0.5 and i > 0: # cross breed - not sure this works!
            try:
                new_ship.brain.wih = (new_ship.brain.wih + bestships[-1].brain.wih) * 0.75
                new_ship.brain.who = (new_ship.brain.who + bestships[-1].brain.who) * 0.25
            except IndexError:
                new_ship.brain.wih = (new_ship.brain.wih + ships[-1].brain.wih) * 0.75
                new_ship.brain.who = (new_ship.brain.who + ships[-1].brain.who) * 0.25
        new_ship.crossovers += 1
        ships.append(new_ship)
    for i in range(5):
        ships.append(Ship()) # add 50 fresh blood

def pickOne(savedships, rate=0.3):
    index = 0
    r = random.random() * 0.5 # only select from first half of savedships
    while r > 0:
        try:
            r = r - savedships[index].fitness
        except IndexError:
            break#print("index",index)
        index += 1

    index -= 1
    ship = savedships[index]
    child = Ship(brain=ship.brain)
    amount = 0.2 if index > 50 else 0.002 * index #<><><><><><>#.#<><><><><><>#.#<><><><><><>#
    child.brain.mutate(rate, amount)
    child.mutated = ship.mutated + 1
    child.crossovers = ship.crossovers + 1
    return child

def calculateFitness():
    global savedships
    _sum = 0
    for ship in savedships:
        _fitness = ship.calcFitness(savedships)
        if _fitness:
            _sum += _fitness

    for ship in savedships:
        try:
            ship.fitness /= _sum
        except:
            pass
    return _sum

NUM_SHIPS = 20
GENERATIONS = 25

ships = [Ship() for i in range(NUM_SHIPS)]
savedships = []
bestships = []
bestship = None
generation = 0
counter = 0
bestScore = 0
highScore = 0

for i in range(GENERATIONS):
    if i>0:
        nextGeneration()
    generation += 1
    #if generation % 50 == 0:
    print("Generation:", generation)

    for n,ship in enumerate(ships):
        #ship.think(bullets)
        score = ship.play()
        print("Ship",n,"done.")
        if score > bestScore:
            bestScore = score
            bestship = ship
            bestships.append(ship)
            bestships.sort(key=Ship.get_score, reverse=True)
            bestships = bestships[:10]  # only keep best 10 (PG)
            savedships.append(ship)
            print("Best brain:", bestship.brain.wih, bestship.brain.who)
        elif score > 5000:
            savedships.append(ship)
        print("score:", score)
        print("Best score:",bestScore)
        print("Best ship mutation improvements:",bestship.mutated)
        print("Best ship crossover improvements:", bestship.crossovers)
        bestships_mutations = sum(s.mutated for s in bestships)
        bestships_crossovers = sum(s.crossovers for s in bestships)
        print("Best ships mutation improvements:", bestships_mutations)
        print("Best ships crossover improvements:", bestships_crossovers)
        print("best ships:",len(bestships))
        print("savedships:",len(savedships))

        total = calculateFitness()
        if savedships:
            print("Average Fitness:", total / len(savedships))
        else:
            print("Average Fitness:", total)
        print()
        savedships= savedships[:100]

    print("Best Score:",bestScore)
    total = calculateFitness()
    if savedships:
        print("Average Fitness:",round(total/len(savedships),1))
    else:
        print("Average Fitness:",total)
    print()

    #ships.append(pickOne(savedships))

    #drawText("Score: "+str(displayship.score), GREEN, 20, 20, 24, False)

    #generation_surface = myfont.render('Generation: ' + str(generation), False, (255, 0, 0))
    #fitness_surface = myfont.render('Fitness: ' + str(bestScore), False, (255, 0, 0))
    #num_surface = myfont.render('Ships: ' + str(len(ships)), False, (255, 0, 0))
    #score_surface = myfont.render("Score:" + str(score), False, (255, 0, 0))
    #hscore_surface = myfont.render("High Score:" + str(highScore), False, (255, 0, 0))

    #screen.blit(generation_surface, (400, 0))
    #screen.blit(fitness_surface, (400, 30))
    #screen.blit(num_surface, (400, 60))
    #screen.blit(score_surface, (400, 90))
    #screen.blit(hscore_surface, (400, 120))

print()
print("Time:",round(time.time()-start,1))
