import numpy as np

from vns_saa.core import clarke_wright_algorithm, variable_neighborhood_search
from vns_saa.tool import calculate_cost_over_samples
from utils.data_model import ServiceInstance, Patient


def saa(size, cost_matrix, service_duration, travel_matrix, cf=100, co=1, ct=3, length=480, num_samples=30,
        max_iter=1000, k_max=4, ts_iter=30, ratio=0.2):
    # Each instance has the same cost_matrix(same location)
    # but different travel matrix(stochastic travel time) and service_duration(stochastic service time)
    instance_list = []
    for idn in range(num_samples):
        instance = ServiceInstance(size, int(np.ceil(size / 6)), length, cost_matrix, travel_matrix[idn],
                                   [0] + service_duration[idn], cf, co, ct)
        for i in range(size):
            patient = Patient()
            patient.service_duration = service_duration[idn][i]
            patient.index = i
            instance.list_of_patients.append(patient)
        instance_list.append(instance)

    # C-W initialization
    initial_route, initial_schedule = clarke_wright_algorithm(instance_list)
    print("initial_solution:\n{}\n{}".format(initial_route, initial_schedule))
    # Calculate the real cost over samples
    initial_cost = calculate_cost_over_samples(instance_list, initial_route, initial_schedule)
    print("Real avg cost over {} samples:{}".format(num_samples, initial_cost))

    # Variable Neighborhood Search
    best_route, best_schedule = variable_neighborhood_search(instance_list, initial_route, initial_schedule,
                                                             max_iter, k_max, ts_iter, ratio)
    print("best_solution:\n{}\n{}".format(best_route, best_schedule))
    # Calculate the real cost over samples
    best_cost = calculate_cost_over_samples(instance_list, best_route, best_schedule)
    print("Real avg cost over {} samples:{}".format(num_samples, best_cost))

    return
