import numpy as np
import matplotlib.pyplot as plt
from constants import *

time_epochs = 6

msg_files = 3
puser_files = 5

Geo_TV = np.zeros(shape=(time_epochs, msg_files, puser_files))
Geo_LTE = np.zeros(shape=(time_epochs, msg_files, puser_files))
Geo_CBRS = np.zeros(shape=(time_epochs, msg_files, puser_files))
Geo_ISM = np.zeros(shape=(time_epochs, msg_files, puser_files))

num_mules = 92
# num_channels = 5
num_Pusers = 200
msg_mean = 15
T = 360
channels = 6
ttl = 90
max_memory = [25, 50, 100, 200, 300, -1]
startTime = 1
days = "50"
dataset = "Lexington"
buffer_type = ["PQ", "PQ"]
weighted_approach = "weighted_0.5"
smart_settings = [weighted_approach]
protocols = ["geo"]
# protocols = ["Epidemic_Smart_optimistic"]
# fwd_strat = ["geo_3"]
num_replicas = 1
num_replicas_snw = 25
metrics_file = "metrics.txt"
sim_round = 7

p_id = 1 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

for i in range(msg_files):
    for j in range(puser_files):
        for mem_size in max_memory:
            for setting in smart_settings:
                for protocol in protocols:
                    t = max_memory.index(mem_size)

                    path_exists = False

                    if setting in [weighted_approach]:  # ALL Bands
                        if protocol in ["geo"]:
                            protocol = protocol + "_" + str(num_replicas)

                        if protocol in ["SnW"]:
                            protocol = protocol + "_" + str(num_replicas_snw)

                        path_exists = True

                    if path_exists:
                        path = "DataMules/" + dataset + "/" + days + "/" + str(sim_round) + "/Link_Exists/LE_" + str(
                            startTime) + \
                               "_" + str(T) + "/Epidemic_Smart_" + setting + "/" + buffer_type[
                                   0] + "/" + protocol + "/mules_" + \
                               str(num_mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + \
                               "/msgfile_" + str(i) + "_" + str(msg_mean) + "/puserfile_" + str(j) + "/TTL_" + str(
                            ttl) + "/BuffSize_" + str(mem_size) + "/"

                        with open(path + metrics_file, "r") as f:
                            lines = f.readlines()[1:]

                        for line in lines:
                            line_arr = line.strip().split()
                            if int(line_arr[0]) == 360:

                                # if "geo" in protocol:
                                Geo_LTE[t, i, j] = float(line_arr[6])
                                Geo_TV[t, i, j] = float(line_arr[8])
                                Geo_CBRS[t, i, j] = float(line_arr[7])
                                Geo_ISM[t, i, j] = float(line_arr[9])

Geo_TV_mean = []
Geo_TV_sd = []
Geo_LTE_mean = []
Geo_LTE_sd = []
Geo_CBRS_mean = []
Geo_CBRS_sd = []
Geo_ISM_mean = []
Geo_ISM_sd = []

Geo_TV_temp = []
Geo_LTE_temp = []
Geo_CBRS_temp = []
Geo_ISM_temp = []

for t in range(len(Geo_TV)):

    t_arr_tv_geo = []
    t_arr_lte_geo = []
    t_arr_cbrs_geo = []
    t_arr_ism_geo = []
    for i in range(len(Geo_TV[t])):
        for j in range(len(Geo_TV[t][i])):

            t_arr_tv_geo.append(Geo_TV[t, i, j])
            t_arr_lte_geo.append(Geo_LTE[t, i, j])
            t_arr_cbrs_geo.append(Geo_CBRS[t, i, j])
            t_arr_ism_geo.append(Geo_ISM[t, i, j])

    Geo_TV_temp.append(t_arr_tv_geo)
    Geo_LTE_temp.append(t_arr_lte_geo)
    Geo_CBRS_temp.append(t_arr_cbrs_geo)
    Geo_ISM_temp.append(t_arr_ism_geo)

for i in range(len(Geo_TV_temp)):

    Geo_TV_mean.append(np.mean(Geo_TV_temp[i]))
    Geo_TV_sd.append(np.std(Geo_TV_temp[i]))
    Geo_LTE_mean.append(np.mean(Geo_LTE_temp[i]))
    Geo_LTE_sd.append(np.std(Geo_LTE_temp[i]))
    Geo_CBRS_mean.append(np.mean(Geo_CBRS_temp[i]))
    Geo_CBRS_sd.append(np.std(Geo_CBRS_temp[i]))
    Geo_ISM_mean.append(np.mean(Geo_ISM_temp[i]))
    Geo_ISM_sd.append(np.std(Geo_ISM_temp[i]))

print(len(Geo_TV_mean))

x = [25, 50, 100, 200, 300, 500]
plt.figure(figsize=(8,4.5))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(x, ["25", "50", "100", "200", "300", "Unlimited"])

plt.xlabel('Memory buffer size', fontsize=15)
plt.ylabel('Perc. of band usage', fontsize=15)

if "geo" in protocols:
    fig_name = "Plots/msgmean_bandusage_geo.eps"
elif "broadcast" in protocols:
    fig_name = "Plots/msgmean_bandusage_SER.eps"
else:
    fig_name = "Plots/msgmean_bandusage_SnW.eps"

plt.errorbar(x, Geo_TV_mean, 0, marker='*', markersize=5, linestyle='-', linewidth=2)
plt.errorbar(x, Geo_LTE_mean, 0, marker='*', markersize=5, linestyle=':', linewidth=2)
plt.errorbar(x, Geo_CBRS_mean, 0, marker='*', markersize=5, linestyle='-', linewidth=2)
plt.errorbar(x, Geo_ISM_mean, 0, marker='*', markersize=5, linestyle='--', linewidth=2)

routing_name_list = ["TV", "LTE", "CBRS", "ISM"]
plt.legend(routing_name_list, loc="upper left",  bbox_to_anchor=(0.01, 0.65), fontsize=12, ncol = 4, frameon=False)

plt.tight_layout()
plt.savefig(fig_name)

plt.show()