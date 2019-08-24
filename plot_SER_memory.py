import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from constants import *
import sys

time_epochs = 6

msg_files = 3
puser_files = 5

# arrays for broadcast
# arrays for broadcast
Epidemic_opt_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_pes_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_wei_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))
bro_opt_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))
bro_pes_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))
bro_wei_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))
snw_wei_PQ = np.zeros(shape=(time_epochs, msg_files, puser_files))

Epidemic_TV = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_LTE = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_CBRS = np.zeros(shape=(time_epochs, msg_files, puser_files))
Epidemic_ISM = np.zeros(shape=(time_epochs, msg_files, puser_files))

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
smart_settings = [weighted_approach, "TV", "LTE", "CBRS", "ISM"]
protocols = ["broadcast", "geo", "SnW"]
# protocols = ["Epidemic_Smart_optimistic"]
# fwd_strat = ["geo_3"]
num_replicas = 1
num_replicas_snw = 25
metrics_file = "metrics.txt"
sim_round = 7

p_id = int(str(sys.argv[1]))
#12 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

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

                    else:
                        if protocol in ["geo"]:
                            protocol = protocol + "_" + str(num_replicas)
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
                                # if "optimistic" in setting and "geo" in protocol:
                                #     Epidemic_opt_PQ[t, i, j] = float(line_arr[p_id])
                                # elif "pessimistic" in setting and "geo" in protocol:
                                #      Epidemic_pes_PQ[t, i, j] = float(line_arr[p_id])
                                if "weighted" in setting and "geo" in protocol:
                                    Epidemic_wei_PQ[t, i, j] = float(line_arr[p_id])
                                elif "weighted" in setting and "SnW" in protocol:
                                    snw_wei_PQ[t, i, j] = float(line_arr[p_id])
                                elif "weighted" in setting and "broadcast" in protocol:
                                    bro_wei_PQ[t, i, j] = float(line_arr[p_id])
                                elif "TV" in setting and "geo" in protocol:
                                    Epidemic_TV[t, i, j] = float(line_arr[p_id])
                                elif "LTE" in setting and "geo" in protocol:
                                    Epidemic_LTE[t, i, j] = float(line_arr[p_id])
                                elif "CBRS" in setting and "geo" in protocol:
                                    Epidemic_CBRS[t, i, j] = float(line_arr[p_id])
                                elif "ISM" in setting and "geo" in protocol:
                                    Epidemic_ISM[t, i, j] = float(line_arr[p_id])

optB_mean = []
optB_sd = []
pesB_mean = []
pesB_sd = []
weiB_mean = []
weiB_sd = []
optBro_mean = []
optBro_sd = []
pesBro_mean = []
pesBro_sd = []
weiBro_mean = []
weiBro_sd = []

weiSnW_mean = []
weiSnW_sd = []

TV_mean = []
TV_sd = []
LTE_mean = []
LTE_sd = []
CBRS_mean = []
CBRS_sd = []
ISM_mean = []
ISM_sd = []

optB_temp = []
pesB_temp = []
weiB_temp = []
optBro_temp = []
pesBro_temp = []
weiBro_temp = []
weiSnW_temp = []

TV_temp = []
LTE_temp = []
CBRS_temp = []
ISM_temp = []

for t in range(len(Epidemic_opt_PQ)):

    t_arr_optB = []
    t_arr_pesB = []
    t_arr_weiB = []
    t_arr_optBro = []
    t_arr_pesBro = []
    t_arr_weiBro = []

    t_arr_weiSnW = []

    t_arr_tv = []
    t_arr_lte = []
    t_arr_cbrs = []
    t_arr_ism = []
    for i in range(len(Epidemic_opt_PQ[t])):
        for j in range(len(Epidemic_opt_PQ[t][i])):
            t_arr_optB.append(Epidemic_opt_PQ[t, i, j])
            t_arr_pesB.append(Epidemic_pes_PQ[t, i, j])
            t_arr_weiB.append(Epidemic_wei_PQ[t, i, j])
            t_arr_optBro.append(bro_opt_PQ[t, i, j])
            t_arr_pesBro.append(bro_pes_PQ[t, i, j])
            t_arr_weiBro.append(bro_wei_PQ[t, i, j])
            t_arr_weiSnW.append(snw_wei_PQ[t, i, j])

            t_arr_tv.append(Epidemic_TV[t, i, j])
            t_arr_lte.append(Epidemic_LTE[t, i, j])
            t_arr_cbrs.append(Epidemic_CBRS[t, i, j])
            t_arr_ism.append(Epidemic_ISM[t, i, j])

    optB_temp.append(t_arr_optB)
    pesB_temp.append(t_arr_pesB)
    weiB_temp.append(t_arr_weiB)
    optBro_temp.append(t_arr_optBro)
    pesBro_temp.append(t_arr_pesBro)
    weiBro_temp.append(t_arr_weiBro)
    weiSnW_temp.append(t_arr_weiSnW)

    TV_temp.append(t_arr_tv)
    LTE_temp.append(t_arr_lte)
    CBRS_temp.append(t_arr_cbrs)
    ISM_temp.append(t_arr_ism)

