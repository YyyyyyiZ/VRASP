import time
import argparse
from utils.readwrite import read_txt
from vns_de.vns_solver_de import deterministic
from vns_saa.vns_solver_saa import saa


def main(size, instance_id, total_samples, num_samples, isSaa=True, cf=100, co=1, ct=3, length=480, max_iter=1000,
         k_max=4, ts_iter=30, ratio=0.2):
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
    :param max_iter: maximum number of iterations in VNS
    :param k_max: number of neighborhoods in VNS
    :param ts_iter: max iteration of local search
    :param ratio: Ratio of customers in Neighborhood
    """

    # Load generated data
    # cost_matrix, service_duration, travel_matrix, x_coord, y_coord = read_txt(size=size,
    # ids=instance_id, total_samples=total_samples, num_samples=num_samples)
    cost_matrix, service_duration, travel_matrix, _, _ = read_txt(size=size, ids=instance_id,
                                                                  total_samples=total_samples, num_samples=num_samples)

    if isSaa:
        # saa(size, cost_matrix, service_duration, travel_matrix, x_coord, y_coord, cf, co, ct, length, num_samples)
        saa(size, cost_matrix, service_duration, travel_matrix, cf, co, ct, length, num_samples,
            max_iter, k_max, ts_iter, ratio)

    else:
        # deterministic(size, cost_matrix, service_duration, travel_matrix, x_coord, y_coord, cf, co, ct, length,
        # num_samples)
        deterministic(size, cost_matrix, service_duration, travel_matrix, cf, co, ct, length, num_samples,
                      max_iter, k_max, ts_iter, ratio)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='VRASP VNS solver')
    parser.add_argument('--size', default=5, type=int, help='problem size')
    parser.add_argument('--instance', default=10, type=int, help='number of instance')
    parser.add_argument('--total_samples', default=100, type=int, help='number of all available samples')
    parser.add_argument('--num_samples', default=80, type=int, help='number of samples')
    parser.add_argument('--isSAA', default=True, type=bool, help='SAA or deterministic')
    parser.add_argument('--cf', default=100, type=int, help='fixed cost')
    parser.add_argument('--co', default=1, type=int, help='unit work overtime cost')
    parser.add_argument('--ct', default=2, type=int, help='unit lateness cost')
    parser.add_argument('--length', default=480, type=int, help='total work time')

    parser.add_argument('--max_iter', default=100, type=int, help='max iteration of VNS')
    parser.add_argument('--k_max', default=2, type=int, help='number of neighborhood')
    parser.add_argument('--ts_iter', default=100, type=int, help='max iteration of local search')
    parser.add_argument('--ratio', default=0.2, type=int, help='ratio of customers in Neighborhood')
    args = parser.parse_args()

    # Print arguments
    for k, v in vars(args).items():
        print(k, '=', v)

    time_list = []
    for ids in range(args.instance):
        start_time = time.time()
        main(size=args.size, instance_id=ids + 1, total_samples=args.total_samples, num_samples=args.num_samples,
             isSaa=args.isSAA, cf=args.cf, co=args.co, ct=args.ct, length=args.length, max_iter=args.max_iter,
             k_max=args.k_max, ts_iter=args.ts_iter, ratio=args.ratio)
        end_time = time.time()
        print("Instance Running Time：{}".format(end_time - start_time))
        print(
            "--------------------------------------------------------------------------------------------------------")
        time_list.append(end_time - start_time)
    print("Average Running Time：{}".format(sum(time_list) / len(time_list)))