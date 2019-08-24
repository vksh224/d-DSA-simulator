import numpy as np
import matplotlib.pyplot as plt
from constants import *

time_epochs = 4

msg_files = 1
puser_files = 1

# arrays for broadcast
# arrays for broadcast
Epidemic = np.zeros(shape=(time_epochs, msg_files, puser_files))
Geographic = np.zeros(shape=(time_epochs, msg_files, puser_files))
SnW = np.zeros(shape=(time_epochs, msg_files, puser_files))


num_mules = 92
# num_channels = 5
num_Pusers = 200
msg_mean = 15
T = 360
channels = 6
ttl = 180
max_memory = 100
startTime = 1
days = "50"
dataset = "Lexington"
buffer_type = "FIFO"
weight = "weighted_0.5"
protocols = ["broadcast", "geo_1", "SnW_20"]
# protocols = ["Epidemic_Smart_optimistic"]
# fwd_strat = ["geo_3"]
num_replicas = 5
metrics_file = "metrics.txt"
sim_round = 6

p_id = 4 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

for i in range(msg_files):
    for j in range(puser_files):
        for protocol in protocols:
            t = 0

            path = "DataMules/" + dataset + "/" + days + "/" + str(sim_round) + "/Link_Exists/LE_" + str(startTime) + \
                   "_" + str(T) + "/Epidemic_Smart_" + weight + "/" + buffer_type + "/" + protocol + "/mules_" + \
                   str(num_mules) + "/channels_" + str(channels) + "/P_users_" + str(num_Pusers) + \
                   "/msgfile_" + str(i) + "_" + str(msg_mean)+ "/puserfile_" + str(j) + "/TTL_" + str(ttl) + "/BuffSize_" + str(max_memory) + "/"


            with open(path + metrics_file, "r") as f:
                lines = f.readlines()[1:]

            for line in lines:

                if "broadcast" in protocol:
                    Epidemic[t, i, j] = float(line)
                elif "geo" in protocol:
                     Geographic[t, i, j] = float(line)
                elif "SnW" in protocol:
                     SnW[t, i, j] = float(line)

                t += 1



Epi_mean = []
Epi_sd = []
Geo_mean = []
Geo_sd = []
SnW_mean = []
SnW_sd = []


Epi_temp = []
Geo_temp = []
SnW_temp = []


for t in range(len(Epidemic)):

    t_arr_Epi = []
    t_arr_Geo = []
    t_arr_SnW = []


    for i in range(len(Epidemic[t])):
        for j in range(len(Epidemic[t][i])):
            t_arr_Epi.append(Epidemic[t, i, j])
            t_arr_Geo.append(Geographic[t, i, j])
            t_arr_SnW.append(SnW[t, i, j])


    Epi_temp.append(t_arr_Epi)
    Geo_temp.append(t_arr_Geo)
    SnW_temp.append(t_arr_SnW)


for i in range(len(Epi_temp)):
    Epi_mean.append(np.mean(Epi_temp[i]))
    Geo_mean.append(np.mean(Geo_temp[i]))
    SnW_mean.append(np.mean(SnW_temp[i]))
    Epi_sd.append(np.std(Epi_temp[i]))
    Geo_sd.append(np.std(Geo_temp[i]))
    SnW_sd.append(np.std(SnW_temp[i]))


print(len(Epi_mean))
x = [1, 2, 3]
# x.append(0)
plt.xticks(fontsize=10)
plt.yticks(fontsize=25)
plt.xticks(x, ["Epidemic", "Geographic", "SnW"])

fig_name = "dummy.eps"
plt.xlabel('Protocol', fontsize=25)

plt.ylabel('Band usage', fontsize=25)

