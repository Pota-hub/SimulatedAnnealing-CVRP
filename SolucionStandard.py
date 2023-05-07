import tsplib95
import random
import math
import numpy as np
import sys


def loadProblem(problem):
    #F Funcion que reescribe en memoria el problema
    # Obtener información del problema
    num_nodes = problem.dimension # Número de nodos, incluyendo el depósito
    vehicle_capacity = problem.capacity # Capacidad del vehículo
    coordinates = problem.node_coords # Coordenadas de cada nodo
    demand = problem.demands # Demanda de cada cliente, si aplica
    # Obtener las coordenadas de los nodos
    node_coords = coordinates
    # Calcular la matriz de distancia euclidiana
    num_nodes = len(node_coords)
    # se crea una matriz de distancias a todos los nodos 
    distance_matrix = np.zeros((num_nodes, num_nodes))

    # matriz de distancias A - B
    for i in range(1,num_nodes):
        for j in range(1,num_nodes):
            if i != j:
                try : 
                    distance_matrix[i][j] = np.linalg.norm(np.array(node_coords[i]) - np.array(node_coords[j]))
                except KeyError:
                    print('There was an error on the distance matrix')
    
def dist(n1,n2):
    # distancia ecludieana entre 2 nodos
    C = coordinates[n1]
    x1,y1 = C[0],C[1]
    C2 = coordinates[n2 + 1]
    x2,y2 = C2[0],C2[1]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def route_cost(route):
    # Función para calcular el costo de una ruta
    cost = 0
    pathlenght = len(route) - 1 
    for i in range(1,pathlenght):
        cost += dist(route[i], route[i+1])
    return cost

def solution_cost(solution):
    # Función para calcular el costo total de una solución
    cost = 0
    for route in solution:
        cost += route_cost(route)
    return cost

def initial_solution():
    # Función para generar una solución inicial aleatoria
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

def calculate_cost(best_solution, distance_matrix):
    # Funcion que calcula el costo de la solucion actual en base a la matriz de distancias
    cost = 0
    max = len(best_solution) - 1
    for route in best_solution:
        for i in range(1,max):
            try:
                node1 = route[ i ]
                node2 = route[ i + 1]
                cost += distance_matrix[node1][node2]
            except:
                KeyError
    return cost

def ShowProblem():
    # Funcion para mostrar las caracteristicas del problema After Load
    prm = f'''Número de nodos, incluyendo el depósito:  {num_nodes}\n
        Capacidad del vehículo {vehicle_capacity} \n
    '''
    print(prm)
    

    
def Sim(temperature, cooling_factor ,current_solution):
    while temperature > 1e-6:
        # Generar una solución vecina haciendo una pequeña modificación a la solución actual
        neighbor_solution = list(current_solution)
        route1 = random.randint(0, len(current_solution) -1)
        route2 = random.randint(0, len(current_solution) -1)
        customer1 = random.choice(current_solution[route1][1:-1])
        customer2 = random.choice(current_solution[route2][1:-1])
        neighbor_solution[route1][neighbor_solution[route1].index(customer1)] = customer2
        neighbor_solution[route2][neighbor_solution[route2].index(customer2)] = customer1
        # Calcular la diferencia de costo entre la solución actual y la vecina
        current_cost = solution_cost(current_solution)
        neighbor_cost = solution_cost(neighbor_solution)
        cost_difference = neighbor_cost - current_cost

        # Si la vecina es mejor, aceptarla como la nueva solución actual
        if cost_difference < 0:
            current_solution = neighbor_solution
        #Si la vecina es peor, aceptarla con una probabilidad determinada por la temperatura actual y la diferencia de costo, se puede implementar de la siguiente manera:

        #Calcular la diferencia de costo entre la solución actual y la vecina
        delta_cost = calculate_cost(neighbor_solution, distance_matrix) - calculate_cost(current_solution, distance_matrix)

        #Si la vecina es mejor, aceptarla como la nueva solución actual
        if delta_cost < 0:
            current_solution = neighbor_solution
        #Si la vecina es peor, aceptarla con una probabilidad determinada por la temperatura actual y la diferencia de costo
        else:
            acceptance_probability = math.exp(-delta_cost / temperature)
        if random.random() < acceptance_probability:
            current_solution = neighbor_solution
        #factor de enfriamiento

        temperature *= cooling_factor
        #Obtener la mejor solución encontrada y su costo
        best_solution = current_solution

    best_cost = calculate_cost(best_solution, distance_matrix)
    print("Mejor solución encontrada:")
    print(best_solution)
    print("Costo de la mejor solución encontrada:", best_cost)


if __name__ == '__main__':
    # Cargar el problema CVRP desde un archivo
    if len(sys.argv) != 2:
        print(f"usage: python {sys.argv[0]} fname") #espific .vrp file
        exit(1)
    elif len(sys.argv) == 2: 
        problem = tsplib95.load(sys.argv[1])
    else:# por si no lee
        problem = tsplib95.load("eil22.vrp")

    #print( sys.argv[0] ,problem)
    # Obtener información del problema
    num_nodes = problem.dimension # Número de nodos, incluyendo el depósito
    vehicle_capacity = problem.capacity # Capacidad del vehículo
    coordinates = problem.node_coords # Coordenadas de cada nodo
    demand = problem.demands # Demanda de cada cliente, si aplica
    # Obtener las coordenadas de los nodos
    node_coords = coordinates
    # Calcular la matriz de distancia euclidiana
    num_nodes = len(node_coords)
    # se crea una matriz de distancias a todos los nodos 
    distance_matrix = np.zeros((num_nodes, num_nodes))

    # matriz de distancias A - B
    for i in range(1,num_nodes):
        for j in range(1,num_nodes):
            if i != j:
                try : 
                    distance_matrix[i][j] = np.linalg.norm(np.array(node_coords[i]) - np.array(node_coords[j]))
                except KeyError:
                    print('There was an error on the distance matrix')
    ShowProblem()           
    Sim(temperature= 100,cooling_factor=0.99,current_solution=initial_solution())