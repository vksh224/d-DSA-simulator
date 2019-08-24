import numpy
import math
import pickle
from constants import *



# Initialize the 5-D adjacency matrix where the value is 1 if
# node i and j are in communication range for a time period [ts, te] over any band s in the set S
# Assumption 1: Spectrum power and transmission range does not change
# Assumption 2: Only Spectrum bandwidth changes over time and location (i.e., at different nodes)
# Assumption 3: However given a bandwidth of a certain band at time t,
# it remains constant for the duration of transmission delay for any message
# Compute message colors (i.e., message transmission delays) for one spatial links and temporal links

# Compute message colors (i.e., message transmission delays) for spatial links (ONLY SPATIAL LINKS)
def computeADJ_T_2(specBW, LINK_EXISTS):
    ADJ_T = numpy.empty(shape=(V + NoOfDataCenters + NoOfSources, V+ NoOfDataCenters + NoOfSources, T, len(M)))
    ADJ_T.fill(math.inf)

    ADJ_E = numpy.empty(shape=(V+ NoOfDataCenters + NoOfSources, V+ NoOfDataCenters + NoOfSources, T, len(M)))
    ADJ_E.fill(math.inf)

    Parent = numpy.empty(shape=(V+ NoOfDataCenters + NoOfSources, V+ NoOfDataCenters + NoOfSources, T, len(M)), dtype=int)
    Parent.fill(-1)

    Spectrum = numpy.empty(shape=(V+ NoOfDataCenters + NoOfSources, V+ NoOfDataCenters + NoOfSources, T, len(M)), dtype=int)
    Spectrum.fill(-1)

    # print ("M   i  j  s  ts  te :  Val  cT  LExi   BW    ")
    for m in range(len(M)):
        for t in range(T - tau, -1, -tau):
            for i in range(V+ NoOfDataCenters + NoOfSources):
                for j in range(V+ NoOfDataCenters + NoOfSources):

                    if i == j:
                        ADJ_T[i, j, t, m] = tau
                        ADJ_E[i, j, t, m] = epsilon
                        Spectrum[i, j, t, m] = 10
                        Parent[i, j, t, m] = i

                    else:
                        for s in S:
                            #bandwidth = 0 means there does not exist a link over that spectrum band
                            if specBW[i, j, s, t] > 0:
                                # numerator = math.ceil(M[m] / (60* specBW[i, j, s, t])) * (t_sd + idle_channel_prob * t_td)
                                # consumedTime = tau * math.ceil(numerator/tau)

                                transmission_time = M[m]/specBW[i, j, s, t] #in seconds
                                consumedTime = math.ceil(transmission_time/num_sec_per_tau) #in minutes


                                sensing_energy = math.ceil(M[m] / (specBW[i, j, s, t])) * t_sd * sensing_power
                                switching_energy_total = math.ceil(M[m] / (specBW[i, j, s, t])) * idle_channel_prob * switching_energy
                                transmission_energy = math.ceil(M[m]/specBW[i, j, s, t]) * idle_channel_prob * t_td * spectPower[s]

                                consumedEnergy = sensing_energy + switching_energy_total + transmission_energy
                                consumedEnergy = round(consumedEnergy, 2)

                                # print(i, j, t, consumedTime, m, specBW[i, j, s, t])
                                if (t + consumedTime) < T and LINK_EXISTS[i, j, s, t] < math.inf:

                                    currSpec = Spectrum[i, j, t, m]
                                    if currSpec > 9:
                                        currSpec = currSpec % 10

                                    currSpec = currSpec- 1

                                    if ADJ_T[i, j, t, m] > consumedTime or (ADJ_T[i, j, t, m] == consumedTime and currSpec > -1 and spectRange[s] > spectRange[currSpec]):
                                    # if ADJ_T[i, j, t, m] > consumedTime:
                                        ADJ_T[i, j, t, m] = consumedTime
                                        ADJ_E[i, j, t, m] = consumedEnergy
                                        Spectrum[i, j, t, m] = s + 1
                                        Parent[i, j, t, m] = i

                    if (t + tau) < T and ADJ_T[i, j, t, m] > ADJ_T[i, j, (t + tau), m] + tau and ADJ_T[i, j, (t + tau), m] != math.inf:
                        ADJ_T[i, j, t, m] = ADJ_T[i, j, (t + tau), m] + tau
                        ADJ_E[i, j, t, m] = ADJ_E[i, j, (t + tau), m] + epsilon
                        Parent[i, j, t, m] = Parent[i, j, t + tau, m]
                        Spectrum[i, j, t, m] = Spectrum[i, j, t + tau, m] + 10



    return ADJ_T, Parent, Spectrum, ADJ_E


