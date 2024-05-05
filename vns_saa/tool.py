import numpy as np


def calculate_actual(routes, travel_matrix, service_duration):
    """
    Calculate the actual arrival time of the graph
    given routes, schedule, exact travel time and service duration
    """
    actual = []
    for i in range(len(routes)):
        one_schedule = [0]
        for j in range(len(routes[i]) - 1):
            one_schedule.append(int(np.ceil(one_schedule[-1] + service_duration[routes[i][j]] +
                                            travel_matrix[routes[i][j]][routes[i][j + 1]])))
        actual.append(one_schedule)
    return actual


def merge_shortest_routes(lst, crew):
    new = lst[:]
    while len(lst) > crew:
        shortest_idx1 = min(range(len(lst)), key=lambda i: len(lst[i]))
        shortest_idx2 = min([i for i in range(len(lst)) if i != shortest_idx1], key=lambda i: len(lst[i]))
        new.remove(lst[shortest_idx1])
        new.remove(lst[shortest_idx2])
        new.append(lst[shortest_idx1] + lst[shortest_idx2])
    return new


def route_cost(vrp, route, one_schedule, one_actual):
    """
    Calculate the cost of one single route(one crew)
    """
    travelCost = 0
    for i in range(len(route) - 1):
        travelCost += vrp.cost_matrix[route[i]][route[i + 1]]
    overtimeCost = max(one_actual[-1] - vrp.work_minutes, 0) * vrp.co
    lateCost = 0
    for i in range(len(one_schedule)):
        lateCost += max(one_actual[i] - one_schedule[i], 0) * vrp.ct
    cost = vrp.cf + travelCost + overtimeCost
    return cost


def graph_cost(vrp, routes, scheduled, actual):
    """
    Calculate the cost of the graph(all routes)
    """
    cost = 0
    for i in range(len(routes)):
        cost += route_cost(vrp, routes[i], scheduled[i], actual[i])
    return cost


def calculate_route_cost_over_samples(vrp, route, one_schedule, one_actual):
    """
    Calculate the cost of one single route(one crew)
    """
    cost0 = []
    for idn in range(len(vrp)):
        cost0.append(route_cost(vrp[idn], route, one_schedule, one_actual))
    return sum(cost0)


def calculate_cost_over_samples(vrp, route, schedule):
    cost = []
    for idn in range(len(vrp)):
        actual = calculate_actual(route, vrp[idn].travel_matrix, vrp[idn].service_duration)
        cost.append(graph_cost(vrp[idn], route, schedule, actual))
    return sum(cost)/len(cost)
