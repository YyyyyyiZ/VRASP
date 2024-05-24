import numpy as np


def calculate_schedule_or_actual(routes, travel_matrix, service_duration):
    """
    Calculate the actual arrival time of the graph
    given routes, schedule, exact travel time and service duration
    """
    scheduled = []
    for i in range(len(routes)):
        one_schedule = [0]
        for j in range(len(routes[i]) - 1):
            one_schedule.append(int(np.ceil(one_schedule[-1] + service_duration[routes[i][j]] +
                                            travel_matrix[routes[i][j]][routes[i][j + 1]])))
        scheduled.append(one_schedule)
    return scheduled


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


def merge_shortest_routes(lst, crew):
    while len(lst) > crew:
        shortest_idx1 = min(range(len(lst)), key=lambda i: len(lst[i]))
        shortest_idx2 = min([i for i in range(len(lst)) if i != shortest_idx1], key=lambda i: len(lst[i]))
        lst = [lst[i] for i in range(len(lst)) if i != shortest_idx1 and i != shortest_idx2]
    return lst
