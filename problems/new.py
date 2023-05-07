import tsplib95
import math
import random

# Cargar los datos del problema CVRP
problem = tsplib95.load("gil262.vrp")
# Obtener el número de nodos
num_nodes = problem.dimension
# Obtener las coordenadas de cada nodo
coord = problem.node_coords
# Obtener la capacidad del vehículo
vehicle_capacity = problem.capacity
# Obtener la demanda de cada cliente
demand = problem.demands




# Función para calcular la distancia entre dos nodos
def distance(node1, node2):
    x1, y1 = coord[node1]
    x2, y2 = coord[node2]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Función para calcular el costo de una ruta
def route_cost(route):
    cost = 0
    for i in range(len(route) - 1):
        cost += distance(route[i], route[i+1])
    return cost



# Función para generar una solución inicial aleatoria
def initial_solution():
    # Crear una lista de clientes y mezclarla aleatoriamente
    customers = list(range(1, num_nodes))
    random.shuffle(customers)
    
    # Dividir la lista de clientes en rutas que respeten la capacidad del vehículo
    solution = []
    while len(customers) > 0:
        route = [0]  # Agregar el depósito como el primer nodo de cada ruta
        capacity = 0
        for customer in customers:
            if capacity + demand[customer] <= vehicle_capacity:
                route.append(customer)
                capacity += demand[customer]
        route.append(0)  # Agregar el depósito como el último nodo de cada ruta
        solution.append(route)
        for customer in route[1:-1]:
            customers.remove(customer)
    
    return solution



# Definir una temperatura inicial y un factor de enfriamiento
temperature = 100
cooling_factor = 0.99

# Generar una solución inicial aleatoria que satisfaga las restricciones del problema
current_solution = initial_solution()

# Repetir hasta que se alcance la condición de parada
while temperature > 1e-6:
    # Generar una solución vecina haciendo una pequeña modificación a la solución actual
    neighbor_solution = list(current_solution)
    route1 = random.randint(0, len(current_solution)-1)
    route2 = random.randint(0, len(current_solution)-1)
    customer1 = random.choice(current_solution[route1][1:-1])
    customer2 = random.choice(current_solution[route2][1:-1])
    neighbor_solution[route1].remove(customer1)
    neighbor_solution[route2].remove(customer2)
    if len(neighbor_solution[route1]) == 1:
        neighbor_solution.remove(neighbor_solution[route1])
    if len(neighbor_solution[route2]) == 1:
        neighbor_solution.remove(neighbor_solution[route2])
        neighbor_solution[random.randint(0, len(neighbor_solution)-1)].insert(random.randint(1, len(neighbor_solution[route1])-1), customer2)
        neighbor_solution[random.randint(0, len(neighbor_solution)-1)].insert(random.randint(1, len(neighbor_solution[route2])-1), customer1)

    # Calcular la diferencia de costo entre la solución actual y la vecina
    current_cost = sum(distance_matrix[current_solution[i][-1]][current_solution[i+1][0]] for i in range(len(current_solution)-1))
    current_cost += sum(distance_matrix[current_solution[i][-1]][current_solution[i+1][1]] for i in range(len(current_solution)-1))
    current_cost += sum(distance_matrix[0][current_solution[i][1]] for i in range(len(current_solution)))
    neighbor_cost = sum(distance_matrix[neighbor_solution[i][-1]][neighbor_solution[i+1][0]] for i in range(len(neighbor_solution)-1))
    neighbor_cost += sum(distance_matrix[neighbor_solution[i][-1]][neighbor_solution[i+1][1]] for i in range(len(neighbor_solution)-1))
    neighbor_cost += sum(distance_matrix[0][neighbor_solution[i][1]] for i in range(len(neighbor_solution)))
    cost_difference = neighbor_cost - current_cost

    # Si la vecina es mejor, aceptarla como la nueva solución actual
    if cost_difference < 0:
        current_solution = neighbor_solution
    # Si la vecina es peor, aceptarla con una probabilidad determinada por la temperatura actual y la diferencia de costo
    else:
        acceptance_probability = math.exp(-cost_difference/temperature)
        if random.random() < acceptance_probability:
            current_solution = neighbor_solution
    # Reducir la temperatura según el factor de enfriamiento
    temperature *= cooling_factor

    # Devolver la mejor solución encontrada y su costo
    best_solution = current_solution
    best_cost = sum(distance_matrix[best_solution[i][-1]][best_solution[i+1][0]] for i in range(len(best_solution)-1))
    best_cost += sum(distance_matrix[best_solution[i][-1]][best_solution[i+1][1]] for i in range(len(best_solution)-1))
    best_cost += sum(distance_matrix[0][best_solution[i][1]] for i in range(len(best_solution)))
    print("Mejor solución encontrada: ", best_solution)
    print("Costo de la mejor solución encontrada: ", best_cost)
