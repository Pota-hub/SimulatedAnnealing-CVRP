import tsplib95
from simpleai.search import SearchProblem
import random
import sys

class TSPProblem(SearchProblem):
    def __init__(self, tsp_instance):
        self.tsp_instance = tsp_instance
        self.num_cities = tsp_instance.dimension
        self.initial_state = tuple(random.sample(range(1, self.num_cities+1), self.num_cities))

    def actions(self, state):
        return [(i,j) for i in range(self.num_cities-1) for j in range(i+1, self.num_cities)]

    def result(self, state, action):
        i, j = action
        new_state = list(state)
        new_state[i], new_state[j] = new_state[j], new_state[i]
        return tuple(new_state)

    def value(self, state):
        return -self.tsp_instance.get_weight(state[-1], state[0]) - sum(self.tsp_instance.get_weight(state[i], state[i+1]) for i in range(self.num_cities-1))

def simulated_annealing(problem, schedule):
    current_state = problem.initial_state
    current_value = problem.value(current_state)
    for T in schedule:
        next_state = problem.result(current_state, random.choice(problem.actions(current_state)))
        next_value = problem.value(next_state)
        delta_e = next_value - current_value
        if delta_e > 0 or random.uniform(0, 1) < pow(2.7, delta_e / T):
            current_state, current_value = next_state, next_value
    return current_state, current_value

# Ejemplo de uso
if __name__ == '__main__':
    # Cargar el problema CVRP desde un archivo
    if len(sys.argv) != 2:
        print(f"usage: python {sys.argv[0]} fname") #espific .vrp file
        exit(1)
    elif len(sys.argv) == 2: 
        tsp = tsplib95.load(sys.argv[1])
    else:# por si no lee
        tsp = tsplib95.load("eil22.vrp")

    #tsp = tsplib95.load('IA\Simulated_Annealing\eil22.vrp')
    problem = TSPProblem(tsp)
    schedule = [100000, 10000, 1000, 100, 10]
    #schedule = [10]
    state, value = simulated_annealing(problem, schedule)
    print(f"Mejor solución encontrada: {state}. Valor: {value*-1}")
