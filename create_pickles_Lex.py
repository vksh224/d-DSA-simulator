import os
import pickle
from constants import *


def get_dataMule_ID(filename):
    file_arr = filename.split(".")
    return file_arr[0]



def find_index(t, lines):
    index = 0
    line_arr = lines[index].strip().split()
    time = float(line_arr[0])

    while time < t and index < len(lines) - 1:
        index += 1
        line_arr = lines[index].strip().split()
        time = float(line_arr[0])

    x = line_arr[2]

    if x == '0':
        while time == t and x == '0'  and index < len(lines) - 1:
            index += 1
            line_arr = lines[index].strip().split()
            time = float(line_arr[0])
            x = line_arr[2]

    if time == t:
        return index
    else:
        return -1


dataMules = os.listdir(DataMule_path + "Day" + str(day_num))
dataMules.sort()
# print(dataMules)

for bus in dataMules:

    if not os.path.exists(DataMule_path + pkl_folder):
        os.makedirs(DataMule_path + pkl_folder)

    # print(bus)

    coord_at_time = []

    with open(DataMule_path + "Day" + str(day_num) + "/" + bus, 'r') as f:
        lines = f.readlines()[1:]
    f.close()

    file_len = len(lines)

    for t in range(StartTime, StartTime + T + 1):

        index = find_index(t, lines)
        if index != -1:
            line_arr = lines[index].strip().split()
            coord = [line_arr[1], line_arr[2]]
        else:
            coord = [-1, -1]

        coord_at_time.append(coord)

    filename = get_dataMule_ID(bus)
    filename = filename + ".pkl"

    # print(coord_at_time)

    pickle_file = open(DataMule_path + pkl_folder + filename, 'wb')
    pickle.dump(coord_at_time, pickle_file, protocol=4)
    pickle_file.close()





