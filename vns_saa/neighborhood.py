import random
import copy

from vns_saa.tool import calculate_actual, calculate_cost_over_samples, calculate_route_cost_over_samples


def calculate_regret_values(li, vrp, customer_id, routes, scheduled):
    insertion_cost = []
    for idr, route in enumerate(routes):
        for i in range(1, len(route)-1):
            new_route = route[:i] + [customer_id] + route[i:]
            new_schedule = calculate_actual([new_route], vrp.travel_matrix, vrp.service_duration)[0]
            ori_cost = calculate_route_cost_over_samples(li, route, scheduled[idr], scheduled[idr])
            new_cost = calculate_route_cost_over_samples(li, new_route, new_schedule, new_schedule)
            # positive, the smaller, the better
            delta_cost = new_cost - ori_cost
            insertion_cost.append(delta_cost)
    # secondSmallest-smallest, greater → more regret
    insertion_cost_srt = sorted(insertion_cost)
    regret = insertion_cost_srt[1] - insertion_cost_srt[0]
    return regret


def remove_customer(customer_id, routes):
    return [[element for element in row if element != customer_id] for row in routes]


def insert_customer(li, vrp, customer_id, routes, scheduled):
    best_cost = float('inf')
    best_route_idr = None
    best_position = None
    for idr, route in enumerate(routes):
        for i in range(1, len(route)-1):
            new_route = route[:i] + [customer_id] + route[i:]
            new_schedule = calculate_actual([new_route], vrp.travel_matrix, vrp.service_duration)[0]
            new_cost = calculate_route_cost_over_samples(li, new_route, new_schedule, new_schedule)
            ori_cost = calculate_route_cost_over_samples(li, route, scheduled[idr], scheduled[idr])
            # positive, the smaller, the better
            delta_cost = new_cost - ori_cost
            if delta_cost < best_cost:
                best_cost = new_cost
                best_route_idr = idr
                best_position = i

    if best_route_idr is not None:
        routes = remove_customer(customer_id, routes)
        routes[best_route_idr].insert(best_position, customer_id)

    return routes


def regret_insertion(li, vrp, selected, route1, scheduled):
    while selected:
        regret_values = []
        for customer_id in selected:
            regret_values.append((customer_id, calculate_regret_values(li, vrp, customer_id, route1, scheduled)))
        max_regret_customer_id = max(regret_values, key=lambda x: x[1])[0]

        route1 = insert_customer(li, vrp, max_regret_customer_id, route1, scheduled)
        selected = [customer_id for customer_id in selected if customer_id != max_regret_customer_id]

    return route1


# Randomly choose a set of customers
def change_neighborhood_0(li, vrp, route1, scheduled1, ratio=0.2):
    selected = random.sample(range(1, vrp.number_of_patients + 1), int(ratio * vrp.number_of_patients))
    route1_1 = regret_insertion(li, vrp, selected, route1, scheduled1)
    scheduled1_1 = calculate_actual(route1_1, vrp.travel_matrix, vrp.service_duration)
    return route1_1, scheduled1_1


# A set of customer with the highest removal cost
def change_neighborhood_1(li, vrp, route1, scheduled1, ratio=0.2):
    cost = []
    for i in range(1, vrp.number_of_patients + 1):
        routes_rmd = remove_customer(i, route1)
        scheduled_rmd = calculate_actual(routes_rmd, vrp.travel_matrix, vrp.service_duration)
        temp = calculate_cost_over_samples(li, routes_rmd, scheduled_rmd)
        cost.append((i, temp))
    cost = sorted(cost, key=lambda x: x[1])
    selected = []
    for j in range(int(ratio * vrp.number_of_patients)):
        selected.append(cost[j][0])
    route1_1 = regret_insertion(li, vrp, selected, route1, scheduled1)
    scheduled1_1 = calculate_actual(route1_1, vrp.travel_matrix, vrp.service_duration)
    return route1_1, scheduled1_1


def shake(k, li, vrp, route1, scheduled1, ratio):
    route1_1, schedule1_1 = route1, scheduled1
    if k == 0:
        route1_1, schedule1_1 = change_neighborhood_0(li, vrp, route1, scheduled1, ratio)
    elif k == 1:
        route1_1, schedule1_1 = change_neighborhood_1(li, vrp, route1, scheduled1, ratio)
    else:
        print("Exceed the number of neighborhoods")
    return route1_1, schedule1_1


# Randomly flipping a slice of a route
def ts_opt0(li, vrp, routes, neighbour_num):
    idr = random.randint(0, len(routes) - 1)
    route = routes[idr]
    solution_neighbours = []
    for i in range(0, neighbour_num):
        # Randomly choose 2 points without changing the order
        try:
            endpoints = random.sample(range(1, len(route) - 1), 2)
        except:
            continue
        endpoints.sort()
        temp_route = copy.deepcopy(route)
        temp_route[endpoints[0]:endpoints[1]] = list(reversed(temp_route[endpoints[0]:endpoints[1]]))
        routes[idr] = temp_route
        if routes not in solution_neighbours:
            temp_schedule = calculate_actual(routes, vrp.travel_matrix, vrp.service_duration)
            cost = calculate_cost_over_samples(li, routes, temp_schedule)
            solution_neighbours.append([routes, cost])
    return solution_neighbours


def calculate_arcs(routes):
    arcs = []
    for route in routes:
        for i in range(len(route) - 1):
            arc = (route[i], route[i + 1])
            arcs.append(arc)
    return arcs


def variable_neighborhood_descent(li, vrp, route1, scheduled1, phi):
    tabu_size = int(random.uniform(vrp.number_of_patients, vrp.number_of_patients * 2))
    curr_solution = [route1, calculate_cost_over_samples(li, route1, scheduled1)]
    best_solution = copy.deepcopy(curr_solution)
    tabu_list = list()
    cost_history = list()
    cost_history.append(curr_solution[1])
    for k in range(0, phi):
        neighbour_solution = ts_opt0(li, vrp, curr_solution[0], neighbour_num=100)
        neighbour_solution.sort(key=lambda x: x[1])
        best_neighbour_solution_index = 0
        best_neighbour_solution = neighbour_solution[best_neighbour_solution_index]
        found = False
        find_count = 0
        while (not found) and find_count < len(neighbour_solution):
            curr_solution_arcs = calculate_arcs(curr_solution[0])
            best_neighbour_solution_arcs = calculate_arcs(best_neighbour_solution[0])
            tabu_arcs = [element for element in curr_solution_arcs if element not in best_neighbour_solution_arcs]

            # Not in tabu list, accept, may be suboptimal
            if not set(tabu_arcs) & set(tabu_list):
                found = True
                tabu_list.extend(tabu_arcs)
                curr_solution = best_neighbour_solution
                if best_neighbour_solution[1] < best_solution[1]:
                    best_solution = best_neighbour_solution

            else:
                # Under the amnesty rule, best_neighbour_solution is current_best
                if best_neighbour_solution[1] < best_solution[1]:
                    curr_solution = best_solution
                    best_solution = best_neighbour_solution
                    found = True
                # No optimal, select the suboptimal
                else:
                    best_neighbour_solution_index += 1
                    best_neighbour_solution = neighbour_solution[best_neighbour_solution_index]
            find_count += 1
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)
        cost_history.append(curr_solution[1])
        # print("iterations: %d, current cost:%.2f, best cost:%.2f" % (k, curr_solution[1], best_solution[1]))
    best_route = best_solution[0]
    best_schedule = calculate_actual(best_route, vrp.travel_matrix, vrp.service_duration)
    return best_route, best_schedule
