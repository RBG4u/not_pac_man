from deap import algorithms, tools, creator, base
import deap

import numpy as np
import random

POLE_SIZE = 23
OBJECTS = 20
LENGHT_CHROM = 3*OBJECTS
TYPE_LENGHT_OBJECT = [10, 10, 7, 7, 7, 5, 5, 5, 5, 5, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1]

POPULATION_SIZE = 50
PROB_CROSSOVER = 0.9
PROB_MUTATION = 0.3
MAX_GENERATIONS = 20
HOF_SIZE = 1


def random_objects(total: int) -> list[int]:
    objects = []
    for n in range(total):
        objects.extend([random.randint(1, POLE_SIZE),
                        random.randint(1, POLE_SIZE),
                        random.randint(0, 1)])

    return creator.Individual(objects)


def check_objects_fitness(individual: list[int]) -> tuple[float]:
    inf = 1000
    field_s = np.zeros((POLE_SIZE, POLE_SIZE))
    field = np.ones((POLE_SIZE+12, POLE_SIZE+12)) * inf
    field[2:POLE_SIZE+2, 2:POLE_SIZE+2] = field_s

    border = 0.2
    horiz = np.ones((3, 12)) * border
    object_one = np.ones((1, 10))
    vert = np.ones((12, 3)) * border

    for *object, type in zip(*[iter(individual)]*3,  TYPE_LENGHT_OBJECT):
        if object[-1] == 0:
            m_object = np.copy(horiz[:, :type+2])
            m_object[1, 1:type+1] = object_one[0, :type]
            field[object[0]-1:object[0]+2, object[1]-1:object[1]+type+1] += m_object
        else:
            m_object = np.copy(vert[:type+2, :])
            m_object[1:type+1, 1] = object_one[0, :type]
            field[object[0]-1:object[0]+type+1, object[1]-1:object[1]+2] += m_object

    fitness = np.sum(field[np.bitwise_and(field > 1, field < inf)])
    fitness += np.sum(field[field > inf+border*4])
    return fitness,


def mutate_objects(individual: list[int], indpb: float
                   ) -> tuple[list[int]]:
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] = random.randint(0, 1) if (i+1) % 3 == 0 else random.randint(1, POLE_SIZE)

    return individual,


def find_best_objects(population: list[list[int]],
                      toolbox: deap.base.Toolbox,
                      stats: deap.tools.support.Statistics,
                      hof: deap.tools.support.HallOfFame
                      ) -> list[int]:
    max_fitness = 1000

    while max_fitness > 0.5:
        population, logbook = algorithms.eaSimple(population,
                                                  toolbox,
                                                  cxpb=PROB_CROSSOVER,
                                                  mutpb=PROB_MUTATION,
                                                  ngen=MAX_GENERATIONS,
                                                  stats=stats,
                                                  halloffame=hof,
                                                  verbose=True)

        max_fitness = logbook.select("min")[-1]
        print(max_fitness)

    best = hof.items[0]
    return best


def init() -> tuple[deap.base.Toolbox,
                    deap.tools.support.Statistics]:
    creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
    creator.create('Individual', list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register('random_objects', random_objects, OBJECTS)
    toolbox.register('population_creator', tools.initRepeat,
                     list, toolbox.random_objects)
    toolbox.register('evaluate', check_objects_fitness)
    toolbox.register('select', tools.selTournament, tournsize=3)
    toolbox.register('mate', tools.cxTwoPoint)
    toolbox.register('mutate', mutate_objects, indpb=1.0/LENGHT_CHROM)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)

    return toolbox, stats


def find_objects() -> list[tuple[int, int]]:
    toolbox, stats = init()
    population = toolbox.population_creator(n=POPULATION_SIZE)
    hof = tools.HallOfFame(HOF_SIZE)
    size = 40
    objects_coords = []
    objects = find_best_objects(population, toolbox, stats, hof)
    for *object, type in zip(*[iter(objects)]*3,  TYPE_LENGHT_OBJECT):
        if object[-1] == 0:
            for i in range(type):
                coord = (object[0]*size, (object[1]+i)*size)
                objects_coords.append(coord)
        else:
            for i in range(type):
                coord = ((object[0]+i)*size, object[1]*size)
                objects_coords.append(coord)

    return objects_coords
