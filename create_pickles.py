import os
import pickle
from constants import *
from STB_help import *


def get_dataMule_ID(filename):
    if filename[1] == '.':
        return filename[0]
    else:
        return filename[0:2]

def get_dataMule_ID_flip(filename, num_nodes):
    filename = filename.split(".")
    file_num = int(filename[0])
    new_file_num = (file_num - num_nodes) * -1
    print("old:", file_num, "new:", new_file_num)
    return str(new_file_num)

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



days = ["1","2"]
startTime = [StartTime, StartTime + T]



for j in range(len(days)):
    dataMules = findfiles(DataMule_path + "Day" + str(j + 1) + "/")
    dataMules.sort()
    print(dataMules)

    for bus in dataMules:

        if not os.path.exists(DataMule_path + "Day" + str(days[j]) + "_pkl" ):
            os.makedirs(DataMule_path + "Day" + str(days[j]) + "_pkl" )

        coord_at_time = []

        with open(DataMule_path + "Day" + str(j + 1) + "/" + bus, 'r') as f:
            lines = f.readlines()
        f.close()

        file_len = len(lines)



        for t in range(startTime[j], startTime[j] + T + 1):

            index = find_index(t, lines)
            if index != -1:
                line_arr = lines[index].strip().split()
                coord = [line_arr[2], line_arr[3]]
            else:
                coord = [-1, -1]

            coord_at_time.append(coord)

        filename = get_dataMule_ID(bus)
        filename = filename + ".pkl"

        # print(coord_at_time)

        pickle_file = open(DataMule_path + "/Day" + days[j] + "_pkl/" + filename, 'wb')
        pickle.dump(coord_at_time, pickle_file, protocol=4)
        pickle_file.close()