for i in range(len(optB_temp)):
    optB_mean.append(np.mean(optB_temp[i]))
    pesB_mean.append(np.mean(pesB_temp[i]))
    weiB_mean.append(np.mean(weiB_temp[i]))
    optB_sd.append(np.std(optB_temp[i]))
    pesB_sd.append(np.std(pesB_temp[i]))
    weiB_sd.append(np.std(weiB_temp[i]))
    optBro_mean.append(np.mean(optBro_temp[i]))
    pesBro_mean.append(np.mean(pesBro_temp[i]))
    weiBro_mean.append(np.mean(weiBro_temp[i]))
    optBro_sd.append(np.std(optBro_temp[i]))
    pesBro_sd.append(np.std(pesBro_temp[i]))
    weiBro_sd.append(np.std(weiBro_temp[i]))

    weiSnW_mean.append(np.mean(weiSnW_temp[i]))
    weiSnW_sd.append(np.std(weiSnW_temp[i]))

    TV_mean.append(np.mean(TV_temp[i]))
    TV_sd.append(np.std(TV_temp[i]))
    LTE_mean.append(np.mean(LTE_temp[i]))
    LTE_sd.append(np.std(LTE_temp[i]))
    CBRS_mean.append(np.mean(CBRS_temp[i]))
    CBRS_sd.append(np.std(CBRS_temp[i]))
    ISM_mean.append(np.mean(ISM_temp[i]))
    ISM_sd.append(np.std(ISM_temp[i]))

print(len(optB_mean))
x = [25, 50, 100, 200, 300, 500]
xlabel_text = "Memory buffer size"

