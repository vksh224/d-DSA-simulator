import numpy as np
import matplotlib.pyplot as plt

time_epochs = 3
runs = 1

geo1 = np.zeros(shape=(time_epochs, runs))
geo2 = np.zeros(shape=(time_epochs, runs))
geo3 = np.zeros(shape=(time_epochs, runs))
geo4 = np.zeros(shape=(time_epochs, runs))
geo5 = np.zeros(shape=(time_epochs, runs))
geo6 = np.zeros(shape=(time_epochs, runs))
geo7 = np.zeros(shape=(time_epochs, runs))
geo8 = np.zeros(shape=(time_epochs, runs))
geo9 = np.zeros(shape=(time_epochs, runs))
geo10 = np.zeros(shape=(time_epochs, runs))
broadcast = np.zeros(shape=(time_epochs, runs))

geoP1 = np.zeros(shape=(time_epochs, runs))
geoP2 = np.zeros(shape=(time_epochs, runs))
geoP3 = np.zeros(shape=(time_epochs, runs))
geoP4 = np.zeros(shape=(time_epochs, runs))
geoP5 = np.zeros(shape=(time_epochs, runs))
geoP6 = np.zeros(shape=(time_epochs, runs))
geoP7 = np.zeros(shape=(time_epochs, runs))
geoP8 = np.zeros(shape=(time_epochs, runs))
geoP9 = np.zeros(shape=(time_epochs, runs))
geoP10 = np.zeros(shape=(time_epochs, runs))
broadcastP = np.zeros(shape=(time_epochs, runs))


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
num_replicas = [1, 3]
sim_round = 5


# num_mules = 92
# num_channels = 6
# num_Pusers = 200
# T = 180
# startTime = 1
# num_messages = 200
# days = ["30"]
# dataset = "Lexington"
# buffer_types = ["PQ"]
# protocols = ["Epidemic_Smart_optimistic", "Epidemic_Smart_pessimistic"]
# # fwd_strat = ["broadcast", "geo_1", "geo_3", "geo_5"]
# fwd_strat = "geo_"
# metrics_file = "metrics.txt"

p_id = 4 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

for i in range(msg_files):
    for j in range(puser_files):
        # for protocol in protocols:
        for buffer_type in buffer_types:
            for num_fwd in num_replicas:
                t = 0
                path = "./DataMules/" + dataset + "/" + days + "/" + str(sim_round) + "/Link_Exists/LE_" + str(
                    startTime) + \
                       "_" + str(T) + "/Epidemic_Smart_" + protocol + "/" + buffer_type[0] + "/geo_" + str(
                    num_replicas) + "/mules_" + \
                       str(num_mules) + "/channels_" + str(num_channels) + "/P_users_" + str(
                    num_Pusers) + "/msgfile_" + str(
                    i) + "_" + str(msg_mean) + "/puserfile_" + str(j) + "/TTL_" + str(ttl) + "/BuffSize_" + str(
                    max_mem) + "/"

                #path = "DataMules/" + dataset + "/" + days[i] + "/1/Link_Exists/LE_" + str(startTime) + "_" + str(T) + "/" + protocol + "/" + buffer_type + "/" + fwd_strat + str(num_fwd) + "/mules_" + str(num_mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + "/" + str(num_messages) + "/"
                with open(path + metrics_file, "r") as f:
                    lines = f.readlines()[1:]

                for line in lines:
                    line_arr = line.strip().split()
                    if int(line_arr[0]) % 5 == 0:
                        if "optimistic" in protocol:
                            if num_fwd == 1:
                                geo1[t][i] = float(line_arr[p_id])
                            elif num_fwd == 2:
                                geo2[t][i] = float(line_arr[p_id])
                            elif num_fwd == 3:
                                geo3[t][i] = float(line_arr[p_id])
                            elif num_fwd == 4:
                                geo4[t][i] = float(line_arr[p_id])
                            elif num_fwd == 5:
                                geo5[t][i] = float(line_arr[p_id])
                            elif num_fwd == 6:
                                geo6[t][i] = float(line_arr[p_id])
                            elif num_fwd == 7:
                                geo7[t][i] = float(line_arr[p_id])
                            elif num_fwd == 8:
                                geo8[t][i] = float(line_arr[p_id])
                            elif num_fwd == 9:
                                geo9[t][i] = float(line_arr[p_id])
                            elif num_fwd == 10:
                                geo10[t][i] = float(line_arr[p_id])
                        elif "pessimistic" in protocol:
                            if num_fwd == 1:
                                geoP1[t][i] = float(line_arr[p_id])
                            elif num_fwd == 2:
                                geoP2[t][i] = float(line_arr[p_id])
                            elif num_fwd == 3:
                                geoP3[t][i] = float(line_arr[p_id])
                            elif num_fwd == 4:
                                geoP4[t][i] = float(line_arr[p_id])
                            elif num_fwd == 5:
                                geoP5[t][i] = float(line_arr[p_id])
                            elif num_fwd == 6:
                                geoP6[t][i] = float(line_arr[p_id])
                            elif num_fwd == 7:
                                geoP7[t][i] = float(line_arr[p_id])
                            elif num_fwd == 8:
                                geoP8[t][i] = float(line_arr[p_id])
                            elif num_fwd == 9:
                                geoP9[t][i] = float(line_arr[p_id])
                            elif num_fwd == 10:
                                geoP10[t][i] = float(line_arr[p_id])

                        t += 1


