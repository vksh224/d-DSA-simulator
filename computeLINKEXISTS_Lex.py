import pickle
import numpy
import math

from STB_help import *
from constants import *

def getIndex(ts, currTimeInFile1, currTimeInFile2, currIndexInFile1, currIndexInFile2, linesInFile1, linesInFile2):
    while currTimeInFile1 < ts and currIndexInFile1 < len(linesInFile1):
        currIndexInFile1 += 1
        currTimeInFile1 = float(linesInFile1[currIndexInFile1].split()[0])


    # # Go to ts - Skip all other lines up to ts
    while currTimeInFile2 < ts and currIndexInFile2 < len(linesInFile2):
        currIndexInFile2 += 1
        currTimeInFile2 = float(linesInFile2[currIndexInFile2].split()[0])

    return currIndexInFile1, currIndexInFile2


def CHECK_IF_LINK_EXISTS(file1_pkl, file2_pkl, s, ts, te):

    for time in range(ts, te):

        dataMule1_X = float(file1_pkl[time][0])
        dataMule1_Y = float(file1_pkl[time][1])
        dataMule2_X = float(file2_pkl[time][0])
        dataMule2_Y = float(file2_pkl[time][1])

        if dataMule1_X == -1 or dataMule2_X == -1 or dataMule1_X == '0' or dataMule2_X == '0' or dataMule1_X == ' ' or dataMule2_X == ' ':
            return False

        dist = euclideanDistance(dataMule1_X, dataMule1_Y, dataMule2_X, dataMule2_Y)

        if dist > spectRange[s]:
            return False

    return True


    #
    # with open(filepath1) as f1:
    #     linesInFile1 = f1.readlines()
    # f1.close()
    #
    # with open(filepath2) as f2:
    #     linesInFile2 = f2.readlines()
    # f2.close()
    #
    # currIndexInFile1 = 0
    # currIndexInFile2 = 0
    # currTimeInFile1 = float(linesInFile1[0].split()[0])
    # currTimeInFile2 = float(linesInFile2[0].split()[0])
    #
    # # print("ts: " + str(ts) + " te: " + str(te))
    # # print("First timestamp: " + str(currTimeInFile1) + " " + str(currTimeInFile2))
    #
    # if currTimeInFile1 > ts or currTimeInFile2 > ts:
    #     return False
    #
    # else:
    #     # Go to ts - Skip all other lines up to ts
    #     while currTimeInFile1 < ts and currIndexInFile1 < len(linesInFile1) -1:
    #         currIndexInFile1 += 1
    #         currTimeInFile1 = float(linesInFile1[currIndexInFile1].split()[0])
    #
    #     # # Go to ts - Skip all other lines up to ts
    #     while currTimeInFile2 < ts and currIndexInFile2 < len(linesInFile2) -1:
    #         currIndexInFile2 += 1
    #         currTimeInFile2 = float(linesInFile2[currIndexInFile2].split()[0])
    #
    #     if (currTimeInFile1 != ts or currTimeInFile2 != ts):
    #         #print(currTimeInFile1, currTimeInFile2, ts)
    #         return False
    #
    #     #print(currTimeInFile1, currTimeInFile2, ts)
    #     # Check if these two buses are in range between time period [ts, te]
    #
    #     while currTimeInFile1 < te and currTimeInFile2 < te and currIndexInFile1 < len(linesInFile1) and currIndexInFile2 < len(linesInFile2) and currTimeInFile1 >= ts and currTimeInFile2 >= ts :
    #
    #         line1Arr = linesInFile1[currIndexInFile1].split()
    #         line2Arr = linesInFile2[currIndexInFile2].split()
    #
    #         # print("Here: " + str(currTimeInFile1) + " " + str(currTimeInFile2))
    #         # print(filepath1, filepath2, line1Arr[1], line1Arr[2], line2Arr[1], line2Arr[2], funHaversine(float(line1Arr[3]), float(line1Arr[2]), float(line2Arr[3]), float(line2Arr[2])) )
    #         #if euclideanDistance(float(line1Arr[1]), float(line1Arr[2]), float(line2Arr[1]), float(line2Arr[2])) > spectRange[s]:
    #         dist = funHaversine(float(line1Arr[3]), float(line1Arr[2]), float(line2Arr[3]), float(line2Arr[2]))
    #         # if  '0' in filepath1 and ts == StartTime:
    #         #     print(filepath1, filepath2, str(dist), str(spectRange[s]) )
    #         if dist > spectRange[s]:
    #             # print("Out of range")
    #             return False
    #
    #
    #         ts += 1
    #         if ts != te:
    #             while currTimeInFile1 < ts and currIndexInFile1 < len(linesInFile1) - 1:
    #                 currIndexInFile1 += 1
    #                 currTimeInFile1 = float(linesInFile1[currIndexInFile1].split()[0])
    #
    #             # # Go to ts - Skip all other lines up to ts
    #             while currTimeInFile2 < ts and currIndexInFile2 < len(linesInFile2) - 1:
    #                 currIndexInFile2 += 1
    #                 currTimeInFile2 = float(linesInFile2[currIndexInFile2].split()[0])
    #
    #             if (currTimeInFile1 != ts or currTimeInFile2 != ts):
    #                 # print(currTimeInFile1, currTimeInFile2, ts)
    #                 return False
    #
    #         # currIndexInFile1 += 1
    #         # currIndexInFile2 += 1
    #         # currTimeInFile1 = float(line1Arr[0])
    #         # currTimeInFile2 = float(line2Arr[0])
    #
    #
    #     return True

