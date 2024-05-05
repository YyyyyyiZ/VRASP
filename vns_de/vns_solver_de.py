import numpy as np

from vns_de.core import clarke_wright_algorithm, variable_neighborhood_search
from vns_de.tool import calculate_schedule_or_actual, graph_cost
from utils.data_model import ServiceInstance, Patient


def avg_array(matrix):
    matrix = np.array(matrix)
    col_avg = np.mean(matrix, axis=0)
    return col_avg.tolist()


def deterministic(size, cost_matrix, service_duration, travel_matrix, cf=100, co=1, ct=3, length=480, num_samples=30,
                  max_iter=1000, k_max=4, ts_iter=30, ratio=0.2):
    # Average service_time and travel_time in samples to obtain an estimate
    cost_matrix = cost_matrix
    avg_travel = avg_array(travel_matrix)
    avg_service = [0] + avg_array(service_duration)

    instance = ServiceInstance(size, int(np.ceil(size / 6)), length, cost_matrix, avg_travel, avg_service, cf, co, ct)
    for i in range(size):
        patient = Patient()
        patient.service_duration = avg_service[i]
        patient.index = i
        instance.list_of_patients.append(patient)

    # C-W initialization
    initial_route, initial_schedule = clarke_wright_algorithm(instance)
    print("initial_solution:\n{}\n{}".format(initial_route, initial_schedule))
    print("cost:\n{}".format(graph_cost(instance, initial_route, initial_schedule, initial_schedule)))
    # Calculate the real cost over samples
    cost0 = []
    for idn in range(num_samples):
        actual = calculate_schedule_or_actual(initial_route, travel_matrix[idn], [0] + service_duration[idn])
        cost0.append(graph_cost(instance, initial_route, initial_schedule, actual))
    print("Real avg cost over {} samples:{}".format(num_samples, sum(cost0) / len(cost0)))

    # Variable Neighborhood Search
    best_route, best_schedule = variable_neighborhood_search(instance, initial_route, initial_schedule, avg_travel,
                                                             avg_service, max_iter, k_max, ts_iter, ratio)
    print("best_solution:\n{}\n{}".format(best_route, best_schedule))
    print("cost:{}".format(graph_cost(instance, best_route, best_schedule, best_schedule)))
    # Calculate the real cost over samples
    cost1 = []
    for idn in range(num_samples):
        actual = calculate_schedule_or_actual(best_route, travel_matrix[idn], [0] + service_duration[idn])
        cost1.append(graph_cost(instance, best_route, best_schedule, actual))
    print("Real avg cost over {} samples:{}".format(num_samples, sum(cost1) / len(cost1)))