if p_id == 12 or p_id == 3 or p_id == 4:
    # f, (ax1, ax2) = plt.subplots(2, sharex=True)
    fig = plt.figure(figsize=(8, 4.5))
    gs = gridspec.GridSpec(3, 3)

    ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)
    ax2 = plt.subplot2grid((3, 3), (1, 0), rowspan=2, colspan=3)

    if p_id != 4:
        ax1.errorbar(x, [y / 1000 for y in weiBro_mean], 0, color="black", marker='d', markersize=5, linestyle='-',
                     linewidth=2)
        ax2.errorbar(x, [y / 1000 for y in weiB_mean], 0, marker='d', markersize=5, linestyle='-', linewidth=2)
        ax2.errorbar(x, [y / 1000 for y in weiSnW_mean], 0, marker='d', markersize=5, linestyle='-', linewidth=2)
        ax2.errorbar(x, [y / 1000 for y in TV_mean], 0, marker='*', markersize=5, linestyle='-', linewidth=2)
        ax2.errorbar(x, [y / 1000 for y in LTE_mean], 0, marker='*', markersize=5, linestyle=':', linewidth=2)
        ax2.errorbar(x, [y / 1000 for y in CBRS_mean], 0, marker='*', markersize=5, linestyle='-.', linewidth=2)
        ax2.errorbar(x, [y / 1000 for y in ISM_mean], 0, marker='*', markersize=5, linestyle='--', linewidth=2)

        ax1.legend(["dDSA-ER"], loc="lower right", fontsize=12, ncol=3, frameon=False)
        ax1.set_xticks([])
        ax2.legend(["dDSA-GR", "dDSA-SnW (25)", "GR(TV)", "GR(LTE)", "GR(CBRS)", "GR(ISM)"], loc="upper left",
                   fontsize=12, ncol=3, frameon=False)

    else:
        ax1.errorbar(x, weiBro_mean, 0, color="black", marker='d', markersize=5, linestyle='-', linewidth=2)
        ax2.errorbar(x, weiB_mean, 0, marker='d', markersize=5, linestyle='-', linewidth=2)
        ax2.errorbar(x, weiSnW_mean, 0, marker='d', markersize=5, linestyle='-', linewidth=2)
        ax2.errorbar(x, TV_mean, 0, marker='*', markersize=5, linestyle='-', linewidth=2)
        ax2.errorbar(x, LTE_mean, 0, marker='*', markersize=5, linestyle=':', linewidth=2)
        ax2.errorbar(x, CBRS_mean, 0, marker='*', markersize=5, linestyle='-.', linewidth=2)
        ax2.errorbar(x, ISM_mean, 0, marker='*', markersize=5, linestyle='--', linewidth=2)

        ax1.legend(["dDSA-ER"], loc="lower right", fontsize=12, ncol=3, frameon=False)
        ax1.set_xticks([])
        ax2.legend(["dDSA-GR", "dDSA-SnW (25)", "GR(TV)", "GR(LTE)", "GR(CBRS)", "GR(ISM)"], bbox_to_anchor=(0.01, 0.5),
                   loc="upper left", fontsize=12, ncol=3, frameon=False)

    ax1.yaxis.set_tick_params(labelsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xticks(x, ["25", "50", "100", "200", "300", "Unlimited"])
    # plt.xlim(45, 7)

    if p_id == 3:
        ax2.set_ylim(0, 16)
        fig.text(0.02, 0.5, 'Cons. energy per del. message(kJ)', va='center', rotation='vertical', fontsize=15)
        fig.text(0.35, 0.02, xlabel_text, fontsize=15)
        fig_name = "Plots/energy_mem_SER.eps"

    elif p_id == 4:
        fig.text(0.02, 0.5, 'Packet overhead', va='center', rotation='vertical', fontsize=15)
        fig.text(0.3, 0.02, xlabel_text, fontsize=15)
        fig_name = "Plots/overhead_mem_SER.eps"

    elif p_id == 12:
        # ax2.set_ylim(0, 16)
        fig.text(0.04, 0.5, 'Num. of transmissions(x1000)', va='center', rotation='vertical', fontsize=15)
        fig.text(0.3, 0.02, xlabel_text, fontsize=15)
        fig_name = "Plots/trans_mem_SER.eps"

else:
    plt.figure(figsize=(8, 4.5))
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xticks(x, ["25", "50", "100", "200", "300", "Unlimited"])

    # plt.xlim(0,12)
    fig_name = "dummy.eps"
    plt.xlabel(xlabel_text, fontsize=25)

    if p_id == 1:
        plt.ylabel('Message delivery ratio', fontsize=25)
        plt.ylim(-0.1,1.1)
        fig_name = "Plots/pdr_mem_SER.eps"

    if p_id == 2:
        plt.ylabel('Network delay (min)', fontsize=25)
        fig_name = "Plots/latency_mem_SER.eps"

    # if p_id == 3:
    #
    #     plt.ylabel('Energy per packet (kJ)', fontsize=25)
    #     fig_name = "Plots/energy_mem_SER.eps"

    # if p_id == 4:
    #     # plt.ylim(0, 65)
    #
    #     plt.ylabel('Message overhead', fontsize=25)
    #     # plt.ylim(-1, 20)
    #     fig_name = "Plots/overhead_mem_SER.eps"

    if p_id == 5:
        # plt.ylim(0, 65)

        plt.ylabel('Avg num. of hops', fontsize=25)
        # plt.ylim(-1, 20)
        fig_name = "Plots/hops_mem_SER.eps"

    # plt.errorbar(x, optB_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    # plt.errorbar(x, pesB_mean, 0, marker='x', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, weiB_mean, 0, marker='d', markersize=5, linestyle='-', linewidth=2)
    # plt.errorbar(x, optBro_mean, 0, marker='o', markersize=5, linestyle='-', linewidth=1)
    # plt.errorbar(x, pesBro_mean, 0, marker='x', markersize=5, linestyle='--', linewidth=1)
    plt.errorbar(x, weiBro_mean, 0, color="black", marker='d', markersize=5, linestyle='-', linewidth=2)
    plt.errorbar(x, weiSnW_mean, 0, marker='d', markersize=5, linestyle='-', linewidth=2)

    plt.errorbar(x, TV_mean, 0, marker='*', markersize=5, linestyle='-', linewidth=2)
    plt.errorbar(x, LTE_mean, 0, marker='*', markersize=5, linestyle=':', linewidth=2)
    plt.errorbar(x, CBRS_mean, 0, marker='*', markersize=5, linestyle='-.', linewidth=2)
    plt.errorbar(x, ISM_mean, 0, marker='*', markersize=5, linestyle='--', linewidth=2)


    routing_name_list = ["dDSA-GR",  "dDSA-ER", "dDSA-SnW(25)", "GR(TV)", "GR(LTE)", "GR(CBRS)", "GR(ISM)"]
    if p_id == 1:
        plt.legend(routing_name_list, loc="lower left", fontsize=12, ncol = 3, frameon=False)
    elif p_id == 2:
        plt.legend(routing_name_list, loc="upper left", bbox_to_anchor=(0.1, 0.85), fontsize=12, ncol = 3, frameon=False)
    elif p_id ==3:
        plt.legend(routing_name_list, loc="upper left", fontsize=12, ncol = 3, frameon=False)
    elif p_id ==5:
        plt.legend(routing_name_list, loc="upper left",  bbox_to_anchor=(0.01, 0.65), fontsize=12, ncol = 3, frameon=False)

if p_id != 12 and p_id != 3:
    plt.tight_layout()
plt.savefig(fig_name)

plt.show()