import numpy as np
import matplotlib.pyplot as plt
from constants import *

time_epochs = 13

msg_files = 5
puser_files = 1

# arrays for broadcast
opt_geo1 = np.zeros(shape=(time_epochs, msg_files, puser_files))
pes_geo1 = np.zeros(shape=(time_epochs, msg_files, puser_files))
wei_geo1 = np.zeros(shape=(time_epochs, msg_files, puser_files))
opt_geo2 = np.zeros(shape=(time_epochs, msg_files, puser_files))
pes_geo2 = np.zeros(shape=(time_epochs, msg_files, puser_files))
wei_geo2 = np.zeros(shape=(time_epochs, msg_files, puser_files))
opt_geo3 = np.zeros(shape=(time_epochs, msg_files, puser_files))
pes_geo3 = np.zeros(shape=(time_epochs, msg_files, puser_files))
wei_geo3 = np.zeros(shape=(time_epochs, msg_files, puser_files))
opt_epi = np.zeros(shape=(time_epochs, msg_files, puser_files))

num_mules = 92
num_channels = 6
num_Pusers = 200
msg_mean = 15
ttl = 180
max_mem = 100
T = 360
startTime = 1
days = "50"
dataset = "Lexington"
buffer_type = ["PQ", "FIFO"]
protocols = ["optimistic", "pessimistic", "weighted"]
#fwd_strat = 1
metrics_file = "metrics.txt"
num_replicas = [1, 3, 5]
sim_round = 5

p_id = 3 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

