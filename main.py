import random
import math
import timeit

def of(gen, k_x):
    r = 0
    gen = decrypt_gen(gen)
    for i in range(len(k_x)):
        cr = 0
        dim = len(k_x[i])
        for d in range(dim):
            cr += (k_x[i][d] - gen[d]) ** 2
        r += math.sqrt(cr)
    return r

def ff(gen, k_x):
    return 1.0 / (1.0 + of(gen, k_x))

def roulette_wheel_selection(probs):
    summation = sum(probs)
    rnd = random.random() * summation
    passed_probs = 0
    for index, prob in enumerate(probs):
        passed_probs += prob
        if passed_probs > rnd:
            return index
    return -1

def decrypt_gen(gen):
    new_gen = []
    dim = int(len(gen) / bits)
    for i in range(dim):
        gen_part = gen[bits * i:bits * (i+1)]
        new_gen.append(int(gen_part,2))
    return new_gen

def mutation(gen):
    mutuation_pos = random.randrange(len(gen))
    gen = list(gen)
    gen[mutuation_pos] = '0' if gen[mutuation_pos] == '1' else '1'
    gen = "".join(gen)
    return gen

def crossover(gen1, gen2):
    crossover_pos = random.randrange(len(gen1))
    newgen1 = gen1[:crossover_pos] + gen2[crossover_pos:]
    newgen2 = gen2[:crossover_pos] + gen1[crossover_pos:]
    return newgen1, newgen2

def create_initial_pop(n_pop, n):
    pop = []
    
    for i in range(n_pop):
        this_pop = ''
        for dim in range(n):
            rnd = random.randrange(2 ** bits)
            this_pop += bin(rnd)[2:].zfill(bits)
        pop.append(this_pop)

    return pop

def get_middle_pop(pop, p_mutuation):
    middle_pop = []
    random.shuffle(pop)
    
    for i in range(0, len(pop) if len(pop) % 2 == 0 else len(pop) - 1, 2):
        if random.random() < p_crossover:
            newgen1, newgen2 = crossover(pop[i], pop[i + 1])
            middle_pop.append(newgen1)
            middle_pop.append(newgen2)

    for i in range(len(pop)):
        if(random.random() < p_mutuation):
            middle_pop.append(mutation(pop[i]))
        else:
            middle_pop.append(pop[i])

    return middle_pop


def get_final_pop(middle_pop, n_pop):
    final_pop = []
    for i in range(n_pop):
        middle_pop_ff = list(map(lambda x: ff(x, k_x), middle_pop))
        pick = roulette_wheel_selection(middle_pop_ff)
        final_pop.append(middle_pop[pick])
        middle_pop.pop(pick)
    return final_pop

def bits_needed_for(num):
    return math.floor(math.log(num, 2)) + 1

def minimize_k_x(k_x):
    minimum = min([min(p) for p in k_x])
    new_k_x = []

    for x in k_x:
        new_k_x.append([e - minimum for e in x])
    return minimum, new_k_x

# problem definition
k = 6
k_x = [[33,27,33], [46,27,20], [33,14,20], [33,40,20], [33,27,7], [20,27,20]]

n = 3 # dim
n_pop = 16
iterations = 5000

p_crossover = .2
p_mutuation = 1.0

# main algorithm
k_x_minimum, k_x_min = minimize_k_x(k_x)
bits = bits_needed_for(max([max(p) for p in k_x_min]))

start = timeit.default_timer() # start time
initial_pop = create_initial_pop(n_pop, n)
new_pop = initial_pop
best_sol_gen = ''
best_sol_cost = float('Inf')

for i in range(iterations):
    middle_pop = get_middle_pop(new_pop, p_mutuation)
    new_pop = get_final_pop(middle_pop, n_pop)
    
    for gen in new_pop:
        if(of(gen, k_x_min) < best_sol_cost):
            best_sol_cost = of(gen, k_x_min)
            best_sol_gen = gen

print("Best Cost: ", best_sol_cost)
print("Best Solution: ", [x + k_x_minimum for x in decrypt_gen(best_sol_gen)])
stop = timeit.default_timer()
print('Execution Time: ', stop - start, 's')