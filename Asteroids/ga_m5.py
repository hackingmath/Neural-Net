# adapting flappy bird GA for Asteroids
# October 20, 2020
import random
from ship_ai_m5 import Ship
import time
import copy

start = time.time()

def nextGeneration():
    """Start next generation of ships using best ships from
    previous generation, mutating some and crossing over some."""
    global NUM_SHIPS,savedships,ships,bestships
    ships = bestships[:30]
    #calculateFitness()
    savedships.sort(key=Ship.get_score, reverse=True) #<><><><><><>#.#<><><><><><>#.#<><><><><><>#
    for i in range(15): #<><><><><><>#.#<><><><><><>#.#<><><><><><>#
        new_ship = pickOne(bestships)
        if random.random() < 0.5 and i > 0: # cross breed - not sure this works!
            try:
                new_ship.brain.state_dict()['l1.weight'] = \
                    (new_ship.brain.state_dict()['l1.weight'] + bestships[-1].brain.state_dict()['l1.weight']) * 0.5
                new_ship.brain.state_dict()['l2.weight'] = \
                    (new_ship.brain.state_dict()['l2.weight'] + bestships[-1].brain.state_dict()['l2.weight']) * 0.5
                new_ship.brain.state_dict()['l3.weight'] = \
                    (new_ship.brain.state_dict()['l3.weight'] + bestships[-1].brain.state_dict()['l3.weight']) * 0.5
            except IndexError:
                new_ship.brain.state_dict()['l1.weight'] = \
                    (new_ship.brain.state_dict()['l1.weight'] + ships[-1].brain.state_dict()['l1.weight']) * 0.5
                new_ship.brain.state_dict()['l2.weight'] = \
                    (new_ship.brain.state_dict()['l2.weight'] + ships[-1].brain.state_dict()['l2.weight']) * 0.5
                new_ship.brain.state_dict()['l3.weight'] = \
                    (new_ship.brain.state_dict()['l3.weight'] + ships[-1].brain.state_dict()['l3.weight']) * 0.5
        new_ship.crossovers += 1
        ships.append(new_ship)
    for i in range(5):
        ships.append(Ship()) # add 5 fresh blood

def pickOne(shipList, rate=0.3):
    """Mutate the brain of on"""
    index = 0
    r = random.random() * 0.5 # only select from first half of savedships
    while r > 0:
        try:
            r = r - shipList[index].score/total
        except IndexError:
            break#print("index",index)
        index += 1

    index -= 1
    ship = shipList[index]
    child = Ship()
    amount = 0.2 if index > 50 else 0.002 * index #<><><><><><>#.#<><><><><><>#.#<><><><><><>#
    child.brain = copy.deepcopy(ship.brain)
    child.brain.mutate(rate, amount)
    child.mutated = ship.mutated + 1
    #child.crossovers = ship.crossovers + 1
    return child

NUM_SHIPS = 200
GENERATIONS = 30

ships = [Ship() for i in range(NUM_SHIPS)]
savedships = []
bestships = []
bestship = None
generation = 0
counter = 0
bestScore = 0
highScore = 0

#for average score printout
total = 0
averageScore = 0
num_scored = 0
averages = []

print("Starting...")

for i in range(GENERATIONS):
    if i>0:
        nextGeneration()
    generation += 1
    #if generation % 50 == 0:
    print("Generation:", generation)
    gen_average = 0
    gen_total = 0
    for n,ship in enumerate(ships):
        #ship.think(bullets)
        score = ship.play()
        total += score
        gen_total += score
        num_scored += 1
        gen_average = gen_total/(n+1)
        averageScore = total / num_scored
        print("Gen",generation,"Ship",n,"Score:",score)
        if score > bestScore:
            bestScore = score
            bestship = ship
            bestships.append(ship)
            bestships.sort(key=Ship.get_score, reverse=True)
            #bestships = bestships[:10]  # only keep best 10 (PG)
            #savedships.append(ship)
            print("Best brain:", bestship.brain)#.wih, bestship.brain.who)
        # elif score > 5000:
        #     savedships.append(ship)
        #print("score:", score)
        # print("Best score:",bestScore)
        # print("Best ship mutation improvements:",bestship.mutated)
        # print("Best ship crossover improvements:", bestship.crossovers)
        bestships_mutations = sum([1 for s in bestships if s.mutated])
        bestships_crossovers = sum([1 for s in bestships if s.crossovers])
        # print("Best ships mutation improvements:", bestships_mutations)
        # print("Best ships crossover improvements:", bestships_crossovers)
        # print("best ships:",len(bestships))
        # print("savedships:",len(savedships))

        #total = calculateFitness()
        # if savedships:
        #     print("Average Fitness:", total / len(savedships))
        # else:
        #     print("Average Fitness:", total)
        # print()
        #savedships= savedships[:100]
        print("Average this Generation:",round(gen_average,1))
        print("Average Score:", round(averageScore,1))
        print("High Score:", bestScore)
    print("Best ships mutation improvements:", bestships_mutations)
    print("Best ships crossover improvements:", bestships_crossovers)
    averages.append(round(gen_average,1))
    print("Averages per generation:", averages)
    print()
    # print("Best Score:",bestScore)
    # total = calculateFitness()
    # if savedships:
    #     print("Average Fitness:",round(total/len(savedships),1))
    # else:
    #     print("Average Fitness:",total)

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
secs = int(time.time()-start)
hours,minutes,seconds = secs//3600,secs//60,secs%60
print("Time:",hours,"hours,",minutes,"minutes,",seconds,"seconds.")