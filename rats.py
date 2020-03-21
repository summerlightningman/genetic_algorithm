import time
import random
import statistics

GOAL = 50000  # Target weight (g)
NUM_RATS = 20  # Num of adult rats

INITIAL_MIN_WT = 200  # min weight of rats, in initial population
INITIAL_MAX_WT = 600  # max weight ...
INITIAL_MODE_WT = 300  # Most common weight

MUTATE_ODDS = .01  # Probability of a mutation occurring in a rat
MUTATE_MIN = .5
MUTATE_MAX = 1.2

LITTER_SIZE = 8  # Number of children per pair
LITTERS_PER_YEAR = 10  # Yearly number of children per pair per

GENERATION_LIMIT = 500  # Total count of generations

if NUM_RATS % 2 != 0:
    NUM_RATS += 1


def populate(num_rats, min_wt, max_wt, mode_wt):
    return [int(random.triangular(min_wt, max_wt, mode_wt)) for _ in range(num_rats)]


def fitness(population, goal):
    ave = statistics.mean(population)
    return ave / goal


def select(population, to_retain):
    sorted_population = sorted(population)

    to_retain_by_gender = to_retain // 2
    members_per_gender = len(sorted_population) // 2

    females = sorted_population[:members_per_gender]
    males = sorted_population[members_per_gender:]

    selected_females = females[-to_retain_by_gender:]
    selected_males = males[-to_retain_by_gender:]
    return selected_females, selected_males


def breed(males, females, litter_size):
    random.shuffle(males)
    random.shuffle(females)
    children = []
    for male, female in zip(males, females):
        for child in range(litter_size):
            try:
                child = random.randint(female, male)
            except ValueError:
                child = random.randint(male, female)
            children.append(child)
    return children


def mutate(children, mutate_odds, mutate_min, mutate_max):
    for index, rat in enumerate(children):
        if mutate_odds >= random.random():
            children[index] = round(rat * random.uniform(mutate_min, mutate_max))
    return children


def start():
    generations = 0
    parents = populate(NUM_RATS, INITIAL_MIN_WT, INITIAL_MAX_WT, INITIAL_MODE_WT)

    print(f'Initial population weights = {parents}')

    population_fitness = fitness(parents, GOAL)

    print(f'initial population fitness = {population_fitness}')
    print(f'number to retain = {NUM_RATS}')

    ave_weight = []

    while population_fitness < 1 and generations < GENERATION_LIMIT:
        selected_males, selected_females = select(parents, NUM_RATS)

        children = breed(selected_males, selected_females, LITTER_SIZE)
        children = mutate(children, MUTATE_ODDS, MUTATE_MIN, MUTATE_MAX)

        parents = selected_males + selected_females + children
        population_fitness = fitness(parents, GOAL)

        print(f'Generation: {generations} fitness = {"%.4f" % population_fitness}')
        ave_weight.append(int(statistics.mean(parents)))
        generations += 1
    print(f'''Average weight per generation = {ave_weight}
Number of generations = {generations}
Number of years = {int(generations / LITTERS_PER_YEAR)}''')


if __name__ == '__main__':
    start_time = time.time()
    start()
    end_time = time.time()
    duration = end_time - start_time
    print(f'Program was completed in {duration} seconds')