if p_id == 3:
    for t in range(len(geo1)):
        for run in range(runs):
            geo1[t][run] = float(geo1[t][run] / 1000)
            geo2[t][run] = float(geo2[t][run] / 1000)
            geo3[t][run] = float(geo3[t][run] / 1000)
            geo4[t][run] = float(geo4[t][run] / 1000)
            geo5[t][run] = float(geo5[t][run] / 1000)
            geo6[t][run] = float(geo6[t][run] / 1000)
            geo7[t][run] = float(geo7[t][run] / 1000)
            geo8[t][run] = float(geo8[t][run] / 1000)
            geo9[t][run] = float(geo9[t][run] / 1000)
            geo10[t][run] = float(geo10[t][run] / 1000)

            geoP1[t][run] = float(geoP1[t][run] / 1000)
            geoP2[t][run] = float(geoP2[t][run] / 1000)
            geoP3[t][run] = float(geoP3[t][run] / 1000)
            geoP4[t][run] = float(geoP4[t][run] / 1000)
            geoP5[t][run] = float(geoP5[t][run] / 1000)
            geoP6[t][run] = float(geoP6[t][run] / 1000)
            geoP7[t][run] = float(geoP7[t][run] / 1000)
            geoP8[t][run] = float(geoP8[t][run] / 1000)
            geoP9[t][run] = float(geoP9[t][run] / 1000)
            geoP10[t][run] = float(geoP10[t][run] / 1000)


x = np.array([x for x in range(0, T +1, 30)])
plt.xticks(fontsize=20)
plt.yticks(fontsize=25)
plt.xticks(np.arange(0, 181, 30))
title_str = "Messages: " + str(num_messages) + "    Channels: " + str(num_channels) + "    Primary Users: " + str(num_Pusers)
# title_str = "Broadcast to everyone in range"
plt.title(title_str)
# plt.xlim(0,12)
fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Message delivery ratio', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)
    # plt.ylim(-0.05,1.1)
    fig_name = "Plots/pdr_Time_Geo.png"

if p_id == 2:
    # plt.ylim(-1, 40)
    plt.ylabel('Network delay (min)', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)

    fig_name = "Plots/latency_time_Geo.png"

if p_id == 3:
    plt.ylabel('Energy expenditure (KJ)', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)
    # plt.ylim(-0.01, 22)
    fig_name = "Plots/energy_time_Geo.png"

if p_id == 4:
    plt.ylabel('Message overhead', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)
    # plt.ylim(-1, 20)
    fig_name = "Plots/overhead_Time_Geo.png"


plt.errorbar(x, geo1, 0, marker='o', markersize=10, linestyle='-', linewidth=3, color = "red")
# plt.errorbar(x, geo2, 0, marker='o', markersize=10, linestyle='-', linewidth=3)
plt.errorbar(x, geo3, 0, marker='o', markersize=10, linestyle='-', linewidth=3, color = "blue")
# plt.errorbar(x, geo4, 0, marker='o', markersize=10, linestyle='-', linewidth=3)
plt.errorbar(x, geo5, 0, marker='o', markersize=10, linestyle='-', linewidth=3, color = "blue")
# plt.errorbar(x, geo6, 0, marker='o', markersize=10, linestyle='-', linewidth=3)
# plt.errorbar(x, geo7, 0, marker='o', markersize=10, linestyle='-', linewidth=3, color = "black")
# plt.errorbar(x, geo8, 0, marker='o', markersize=10, linestyle='-', linewidth=3)
# plt.errorbar(x, geo9, 0, marker='o', markersize=10, linestyle='-', linewidth=3)
# plt.errorbar(x, geo10, 0, marker='o', markersize=10, linestyle='-', linewidth=3, color = "green")

plt.errorbar(x, geoP1, 0, marker='x', markersize=10, linestyle='--', linewidth=3, color = "red")
# plt.errorbar(x, geoP2, 0, marker='x', markersize=10, linestyle='--', linewidth=3)
plt.errorbar(x, geoP3, 0, marker='x', markersize=10, linestyle='--', linewidth=3, color = "blue")
# plt.errorbar(x, geoP4, 0, marker='x', markersize=10, linestyle='--', linewidth=3)
plt.errorbar(x, geoP5, 0, marker='x', markersize=10, linestyle='--', linewidth=3, color = "blue")
# plt.errorbar(x, geoP6, 0, marker='x', markersize=10, linestyle='--', linewidth=3)
# plt.errorbar(x, geoP7, 0, marker='x', markersize=10, linestyle='--', linewidth=3, color = "black")
# plt.errorbar(x, geoP8, 0, marker='x', markersize=10, linestyle='--', linewidth=3)
# plt.errorbar(x, geoP9, 0, marker='x', markersize=10, linestyle='--', linewidth=3)
# plt.errorbar(x, geoP10, 0, marker='x', markersize=10, linestyle='--', linewidth=3, color = "green")


if p_id == 1:
    plt.legend(["Opt-1", "Opt-5", "Opt-10",  "Pes-1", "Pes-5", "Pes-10"], loc="upper left", fontsize=15, ncol = 1, frameon=False)
elif p_id == 2:
    plt.legend(["Opt-1", "Opt-5", "Opt-10",  "Pes-1", "Pes-5", "Pes-10"], loc="upper left", fontsize=15, ncol = 1, frameon=False)
elif p_id ==3:
    plt.legend(["Opt-1", "Opt-5", "Opt-10",  "Pes-1", "Pes-5", "Pes-10"], loc="upper left", fontsize=15, ncol = 1, frameon=False)
elif p_id ==4:
    plt.legend(["Opt-1", "Opt-5", "Opt-10",  "Pes-1", "Pes-5", "Pes-10"], loc="upper left", fontsize=15, ncol = 1, frameon=False)


plt.tight_layout()
plt.savefig(fig_name)

plt.show()

# plt.legend(["Opt-1", "Opt-3", "Opt-5", "Opt-7", "Pes-1", "Pes-3", "Pes-5", "Pes-7"], loc="upper left", fontsize=15,
#            ncol=1, frameon=False)

