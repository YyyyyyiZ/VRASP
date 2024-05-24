import argparse
import numpy as np
from docplex.mp.model import Model
from utils.readwrite import read_txt
import time


def avg_array(matrix):
    matrix = np.array(matrix)
    col_avg = np.mean(matrix, axis=0)
    return col_avg.tolist()


def saa(size, cost_matrix, service_duration, travel_matrix, cf=100, co=1, ct=2, length=480, num_samples=30):
    mdl = Model("CPLEX SAA")
    service_duration = np.array([[0] + line + [0] for line in service_duration])
    travel_matrix = np.array(travel_matrix)
    cost_matrix = np.array(cost_matrix)
    # print(service_duration, travel_matrix, cost_matrix)

    N = [i for i in range(1, size + 1)]  # customer set
    K = [i for i in range(1, int(np.ceil(size / 6.0) + 1))]  # crew set
    V = [0] + N + [size + 1]  # all vertices, {start} ∪ {customer set} ∪ {end}
    A = [(i, j) for i in V for j in V if j != i]  # arcs between vertices
    cf = cf
    M = 99999

    A_crew = [(k, i, j) for k in K for i, j in A]
    S_time = [i for i in V]
    A_time = [(sample, i) for sample in range(num_samples) for i in V]
    W_time = [(sample, i) for sample in range(num_samples) for i in V]
    O_time = [(sample, k) for sample in range(num_samples) for k in K]
    x = mdl.binary_var_dict(A_crew, name='x')
    s = mdl.continuous_var_dict(S_time, name='scheduled')
    # x, service, travel → a
    #                      +
    #                      s → w, o
    a = mdl.continuous_var_dict(A_time, name='actual')
    w = mdl.continuous_var_dict(W_time, name='wait')
    o = mdl.continuous_var_dict(O_time, name='overtime')

    # Constraints
    # (2)
    mdl.add_constraints(mdl.sum(x[k, i, j] for k in K for j in V if j != i) == 1 for i in N)
    # (3)
    mdl.add_constraints(mdl.sum(x[k, 0, j] for j in V if j != 0) == 1 for k in K)
    # (4)
    mdl.add_constraints(mdl.sum(x[k, i, size + 1] for i in V if i != (size + 1)) == 1 for k in K)
    # (5)
    mdl.add_constraints(
        mdl.sum(x[k, i, h] for i in V if i != h) == mdl.sum(x[k, h, j] for j in V if j != h) for h in N for k in K)
    # # (6)
    # mdl.add_constraints(s[i] <= length for i in V)
    # Sample constraints
    for idx in range(num_samples):
        # (7)
        mdl.add_constraints(
            s[i] + service_duration[idx][i] + travel_matrix[idx][i, j] - M * (1 - x[k, i, j]) <= s[j] for k in K for
            i, j in A)
        # (8)
        for k, i, j in A_crew:
            if i != size + 1:
                mdl.if_then(x[k, i, j] == 1,
                            a[idx, j] == mdl.max(a[idx, i], s[i]) + service_duration[idx][i] + travel_matrix[idx][i, j])
        # (9)
        mdl.add_constraints(w[idx, i] == mdl.max(a[idx, i] - s[i], 0) for i in V)
        # (10)
        mdl.add_constraints(
            s[i] + service_duration[idx, i] + travel_matrix[idx, i, size + 1] - M * (
                    1 - x[k, i, size + 1]) - length <= o[idx, k] for k in K for i in N)

    # Objective (1)
    mdl.minimize(mdl.sum(cf * x[k, 0, j] for k in K for j in V if j != 0) +
                 mdl.sum(cost_matrix[i, j] * x[k, i, j] for k, i, j in A_crew) +
                 mdl.sum(ct * w[idx, i] for idx, i in W_time) / num_samples +
                 mdl.sum(co * o[idx, k] for idx, k in O_time) / num_samples)

    # Solve
    solution = mdl.solve()
    if solution:
        print(solution)
        actual = dict()
        travel = []
        for idx in range(num_samples):
            for k, i, j in A_crew:
                if i != size + 1:
                    if solution.get_value(x[(k, i, j)]) == 1:
                        if solution.get_value(a[(idx, i)]) > solution.get_value(s[i]):
                            temp = solution.get_value(a[(idx, i)]) + service_duration[idx][i] + travel_matrix[idx][i, j]
                        else:
                            temp = solution.get_value(s[i]) + service_duration[idx][i] + travel_matrix[idx][i, j]
                        key1 = 'actual_' + str(idx) + '_' + str(j)
                        actual[key1] = temp
                        travel.append(travel_matrix[idx][i, j])
        print(actual)
        print("Travel cost:{}".format(sum(travel) / len(travel)))

    else:
        print("No solution found.")


