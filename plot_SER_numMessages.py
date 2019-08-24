import numpy as np
import matplotlib.pyplot as plt

time_epochs = 5
runs = 1

geo1 = np.zeros(shape=(time_epochs, runs))
geo5 = np.zeros(shape=(time_epochs, runs))
geo10 = np.zeros(shape=(time_epochs, runs))

geoP1 = np.zeros(shape=(time_epochs, runs))
geoP5 = np.zeros(shape=(time_epochs, runs))
geoP10 = np.zeros(shape=(time_epochs, runs))


num_mules = 30
num_channels = 6
num_Pusers = 200
T = 180
startTime = 1
num_messages = [50, 100, 200, 300, 400]
days = ["30"]
folder_nums = [x for x in range(1,11, 1)]
buffer_types = ["PQ"]
protocols = ["Epidemic_Smart_optimistic", "Epidemic_Smart_pessimistic"]
metrics_file = "metrics.txt"

p_id = 1 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

for i in range(len(days)):
    for protocol in protocols:
        for buffer_type in buffer_types:
            t = 0
            for msg in num_messages:
                for num_fwd in ["1", "5", "10"]:

                    path = "DataMules/Lexington/" + days[i] + "/1/Link_Exists/LE_" + str(startTime) + "_" + str(T) + "/" + protocol + "/" + buffer_type + "/geo_" + num_fwd + "/mules_" + str(num_mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + "/" + str(msg) + "/"
                    with open(path + metrics_file, "r") as f:
                        lines = f.readlines()[1:]

                    for line in lines:
                        line_arr = line.strip().split()

                        if "180" in line_arr:
                            if "optimistic" in protocol:
                                if num_fwd == "1":
                                    geo1[t][i] = float(line_arr[p_id])
                                elif num_fwd == "5":
                                    geo5[t][i] = float(line_arr[p_id])
                                elif num_fwd == "10":
                                    geo10[t][i] = float(line_arr[p_id])

                            elif "pessimistic" in protocol:
                                if num_fwd == "1":
                                    geoP1[t][i] = float(line_arr[p_id])
                                elif num_fwd == "5":
                                    geoP5[t][i] = float(line_arr[p_id])
                                elif num_fwd == "10":
                                    geoP10[t][i] = float(line_arr[p_id])
                t += 1

if p_id == 3:
    for t in range(len(geo1)):
        for run in range(runs):
            geo1[t][run] = float(geo1[t][run]) / 1000
            geo5[t][run] = float(geo5[t][run]) / 1000
            geo10[t][run] = float(geo10[t][run]) / 1000
            geoP1[t][run] = float(geoP1[t][run]) / 1000
            geoP5[t][run] = float(geoP5[t][run]) / 1000
            geoP10[t][run] = float(geoP10[t][run]) / 1000



x = np.array([50, 100, 200, 300, 400])
plt.xticks(fontsize=20)
plt.yticks(fontsize=25)
plt.xticks(np.array([50, 100, 200, 300, 400]))
title_str = "Time: " + str(T) + "    Channels: " + str(num_channels) + "    Primary Users: " + str(num_Pusers)
plt.title(title_str)
# plt.xlim(0,12)
fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Message delivery ratio', fontsize=25)
    plt.xlabel('Number of messages', fontsize=25)
    plt.ylim(-0.05,1.1)
    fig_name = "Plots/pdr_msg_SER.png"

if p_id == 2:
    plt.ylim(-1, 45)
    plt.ylabel('Network delay (min)', fontsize=25)
    plt.xlabel('Number of messages', fontsize=25)

    fig_name = "Plots/latency_msg_SER.png"

if p_id == 3:
    plt.ylabel('Energy expenditure (KJ)', fontsize=25)
    plt.xlabel('Number of messages', fontsize=25)
    plt.ylim(-1, 17)
    fig_name = "Plots/energy_msg_SER.png"

if p_id == 4:
    plt.ylabel('Message overhead', fontsize=25)
    plt.xlabel('Number of messages', fontsize=25)
    plt.ylim(-1, 20)
    fig_name = "Plots/overhead_msg_SER.png"


plt.errorbar(x, geo1, 0, marker='o', markersize=10, linestyle='-', linewidth=3, color = "red")
plt.errorbar(x, geo5, 0, marker='o', markersize=10, linestyle='-', linewidth=3, color = "blue")
plt.errorbar(x, geo10, 0, marker='o', markersize=10, linestyle='-', linewidth=3, color = "green")
plt.errorbar(x, geoP1, 0, marker='x', markersize=10, linestyle='--', linewidth=3, color = "red")
plt.errorbar(x, geoP5, 0, marker='x', markersize=10, linestyle='--', linewidth=3, color = "blue")
plt.errorbar(x, geoP10, 0, marker='x', markersize=10, linestyle='--', linewidth=3, color = "green")




if p_id == 1:
    plt.legend(["Opt-1", "Opt-5", "Opt-10", "Pes-1", "Pes-5", "Pes-10"], loc="lower left", fontsize=15, ncol = 1, frameon=False)
elif p_id == 2:
    plt.legend(["Opt-1", "Opt-5", "Opt-10", "Pes-1", "Pes-5", "Pes-10"], loc="lower right", fontsize=15, ncol = 1, frameon=False)
elif p_id ==3:
    plt.legend(["Opt-1", "Opt-5", "Opt-10", "Pes-1", "Pes-5", "Pes-10"], loc="lower right", fontsize=15, ncol = 1, frameon=False)
elif p_id ==4:
    plt.legend(["Opt-1", "Opt-5", "Opt-10", "Pes-1", "Pes-5", "Pes-10"], loc="lower left", fontsize=15, ncol = 1, frameon=False)

plt.tight_layout()
plt.savefig(fig_name)

plt.show()