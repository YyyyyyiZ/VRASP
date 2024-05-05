import numpy as np
from scipy import stats


class Patient:
    def __init__(self):
        self.index = 9999
        self.location = (0, 0)
        self.service_duration = 0
        self.scheduled_start = 0
        self.actual_start = 0

    def gen_service_duration(self, start=30, end=90, data_num=1):
        mu = np.random.uniform(low=50, high=70, size=1)[0]
        sigma = mu * 0.5
        norm_lower = np.log(start)
        norm_upper = np.log(end)
        X = stats.truncnorm((norm_lower - mu) / sigma, (norm_upper - mu) / sigma, loc=mu, scale=sigma)
        norm_data = X.rvs(data_num)
        log_data = np.exp(norm_data)
        service_duration = log_data[0]
        return service_duration

    def data_as_string(self):
        return " ".join([str(self.index), str(self.location), str(self.service_duration), str(self.scheduled_start),
                         str(self.actual_start)])


class ServiceInstance:
    def __init__(self, size, num_crew, length, cost_matrix, travel_matrix, service_duration, cf, co, ct):
        self.number_of_patients = size
        self.number_of_crew = num_crew
        self.list_of_patients = []
        self.length_of_city = 50
        self.width_of_city = 50
        self.clinic_location = (0, 0)
        self.work_minutes = length
        self.cost_matrix = cost_matrix
        self.travel_matrix = travel_matrix
        self.service_duration = service_duration
        self.cf = cf
        self.co = co
        self.ct = ct

    def create_patient_data(self, count):
        for i in range(0, count):
            patient = Patient()
            patient.index = i
            patient.location = self.gen_location()
            self.list_of_patients.append(patient)

    def gen_location(self):
        x = np.round(np.random.uniform(low=0, high=50, size=1)[0])
        y = np.round(np.random.uniform(low=0, high=50, size=1)[0])
        return x, y

    def distance(self, point1, point2):
        dist = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        return dist

    def gen_matrix(self):
        travel_matrix = [[] for _ in range(0, len(self.list_of_patients) + 2)]
        cost_matrix = [[] for _ in range(0, len(self.list_of_patients) + 2)]
        l1 = [(0, 0)] + [(one.location[0], one.location[1]) for one in self.list_of_patients] + [(0, 0)]
        for i in range(0, len(l1)):
            for j in range(0, len(l1)):
                distance = self.distance(l1[i], l1[j])
                travel_matrix[i].append(round(distance * np.random.uniform(low=0.5, high=1.5, size=1)[0]))
                cost_matrix[i].append(round(distance * 0.5))
        return travel_matrix, cost_matrix

class VRASPDataModel:
    def __init__(self):
        self.num_vehicles = 0
        self.depot = 0
        self.service_times = []