def deterministic(size, cost_matrix, service_duration, travel_matrix, cf=100, co=1, ct=3, length=480, num_samples=30):
    # Average service_time and travel_time in samples to obtain an estimate
    cost_matrix = np.array(cost_matrix)
    avg_travel = np.array(avg_array(travel_matrix))
    avg_service = np.array([0] + avg_array(service_duration) + [0])

    mdl = Model("CPLEX Deterministic")
    N = [i for i in range(1, size + 1)]  # customer set
    K = [i for i in range(1, int(np.ceil(size / 6.0) + 1))]  # crew set
    V = [0] + N + [size + 1]  # all vertices, {start} ∪ {customer set} ∪ {end}
    A = [(i, j) for i in V for j in V if j != i]  # arcs between vertices
    cf = cf
    M = 99999

    # Decision variable
    A_crew = [(k, i, j) for k in K for i, j in A]
    S_time = [i for i in V]
    A_time = [i for i in V]
    W_time = [i for i in N]
    O_time = [k for k in K]
    x = mdl.binary_var_dict(A_crew, name='x')
    s = mdl.continuous_var_dict(S_time, name='scheduled')
    # x, service, travel → a
    #                      +
    #                      s → w, o
    a = mdl.continuous_var_dict(A_time, name='actual')
    w = mdl.continuous_var_dict(W_time, name='wait')
    o = mdl.continuous_var_dict(O_time, name='overtime')

    # Objective (1)
    mdl.minimize(mdl.sum(cf * x[k, 0, j] for k in K for j in V if j != 0) +
                 mdl.sum(cost_matrix[i, j] * x[k, i, j] for k, i, j in A_crew) +
                 mdl.sum(ct * w[i] for i in W_time) + mdl.sum(co * o[k] for k in O_time))

    # Constraints
    # (2)
    mdl.add_constraints(mdl.sum(x[k, i, j] for k in K for j in V if j != i) == 1 for i in N)
    # (3)
    mdl.add_constraints(mdl.sum(x[k, 0, j] for j in V if j != 0) == 1 for k in K)
    # (4)
    mdl.add_constraints(mdl.sum(x[k, i, size + 1] for i in V if i != (size + 1)) == 1 for k in K)
    # (5)
    mdl.add_constraints(
        mdl.sum(x[k, i, h] for i in V if i != h) == mdl.sum(x[k, h, j] for j in V if j != h) for h in N for k in K)
    # # (6)
    # mdl.add_constraints(s[i] <= length for i in V)
    # (7)
    mdl.add_constraints(
        s[i] + avg_service[i] + avg_travel[i, j] - M * (1 - x[k, i, j]) <= s[j] for k in K for i, j in A)
    # (8)
    for k, i, j in A_crew:
        if i != size + 1:
            mdl.if_then(x[k, i, j] == 1,
                        a[j] == mdl.max(a[i], s[i]) + avg_service[i] + avg_travel[i, j])
    # (9)
    mdl.add_constraints(w[i] == (mdl.max(a[i], s[i]) - s[i]) for i in N)
    # (10)
    mdl.add_constraints(
        s[i] + avg_service[i] + avg_travel[i, size + 1] - M * (1 - x[k, i, size + 1]) - length <= o[k] for k in K for i
        in N)

    # Solve
    solution = mdl.solve()
    if solution:
        print(solution)
        actual = dict()
        travel = dict()
        for k, i, j in A_crew:
            if i != size + 1:
                if solution.get_value(x[(k, i, j)]) == 1:
                    if solution.get_value(a[i]) > solution.get_value(s[i]):
                        temp = solution.get_value(a[i]) + avg_service[i] + avg_travel[i, j]
                    else:
                        temp = solution.get_value(s[i]) + avg_service[i] + avg_travel[i, j]
                    key1 = 'actual_' + str(j)
                    actual[key1] = temp
                    key2 = 'travel_' + str(i) + '_' + str(j)
                    actual[key2] = avg_travel[i, j]
                    print(actual)
                    print(travel)
    else:
        print("No solution found.")


def main(size, instance_id, total_samples, num_samples, isSaa=True, cf=100, co=1, ct=3, length=480):
    """
    for each sample group in each instance, average the service duration and travel time
    :param size: number of customers, [10, 20, 30, 40]
    :param instance_id: id of instance, from 1 to 10
    :param total_samples: number of all available samples, > num_samples
    :param num_samples: number of samples for SAA, [30, 50, 80, 100]
    :param isSaa: SAA method if True otherwise deterministic method
    :param cf: fixed cost
    :param co: unit work overtime cost
    :param ct: unit lateness cost
    :param length: work time
    """

    # Load generated data
    cost_matrix, service_duration, travel_matrix, _, _ = read_txt(size=size, ids=instance_id,
                                                                  total_samples=total_samples,
                                                                  num_samples=num_samples)

    if isSaa:
        saa(size, cost_matrix, service_duration, travel_matrix, cf, co, ct, length, num_samples)

    else:
        deterministic(size, cost_matrix, service_duration, travel_matrix, cf, co, ct, length, num_samples)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='VRASP CPLEX solver')
    parser.add_argument('--size', default=10, type=int, help='problem size')
    parser.add_argument('--instance', default=10, type=int, help='number of instance')
    parser.add_argument('--total_samples', default=100, type=int, help='number of all available samples')
    parser.add_argument('--num_samples', default=10, type=int, help='number of samples')
    parser.add_argument('--isSAA', default=True, type=bool, help='SAA or deterministic')
    parser.add_argument('--cf', default=100, type=int, help='fixed cost')
    parser.add_argument('--co', default=1, type=int, help='unit work overtime cost')
    parser.add_argument('--ct', default=2, type=int, help='unit lateness cost')
    parser.add_argument('--length', default=480, type=int, help='total work time')
    args = parser.parse_args()

    # Print arguments
    for k, v in vars(args).items():
        print(k, '=', v)

    time_list = []
    for ids in range(args.instance):
        start_time = time.time()
        main(size=args.size, instance_id=ids + 1, total_samples=args.total_samples, num_samples=args.num_samples,
             isSaa=args.isSAA, cf=args.cf, co=args.co, ct=args.ct, length=args.length)
        end_time = time.time()
        print("Instance Running Time：{}".format(end_time - start_time))
        time_list.append(end_time - start_time)
    print("Average Running Time：{}".format(sum(time_list) / len(time_list)))