for i in range(msg_files):
    for j in range(puser_files):
        for protocol in protocols:
            t = 0
            path = "./DataMules/" + dataset + "/" + days + "/" + str(sim_round) + "/Link_Exists/LE_" + str(startTime) + \
                   "_" + str(T) + "/Epidemic_Smart_" + protocol + "/" + buffer_type[0] + "/geo_" + str(
                num_replicas) + "/mules_" + \
                   str(num_mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + "/msgfile_" + str(
                i) + "_" + str(msg_mean) + "/puserfile_" + str(j) + "/TTL_" + str(ttl) + "/BuffSize_" + str(max_mem) + "/"

            with open(path + metrics_file, "r") as f:
                lines = f.readlines()[1:]

            for line in lines:
                line_arr = line.strip().split()
                if int(line_arr[0]) % 5 == 0:
                    if "optimistic" in protocol:
                        opt_geo1[t, i, j] = float(line_arr[p_id])
                    elif "pessimistic" in protocol:
                        pes_geo1[t, i, j] = float(line_arr[p_id])
                    elif "weighted" in protocol:
                        wei_geo1[t, i, j] = float(line_arr[p_id])

                    t += 1

for i in range(msg_files):
    for j in range(puser_files):
        for protocol in ["optimistic", "pessimistic", "weighted", "TV", "LTE", "CBRS", "ISM"]:
            t = 0

            if protocol in ["optimistic", "pessimistic", "weighted"]:
                path = "DataMules/" + dataset + "/" + days + "/" + str(sim_round) + "/Link_Exists/LE_" + str(startTime) + \
                       "_" + str(T) + "/Epidemic_Smart_" + protocol + "/" + buffer_type[0] + "/broadcast/mules_" + \
                       str(num_mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + \
                       "/msgfile_" + str(i) + "_" + str(msg_mean) + "/puserfile_" + str(j) + "/TTL_" + str(ttl) + "/BuffSize_" + str(max_mem) + "/"

            else:
                path = "DataMules/" + dataset + "/" + days + "/" + str(sim_round) + "/Link_Exists/LE_" + str(
                    startTime) + \
                       "_" + str(T) + "/Epidemic_Smart_" + protocol + "/" + buffer_type[1] + "/broadcast/mules_" + \
                       str(num_mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + \
                       "/msgfile_" + str(i) + "_" + str(msg_mean) + "/puserfile_" + str(j) + "/TTL_" + str(
                    ttl) + "/BuffSize_" + str(max_mem) + "/"

            with open(path + metrics_file, "r") as f:
                lines = f.readlines()[1:]

            for line in lines:
                line_arr = line.strip().split()
                if int(line_arr[0]) % 5 == 0:
                    if "optimistic" in protocol:
                        opt_geo2[t, i, j] = float(line_arr[p_id])
                    elif "pessimistic" in protocol:
                         pes_geo2[t, i, j] = float(line_arr[p_id])
                    elif "weighted" in protocol:
                         wei_geo2[t, i, j] = float(line_arr[p_id])
                    elif "TV" in protocol:
                        opt_geo3[t, i, j] = float(line_arr[p_id])
                    elif "LTE" in protocol:
                        pes_geo3[t, i, j] = float(line_arr[p_id])
                    elif "CBRS" in protocol:
                        wei_geo3[t, i, j] = float(line_arr[p_id])
                    elif "ISM" in protocol:
                        opt_epi[t, i, j] = float(line_arr[p_id])

                    t += 1

optGeo_mean = []
optGeo_sd = []
pesGeo_mean = []
pesGeo_sd = []
weiGeo_mean = []
weiGeo_sd = []
optEpi_mean = []
optEpi_sd = []
pesEpi_mean = []
pesEpi_sd = []
weiEpi_mean = []
weiEpi_sd = []

TV_mean = []
TV_sd = []
LTE_mean = []
LTE_sd = []
CBRS_mean = []
CBRS_sd = []
ISM_mean = []
ISM_sd = []

optGeo_temp = []
pesGeo_temp = []
weiGeo_temp = []
optEpi_temp = []
pesEpi_temp = []
weiEpi_temp = []

TV_temp = []
LTE_temp = []
CBRS_temp = []
ISM_temp = []

for t in range(len(opt_geo1)):

    t_arr_optGeo = []
    t_arr_pesGeo = []
    t_arr_weiGeo = []
    t_arr_optEpi = []
    t_arr_pesEpi = []
    t_arr_weiEpi = []

    t_arr_tv = []
    t_arr_lte = []
    t_arr_cbrs = []
    t_arr_ism = []
    for i in range(len(opt_geo1[t])):
        for j in range(len(opt_geo1[t][i])):
            t_arr_optGeo.append(opt_geo1[t, i, j])
            t_arr_pesGeo.append(pes_geo1[t, i, j])
            t_arr_weiGeo.append(wei_geo1[t, i, j])
            t_arr_optEpi.append(opt_geo2[t, i, j])
            t_arr_pesEpi.append(pes_geo2[t, i, j])
            t_arr_weiEpi.append(wei_geo2[t, i, j])
            t_arr_tv.append(opt_geo3[t, i, j])
            t_arr_lte.append(pes_geo3[t, i, j])
            t_arr_cbrs.append(wei_geo3[t, i, j])
            t_arr_ism.append(opt_epi[t, i, j])


    optGeo_temp.append(t_arr_optGeo)
    pesGeo_temp.append(t_arr_pesGeo)
    weiGeo_temp.append(t_arr_weiGeo)
    optEpi_temp.append(t_arr_optEpi)
    pesEpi_temp.append(t_arr_pesEpi)
    weiEpi_temp.append(t_arr_weiEpi)
    TV_temp.append(t_arr_tv)
    LTE_temp.append(t_arr_lte)
    CBRS_temp.append(t_arr_cbrs)
    ISM_temp.append(t_arr_ism)

for i in range(len(optGeo_temp)):
    optGeo_mean.append(np.mean(optGeo_temp[i]))
    pesGeo_mean.append(np.mean(pesGeo_temp[i]))
    weiGeo_mean.append(np.mean(weiGeo_temp[i]))
    optGeo_sd.append(np.std(optGeo_temp[i]))
    pesGeo_sd.append(np.std(pesGeo_temp[i]))
    weiGeo_sd.append(np.std(weiGeo_temp[i]))
    optEpi_mean.append(np.mean(optEpi_temp[i]))
    pesEpi_mean.append(np.mean(pesEpi_temp[i]))
    weiEpi_mean.append(np.mean(weiEpi_temp[i]))
    optEpi_sd.append(np.std(optEpi_temp[i]))
    pesEpi_sd.append(np.std(pesEpi_temp[i]))
    weiEpi_sd.append(np.std(weiEpi_temp[i]))
    TV_mean.append(np.mean(TV_temp[i]))
    TV_sd.append(np.std(TV_temp[i]))
    LTE_mean.append(np.mean(LTE_temp[i]))
    LTE_sd.append(np.std(LTE_temp[i]))
    CBRS_mean.append(np.mean(CBRS_temp[i]))
    CBRS_sd.append(np.std(CBRS_temp[i]))
    ISM_mean.append(np.mean(ISM_temp[i]))
    ISM_sd.append(np.std(ISM_temp[i]))


x = np.array([x for x in range(0, T +1, metric_interval)])
plt.xticks(fontsize=10)
plt.yticks(fontsize=25)
plt.xticks(np.arange(0, T+1, 30))
title_str = "Channels: " + str(num_channels) + "    Primary Users: " + str(num_Pusers)
# title_str = "Broadcast to everyone in range"
# plt.title(title_str)
plt.xlim(0,360)
fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Message delivery ratio', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)
    plt.ylim(-0.1,1)
    fig_name = "Plots/pdr_Time_SER.png"

if p_id == 2:
    # plt.ylim(-1, 13)
    plt.ylabel('Network delay (min)', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)

    fig_name = "Plots/latency_time_SER.png"

if p_id == 3:
    plt.ylabel('Energy per packet (kJ)', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)
    fig_name = "Plots/energy_time_SER.png"

if p_id == 4:
    plt.ylabel('Message overhead', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)
    # plt.ylim(-1, 20)
    fig_name = "Plots/overhead_Time_SER.png"

if p_id == 3:
    plt.errorbar(x, [y/1000 for y in optGeo_mean], 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, [y/1000 for y in pesGeo_mean], 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, [y/1000 for y in weiGeo_mean], 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, [y/1000 for y in optEpi_mean], 0, marker='x', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, [y/1000 for y in pesEpi_mean], 0, marker='x', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, [y/1000 for y in weiEpi_mean], 0, marker='x', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, [y/1000 for y in TV_mean], 0, marker='o', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, [y/1000 for y in LTE_mean], 0, marker='o', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, [y/1000 for y in CBRS_mean], 0, marker='o', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, [y/1000 for y in ISM_mean], 0, marker='o', markersize=5, linestyle='--', linewidth=1)

else: 
    plt.errorbar(x, optGeo_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, pesGeo_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, weiGeo_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, optEpi_mean, 0, marker='x', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, pesEpi_mean, 0, marker='x', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, weiEpi_mean, 0, marker='x', markersize=5, linestyle='-', linewidth=1)
    plt.errorbar(x, TV_mean, 0, marker='o', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, LTE_mean, 0, marker='o', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, CBRS_mean, 0, marker='o', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, ISM_mean, 0, marker='o', markersize=5, linestyle='--', linewidth=1)


if p_id == 1:
    plt.legend(["Geo-opt", "Geo-pes", "Geo-wei", "SER-opt", "SER-pes", "SER-wei",  "TV", "LTE", "CBRS", "ISM"], loc="upper left", fontsize=10, ncol = 3, frameon=False)
elif p_id == 2:
    plt.legend(["Geo-opt", "Geo-pes", "Geo-wei", "SER-opt", "SER-pes", "SER-wei",  "TV", "LTE", "CBRS", "ISM"], loc="upper left", fontsize=10, ncol = 1, frameon=False)
elif p_id ==3:
    plt.legend(["Geo-opt", "Geo-pes", "Geo-wei", "SER-opt", "SER-pes", "SER-wei",  "TV", "LTE", "CBRS", "ISM"], loc="upper left", fontsize=10, ncol = 1, frameon=False)
elif p_id ==4:
    plt.legend(["Geo-opt", "Geo-pes", "Geo-wei", "SER-opt", "SER-pes", "SER-wei",  "TV", "LTE", "CBRS", "ISM"], loc="upper left", fontsize=10, ncol = 1, frameon=False)


plt.tight_layout()
plt.savefig(fig_name)

plt.show()