# Determines the Least Latency Cost (LLC) Path for all messages in the STB graph
def LLC_PATH_ADJ_2(ADJ_T, ADJ_E, Parent, Spectrum, V, T, M):

    #print("k i j t : LLC Parent")
    for m in range(len(M)):
        for k in range(V+ NoOfDataCenters + NoOfSources):
            for i in range(V+ NoOfDataCenters + NoOfSources):
                for j in range(V+ NoOfDataCenters + NoOfSources):
                    for t in range(0, T, tau):
                        # leastTime = LLC_PATH[i, j, t, m]
                        # leastTime = math.inf

                        dcurr = ADJ_T[i, j, t, m]
                        d2 = math.inf
                        e2 = math.inf
                        # dalt = math.inf

                        d1 = ADJ_T[i, k, t, m]
                        e1 = ADJ_E[i, k, t, m]
                        if d1 < math.inf and (t + d1) < T:
                            d2 = ADJ_T[k, j, (t + int(d1)), m]
                            e2 = ADJ_E[k, j, (t + int(d1)), m]

                        if d1 + d2 < dcurr:
                            ADJ_T[i, j, t, m] = d1 + d2
                            ADJ_E[i, j, t, m] = e1 + e2
                            Parent[i, j, t, m] = Parent[k, j, (t + int(d1)), m]
                            Spectrum[i, j, t, m] = Spectrum[k, j, (t + int(d1)), m]
                            # if i == 4 and j == 11 and t  == 12:
                            #     print(str(k) + " " + str(i) + " " + str(j) + " " + str(t) + " : " + str(
                            #                     ADJ_T[i, j, t, m]) + " " + str(Parent[i, j, t, m]))

    return ADJ_T, Parent, Spectrum, ADJ_E


def PRINT_LLC_PATH_FILE_3(LLC_PATH, ELC_PATH, Parent, Spectrum, ADJ_T):

    file = open(path_to_save_LLC + "LLC_PATH.txt", "w")
    file2 = open(path_to_save_LLC + "LLC_PATH_Spectrum.txt", "w")
    file3 = open(path_to_save_LLC + "LLC_Spectrum.txt", "w")
    file4 = open(path_to_save_LLC + "LLC_time.txt", "w")

    file.write("#i\tj\tt\tm:\tPATH\n")
    file2.write("#i\tj\tt\tm:\tPATH\n")
    file3.write("#i\tj\tt\tm:\tPATH\n")
    file4.write("#i\tj\tt\tm:\tPATH\n")

    for m in range(len(M)):
        for t in range(0, T, tau):
            for i in range(V+ NoOfDataCenters + NoOfSources):
                for j in range(V+ NoOfDataCenters + NoOfSources):
                    if i == j:
                        continue
                    if LLC_PATH[i, j, t, m] != math.inf:
                        par_u = int(Parent[i, j, t, m])

                        print_path_str = str(j) + " (" + str(Spectrum[i, j, t, m]) + ")\t"
                        path_str = str(j) + "\t"
                        spec_str = str(Spectrum[i, j, t, m]) + "\t"
                        time_str = str(int(ADJ_T[i, j, t, m])) + "\t"

                        temp_spec_val = Spectrum[i, j, t, m]

                        # while temp_spec_val > 10:
                        #     temp_spec_val -= 10
                        #     path_str += str(par_u) + "\t"
                        #     spec_str += str(temp_spec_val) + "\t"
                        #     time_str += "1\t"
                        #     print_path_str += str(par_u) + " (" + str(temp_spec_val) + ")  "

                        while par_u != -1 and t < T and par_u != i:
                            path_str += str(par_u) + "\t"
                            print_path_str += str(par_u) + " (" + str(Spectrum[i, par_u, t, m]) + ")\t"
                            spec_str += str(Spectrum[i, par_u, t, m]) + "\t"
                            time_str += str(int(ADJ_T[i, par_u, t, m])) + "\t"

                            #Get the value earlier than updating par_u
                            temp_spec_val = Spectrum[i, par_u, t, m]

                            par_u = int(Parent[i, par_u, t, m])

                            # while temp_spec_val > 10:
                            #     temp_spec_val -= 10
                            #     path_str += str(par_u) + "\t"
                            #     spec_str += str(temp_spec_val) + "\t"
                            #     time_str += "1\t"
                            #     print_path_str += str(par_u) + " (" + str(temp_spec_val) + ")\t"


                        path_str += str(i)
                        print_path_str += str(i) +"\t"

                        file.write(str(i) + "\t" + str(j) + "\t" + str(t) + "\t" + str(M[m]) + "\t" + str(int(LLC_PATH[i, j, t, m])) + "\t" + path_str + "\n")
                        file2.write(
                            str(i) + "\t" + str(j) + "\t" + str(t) + "\t" + str(M[m]) + "\t" + str(ELC_PATH[i, j, t, m]) + "\t" + str(
                                int(LLC_PATH[i, j, t, m])) + "\t" + print_path_str + "\n")
                        file3.write(str(i) + "\t" + str(j) + "\t" + str(t) + "\t" + str(M[m]) + "\t" + str(int(LLC_PATH[i, j, t, m])) + "\t" + spec_str + "\n")
                        file4.write(str(i) + "\t" + str(j) + "\t" + str(t) + "\t" + str(M[m]) + "\t" + str(
                            int(LLC_PATH[i, j, t, m])) + "\t" + time_str + "\n")

    file.close()
    file2.close()
    file3.close()
    file4.close()