def createLinkExistenceADJ():
    pkl_files = []
    # fileList = findfiles(DataMule_path + pkl_folder)
    # fileList.sort()
    fileList = []
    file_nums = [i for i in range(V + NoOfDataCenters + NoOfSources)]
    for i in range(len(file_nums)):
        fileList.append(str(i) + ".pkl")



    if ".DS_Store" in fileList:
        fileList.remove(".DS_Store")
        noOfFiles = len(fileList)

    #print("Files " + str(noOfFiles), fileList)
    #print("#ts te i j s \n")

    for ts in range(0, T - dt, dt):
        for te in range(ts + dt, ts + dt + maxTau, dt):
            for file1 in fileList:
                file1_pkl = pickle.load(open(DataMule_path + pkl_folder + file1, "rb"))

                for file2 in fileList:
                    file2_pkl = pickle.load(open(DataMule_path + pkl_folder + file2, "rb"))

                    for s in S:
                        if te < T:
                            ts_dt = int(ts / dt)
                            te_dt = int(te / dt)

                            file1_id = file1.split(".")[0]
                            file2_id = file2.split(".")[0]

                            if int(file1_id) < NoOfSources + NoOfDataCenters and int(file2_id) < NoOfSources  + NoOfDataCenters:
                                break

                            else:
                                # print(file1_id, file2_id)
                                if file1_id == file2_id:
                                    LINK_EXISTS[int(file1_id), int(file2_id), s, ts_dt] = 1
                                else:
                                    # filepath1 = lex_data_directory_day + file1
                                    # filepath2 = lex_data_directory_day + file2

                                    # print("i: " + str(file1_id) + " j: " + str(file2_id) + " s: " + str(s))
                                    if CHECK_IF_LINK_EXISTS(file1_pkl, file2_pkl, s, ts, te) == True:
                                        LINK_EXISTS[int(file1_id), int(file2_id), s, ts_dt] = 1

                                  #  print("i: " + str(file1_id) + " j: " + str(file2_id) + " s: " + str(s) + " ts: " + str(ts_dt) + " te: " + str(te_dt) + " = " + str(LINK_EXISTS[int(file1_id), int(file2_id), s, ts_dt, te_dt]))

# Main starts here

# This function is independent of tau
LINK_EXISTS = numpy.empty(shape=(V + NoOfDataCenters + NoOfSources, V + NoOfDataCenters + NoOfSources, numSpec, int(T/dt)))
LINK_EXISTS.fill(math.inf)

# if not os.path.exists(lex_data_directory):
#     os.makedirs(lex_data_directory)

createLinkExistenceADJ()

if not os.path.exists(path_to_folder):
    os.makedirs(path_to_folder)

LE_file = open(link_exists_folder + "LINK_EXISTS.pkl", 'wb')
pickle.dump(LINK_EXISTS, LE_file, protocol = 4)
LE_file.close()

print("Size of Link Exists: " + str(len(LINK_EXISTS)) + " " + str(len(LINK_EXISTS[0])) + " " + str(len(LINK_EXISTS[0][0])) + " " + str(len(LINK_EXISTS[0][0][0])))
save_in_file(link_exists_folder + "LINK_EXISTS.txt", LINK_EXISTS)
#printMAT(LINK_EXISTS)


