from operator import itemgetter
from vns_de.tool import merge_shortest_routes, calculate_schedule_or_actual, graph_cost
from vns_de.neighborhood import shake, variable_neighborhood_descent


def clarke_wright_algorithm(vrp):
    """
    C-W Initialization
    :param vrp: ServiceInstance()
    :return: routes
    """
    routes = []
    for i in range(1, vrp.number_of_patients + 1):
        routes.append([i])

    # Sij = Ci0 + C0j - Cij
    savings = []
    for i in range(1, len(routes) + 1):
        for j in range(1, len(routes) + 1):
            if i == j:
                pass
            else:
                saving = (vrp.cost_matrix[i][0] + vrp.cost_matrix[0][j]) - vrp.cost_matrix[i][j]
                savings.append([i, j, saving])

    savings = sorted(savings, key=itemgetter(2), reverse=True)
    # for i in range(len(savings)):
    #     print(savings[i][0], '--', savings[i][1], "  ", savings[i][2])

    for i in range(len(savings)):
        startRoute = []
        endRoute = []
        serviceTime = 0
        for j in range(len(routes)):
            if savings[i][0] == routes[j][-1]:
                endRoute = routes[j]
            elif savings[i][1] == routes[j][0]:
                startRoute = routes[j]

            if (len(startRoute) != 0) and (len(endRoute) != 0):
                for k in range(len(startRoute)):
                    serviceTime += vrp.service_duration[startRoute[k]]
                for k in range(len(endRoute)):
                    serviceTime += vrp.service_duration[endRoute[k]]
                travelTime = 0
                routeStore = [0] + endRoute + startRoute + [0]
                for h in range(len(routeStore) - 1):
                    travelTime += vrp.travel_matrix[routeStore[h]][routeStore[h + 1]]
                routeTime = serviceTime + travelTime

                if routeTime <= vrp.work_minutes:
                    routes.remove(startRoute)
                    routes.remove(endRoute)
                    routes.append(endRoute + startRoute)
                break

    routes = merge_shortest_routes(routes, vrp.number_of_crew)

    for i in range(len(routes)):
        routes[i].insert(0, 0)
        routes[i].insert(len(routes[i]), 0)

    scheduled = calculate_schedule_or_actual(routes, vrp.travel_matrix, vrp.service_duration)

    return routes, scheduled


def variable_neighborhood_search(vrp, cur_route, cur_schedule, travel_matrix, service_duration,
                                 max_iter, k_max, ts_iter, ratio):
    best_route = cur_route
    best_schedule = cur_schedule

    for idm in range(max_iter):
        k = 0
        while k < k_max:
            # Shaking Phase
            route1, schedule1 = shake(k, vrp, cur_route, cur_schedule, travel_matrix, service_duration, ratio)
            # Variable neighborhood descent Phase, Tabu search for better solution
            route1_1, schedule1_1 = variable_neighborhood_descent(vrp, route1, schedule1, travel_matrix,
                                                                  service_duration, ts_iter)
            # If best solution IMPROVED, continue search in current k
            if (graph_cost(vrp, route1_1, schedule1_1, schedule1_1) <
                    graph_cost(vrp, best_route, best_schedule, best_schedule)):
                best_route = route1_1
                best_schedule = schedule1_1
            else:
                k += 1

        if (idm+1) % 100 == 0:
            print("VNS iter:{}   Current_best_solution:\n{}\n{}".format(idm + 1, best_route, best_schedule))
            print("Cost:{}".format(graph_cost(vrp, best_route, best_schedule, best_schedule)))

    return best_route, best_schedule
