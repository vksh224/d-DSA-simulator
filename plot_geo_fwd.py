import numpy as np
import matplotlib.pyplot as plt

time_epochs = 4
runs = 1

opt = np.zeros(shape=(time_epochs, runs))
pes = np.zeros(shape=(time_epochs, runs))

num_mules = 64
num_channels = 5
num_Pusers = 0
T = 360
startTime = 1
num_messages = 200
days = ["50"]
dataset = "Lexington"
buffer_types = ["PQ"]
protocols = ["Epidemic_Smart_optimistic", "Epidemic_Smart_pessimistic"]
# fwd_strat = ["broadcast", "geo_1", "geo_3", "geo_5"]
fwd_strat = "geo_"
metrics_file = "metrics.txt"

p_id = 4 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

for i in range(len(days)):
    for protocol in protocols:
        for buffer_type in buffer_types:
            t = 0

            for num_fwd in [1, 3, 5, 7]:

                path = "DataMules/" + dataset + "/" + days[i] + "/2/Link_Exists/LE_" + str(startTime) + "_" + str(T) + "/" + protocol + "/" + buffer_type + "/" + fwd_strat + str(num_fwd) + "/mules_" + str(num_mules) + "/channels_" + str(num_channels) + "/P_users_" + str(num_Pusers) + "/msgfile0/puserfile0/"
                with open(path + metrics_file, "r") as f:
                    lines = f.readlines()[1:]

                for line in lines:
                    line_arr = line.strip().split()
                    if "360" in line_arr:
                        if "optimistic" in protocol:
                            opt[t][i] = float(line_arr[p_id])
                        elif "pessimistic" in protocol:
                            pes[t][i] = float(line_arr[p_id])

                t += 1

if p_id == 3:
    for t in range(len(opt)):
        for run in range(runs):
            opt[t][run] = float(opt[t][run]/ 1000)
            pes[t][run] = float(pes[t][run] / 1000)


x = np.array([1, 3, 5, 7])
plt.xticks(fontsize=20)
plt.yticks(fontsize=25)
plt.xticks([1, 3, 5, 7])
title_str = "Messages: " + str(num_messages) + "    Channels: " + str(num_channels) + "    Primary Users: " + str(num_Pusers)
# title_str = "Broadcast to everyone in range"
plt.title(title_str)
# plt.xlim(0,12)
fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Message delivery ratio', fontsize=25)
    plt.xlabel('Number of nodes to forward to', fontsize=25)
    plt.ylim(-0.05,1.1)
    fig_name = "Plots/pdr_fwd_SER.png"

if p_id == 2:
    plt.ylim(-1, 40)
    plt.ylabel('Network delay (min)', fontsize=25)
    plt.xlabel('Number of nodes to forward to', fontsize=25)

    fig_name = "Plots/latency_fwd_SER.png"

if p_id == 3:
    plt.ylabel('Energy expenditure (KJ)', fontsize=25)
    plt.xlabel('Number of nodes to forward to', fontsize=25)
    plt.ylim(-0.01, 22)
    fig_name = "Plots/energy_fwd_SER.png"

if p_id == 4:
    plt.ylabel('Message overhead', fontsize=25)
    plt.xlabel('Number of nodes to forward to', fontsize=25)
    fig_name = "Plots/overhead_fwd_SER.png"

plt.errorbar(x, opt, 0, marker='o', markersize=10, linestyle='-', linewidth=3, color = "red")
plt.errorbar(x, pes, 0, marker='x', markersize=10, linestyle='-', linewidth=3, color = "blue")

if p_id == 1:
    plt.legend(["Optimistic", "Pessimistic"], loc="lower left", fontsize=15, ncol = 1, frameon=False)
elif p_id == 2:
    plt.legend(["Optimistic", "Pessimistic"], loc="lower left", fontsize=15, ncol = 1, frameon=False)
elif p_id ==3:
    plt.legend(["Optimistic", "Pessimistic"], loc="lower left", fontsize=15, ncol = 1, frameon=False)
elif p_id ==4:
    plt.legend(["Optimistic", "Pessimistic"], loc="lower left", fontsize=15, ncol = 1, frameon=False)


plt.tight_layout()
plt.savefig(fig_name)

plt.show()