import random
from operator import itemgetter
from vns_saa.tool import calculate_actual, calculate_cost_over_samples, merge_shortest_routes
from vns_saa.neighborhood import shake, variable_neighborhood_descent


def clarke_wright_algorithm(vrp):
    """
    C-W Initialization
    :param vrp: list of ServiceInstance()
    :return: initial route, initial schedule
    """
    routes = []
    for i in range(1, vrp[0].number_of_patients + 1):
        routes.append([i])

    # Sij = Ci0 + C0j - Cij
    savings = []
    for i in range(1, len(routes) + 1):
        for j in range(1, len(routes) + 1):
            if i == j:
                pass
            else:
                saving = 0
                for idn in range(0, len(vrp)):
                    saving += (vrp[idn].cost_matrix[i][0] + vrp[idn].cost_matrix[0][j]) - vrp[idn].cost_matrix[i][j]
                savings.append([i, j, saving])

    savings = sorted(savings, key=itemgetter(2), reverse=True)

    for i in range(len(savings)):
        startRoute = []
        endRoute = []
        serviceTime = []
        for j in range(len(routes)):
            if savings[i][0] == routes[j][-1]:
                endRoute = routes[j]
            elif savings[i][1] == routes[j][0]:
                startRoute = routes[j]

            if (len(startRoute) != 0) and (len(endRoute) != 0):
                for idn in range(0, len(vrp)):
                    temp = 0
                    for k in range(len(startRoute)):
                        temp += vrp[idn].service_duration[startRoute[k]]
                    serviceTime.append(temp)
                for idn in range(0, len(vrp)):
                    for k in range(len(endRoute)):
                        serviceTime[idn] += vrp[idn].service_duration[endRoute[k]]
                routeStore = [0] + endRoute + startRoute + [0]
                for idn in range(0, len(vrp)):
                    for h in range(len(routeStore) - 1):
                        serviceTime[idn] += vrp[idn].travel_matrix[routeStore[h]][routeStore[h + 1]]

                if serviceTime <= [vrp[0].work_minutes] * len(vrp):
                    routes.remove(startRoute)
                    routes.remove(endRoute)
                    routes.append(endRoute + startRoute)
                break

    routes = merge_shortest_routes(routes, vrp[0].number_of_crew)

    for i in range(len(routes)):
        routes[i].insert(0, 0)
        routes[i].insert(len(routes[i]), 0)

    scheduled = calculate_actual(routes, vrp[0].travel_matrix, vrp[0].service_duration)

    return routes, scheduled


def variable_neighborhood_search(vrp, cur_route, cur_schedule, max_iter, k_max, ts_iter, ratio):
    best_route = cur_route
    best_schedule = cur_schedule

    for idm in range(max_iter):
        k = 0
        while k < k_max:
            idn = random.randint(0, len(vrp) - 1)
            # Shaking Phase
            route1, schedule1 = shake(k, vrp, vrp[idn], cur_route, cur_schedule, ratio)
            # Variable neighborhood descent Phase, Tabu search for better solution
            route1_1, schedule1_1 = variable_neighborhood_descent(vrp, vrp[idn], route1, schedule1, ts_iter)
            # If best solution IMPROVED, continue search in current k
            if (calculate_cost_over_samples(vrp, route1_1, schedule1_1) <
                    calculate_cost_over_samples(vrp, best_route, best_schedule)):
                best_route = route1_1
                best_schedule = schedule1_1
            else:
                k += 1

        if (idm+1) % 100 == 0:
            cur_cost = calculate_cost_over_samples(vrp, best_route, best_schedule)
            print("VNS iter:{}   Current_best_solution:\n{}\n{}".format(idm + 1, best_route, best_schedule))
            print("Cost:{}".format(cur_cost))

    return best_route, best_schedule
