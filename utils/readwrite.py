def read_txt(size=10, ids=1, total_samples=100, num_samples=30):
    service = []
    travel = []
    cost_matrix = []
    for idp in range(num_samples):
        filename = ("size_" + str(size) + "/" + "instance_" + str(ids) + "/" +
                    str(total_samples) + "samples_" + str(idp + 1) + ".txt")
        path = "./experiment/" + filename
        with open(path, "r") as f:
            one_sample = f.readlines()
            service_duration = [float(oneline[:-1].split()[3]) for oneline in one_sample[3: 3 + size]]
            x_coord = [float(oneline[:-1].split()[1][1:-1]) for oneline in one_sample[3: 3 + size]]
            y_coord = [float(oneline[:-1].split()[2][:-1]) for oneline in one_sample[3: 3 + size]]
            cost_matrix = [list(map(float, oneline[:-1].split())) for oneline in one_sample[4 + size: 4 + 2*size + 2]]
            travel_matrix = [list(map(float, oneline.strip("\n").split())) for oneline in one_sample[7 + 2*size:]]
            service.append(service_duration)
            travel.append(travel_matrix)
        f.close()
    return cost_matrix, service, travel, x_coord, y_coord
