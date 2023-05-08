import tsplib95
from simpleai.search import SearchProblem
import random
import sys
class CVRPProblem(SearchProblem):
    def __init__(self, cvrp_instance):
        self.cvrp_instance = cvrp_instance
        self.num_customers = cvrp_instance.dimension - 1
        self.capacity = cvrp_instance.capacity
        self.initial_state = self.generate_initial_state()

    def generate_initial_state(self):
        nodes = list(range(2, self.num_customers+2))
        routes = []
        while nodes:
            route = []
            capacity = 0
            for node in nodes:
                demand = self.cvrp_instance.demands[node]
                if capacity + demand <= self.capacity:
                    route.append(node)
                    capacity += demand
            for node in route:
                nodes.remove(node)
            routes.append(route)
        return tuple(routes)

    def actions(self, state):
        actions = []
        for i in range(len(state)):
            for j in range(len(state)):
                if i == j:
                    continue
                for k in range(len(state[j])+1):
                    if k == 0 and not state[i]:
                        continue
                    if k > 0 and k < len(state[j]) and state[j][k-1] == state[j][k]:
                        continue
                    action = (i, j, k)
                    if self.is_valid_action(state, action):
                        actions.append(action)
        return actions

    def is_valid_action(self, state, action):
        i, j, k = action
        if not state[i]:
            return False
        if i == j:
            return True
        if len(state[j]) == 0:
            return True
        capacity = sum(self.cvrp_instance.demands[node] for node in state[j])
        demand = self.cvrp_instance.demands[state[i][0]]
        if capacity + demand > self.capacity:
            return False
        if k == 0:
            return True
        if k == len(state[j]):
            return True
        if state[j][k-1] == state[i][0]:
            return False
        if k > 0 and state[j][k-1] not in self.cvrp_instance.get_successors(state[i][0]):
            return False
        if k < len(state[j]) and state[i][0] not in self.cvrp_instance.get_successors(state[j][k]):
            return False
        return True

    def result(self, state, action):
        i, j, k = action
        new_state = list(state)
        if i == j:
            new_state[i] = tuple(random.sample(new_state[i], len(new_state[i])))
        else:
            new_state[i] = new_state[i][1:]
            customer = new_state[j][k-1]
            new_state[j] = new_state[j][:k-1] + [customer] + new_state[j][k-1:]
            if not new_state[i]:
                new_state.pop(i)
        return tuple(new_state)

    def value(self, state):
        return -sum(self.cvrp_instance.get_weight(1, node) for route in state for node in route) + 100000 * len(state)

def simulated_annealing(problem, schedule):
    current_state = problem.initial_state
    current_value = problem.value(current_state)
    for T in schedule:
        if not(current_state):
            next_state = problem.result(current_state, random.choice(problem.actions(current_state)))
        else:
            next_state = current_state
        next_value = problem.value(next_state)
        delta_e = next_value - current_value
        if delta_e > 0 or random.uniform(0, 1) < pow(2.7, delta_e / T):
            current_state, current_value = next_state, next_value
    return current_state, current_value

def ShowProblem(cvrp):
    # Funcion para mostrar las caracteristicas del problema After Load
    prm = f'''Número de nodos, incluyendo el depósito:  {cvrp.dimension}\n
        Capacidad del vehículo {cvrp.capacity} \n
    '''
    print(prm)

if __name__ == '__main__':
    # Cargar el problema CVRP desde un archivo
    if len(sys.argv) != 2:
        print(f"usage: python {sys.argv[0]} fname") #espific .vrp file
        exit(1)
    elif len(sys.argv) == 2: 
        cvrp = tsplib95.load(sys.argv[1])
    else:# por si no lee
        cvrp = tsplib95.load("eil22.vrp")

    #cvrp = tsplib95.load('IA\Simulated_Annealing\eil22.vrp')
    ShowProblem(cvrp) 
    problem = CVRPProblem(cvrp)
    schedule = [100000, 10000, 1000, 100, 10]
    state, value = simulated_annealing(problem,schedule)
    print(f"Mejor solución encontrada: {state}. Valor: {value}")
