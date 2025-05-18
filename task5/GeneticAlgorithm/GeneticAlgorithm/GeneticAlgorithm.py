from deap import base, creator, tools, algorithms
import random, numpy as np, matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import math

# ---------- Налаштування ----------
NUM_CITIES = 20
POPULATION_SIZE = 100
P_CROSSOVER = 0.9
P_MUTATION = 0.2
MAX_GENERATIONS = 100 

# ---------- Генерація міст ----------
cities = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(NUM_CITIES)]

def euclidean(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def total_distance(individual):
    dist = 0
    for i in range(len(individual)):
        city1 = cities[individual[i]]
        city2 = cities[individual[(i + 1) % len(individual)]]
        dist += euclidean(city1, city2)
    return (dist,)

# ---------- DEAP ----------
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(NUM_CITIES), NUM_CITIES)
toolbox.register("individualCreator", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

toolbox.register("evaluate", total_distance)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)

population = toolbox.populationCreator(n=POPULATION_SIZE)

# ---------- Статистика ----------
stats = tools.Statistics(lambda ind: ind.fitness.values[0])
stats.register("min", np.min)
stats.register("avg", np.mean)

minFitnessValues = []
meanFitnessValues = []
allFitness = []

# ---------- Еволюція ----------
for gen in range(MAX_GENERATIONS):
    offspring = algorithms.varAnd(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION)

    fits = list(map(toolbox.evaluate, offspring))
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit

    population = toolbox.select(offspring, k=len(population))

    record = stats.compile(population)
    minFitnessValues.append(record['min'])
    meanFitnessValues.append(record['avg'])
    allFitness.append([ind.fitness.values[0] for ind in population])

    print(f"Покоління {gen+1}: найкращий = {record['min']:.2f}, середній = {record['avg']:.2f}")

# ---------- Візуалізація ----------
fig, ax = plt.subplots()
frames = []
for gen_fitness in allFitness:
    line, = ax.plot(gen_fitness, 'go', markersize=2)
    frames.append([line])

animation = ArtistAnimation(fig, frames, interval=150, blit=True)
plt.title("Еволюція придатності по поколіннях")
plt.xlabel("Індивіди")
plt.ylabel("Відстань")
plt.show()
