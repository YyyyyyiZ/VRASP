from math import ceil, sqrt
from data_model import Patient, ServiceInstance
import numpy as np


def write_instance(instance, ids, total_sample, id_sample):
    filename = ("size_" + str(instance.number_of_patients) + "/" +
                "instance_" + str(ids) + "/" + str(total_sample) + "samples_" + str(id_sample) + ".txt")
    download_dir = "../experiment/" + filename
    text = open(download_dir, "w")

    patients = instance.list_of_patients
    lines = [str(instance.number_of_crew), str(instance.number_of_patients)]

    lines.append(",")
    for patient in patients:
        line = " ".join(
            [str(patient.index), str(patient.location), str(patient.service_duration)])
        lines.append(line)

    lines.append(",")
    for row in instance.cost_matrix:
        lines.append(" ".join(list(map(str, row))))

    lines.append(",")
    for row in instance.travel_matrix:
        lines.append(" ".join(list(map(str, row))))

    text.write('\n'.join(lines))
    text.close()
    return


if __name__ == '__main__':
    number_of_patients = [5, 10, 20, 30, 40]
    number_of_crew = [ceil(i / 6.0) for i in number_of_patients]
    number_of_instance = 10
    number_of_samples = [30, 50, 80, 100]

    for idx, val in enumerate(number_of_patients):
        for ids in range(number_of_instance):
            # deterministic
            instance = ServiceInstance()
            instance.number_of_patients = number_of_patients[idx]
            instance.number_of_crew = number_of_crew[idx]
            # index and location
            instance.create_patient_data(instance.number_of_patients)
            instance.cost_matrix = instance.gen_matrix()[1]
            for total_sample in number_of_samples[-1:]:
                for id_sample in range(total_sample):
                    # stochastic
                    # different realization of travel time and service duration in each sample
                    instance.travel_matrix = instance.gen_matrix()[0]
                    for one in instance.list_of_patients:
                        one.service_duration = np.round(one.gen_service_duration())
                    write_instance(instance, ids+1, total_sample, id_sample + 1)
