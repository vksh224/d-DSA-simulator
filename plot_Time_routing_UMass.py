import numpy as np
import matplotlib.pyplot as plt



time_epochs = 13
runs = 2

Xchants = np.zeros(shape=(time_epochs, runs))
Xchants_pk = np.zeros(shape=(time_epochs, runs))
Epidemic_ALL = np.zeros(shape=(time_epochs, runs))
Epidemic_LTE = np.zeros(shape=(time_epochs, runs))
Epidemic_TV = np.zeros(shape=(time_epochs, runs))
Epidemic_CBRS = np.zeros(shape=(time_epochs, runs))
Epidemic_ISM = np.zeros(shape=(time_epochs, runs))
SprayNWait_ALL = np.zeros(shape=(time_epochs, runs))
HotPotato_ALL = np.zeros(shape=(time_epochs, runs))

num_mules = 10
T = 180
startTime = 840
num_messages = 100
days = [ "2007-11-06"]
folder_nums = [x for x in range(1,11, 1)]
bands_epi = ["ALL"]
bands = ["ALL"]
protocols = ["Epidemic_Smart_optimistic", "Epidemic_Smart_pessimistic", "Epidemic_Smart_random",]
metrics_file = "metrics.txt"

p_id = 1 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

t = 0

for i in range(len(days)):
    for protocol in protocols:
        if "Epidemic" in protocol:
            for band in bands_epi:
                path = "DataMules/UMass/" + days[i] + "/1/Link_Exists/LE_" + str(startTime) + "_" + str(T) + "/" + protocol + "/" + band + "/mules_" + str(num_mules) + "/channels_10/P_users_20/" + str(num_messages) + "/"
                with open(path + metrics_file, "r") as f:
                    lines = f.readlines()[1:]

                for line in lines:
                    line_arr = line.strip().split()

                    if band == "ALL":
                        Epidemic_ALL[t][i] = float(line_arr[p_id])
                    elif band == "LTE":
                        Epidemic_LTE[t][i] = float(line_arr[p_id])
                    elif band == "TV":
                        Epidemic_TV[t][i] = float(line_arr[p_id])
                    elif band == "CBRS":
                        Epidemic_CBRS[t][i] = float(line_arr[p_id])
                    elif band == "ISM":
                        Epidemic_ISM[t][i] = float(line_arr[p_id])
        else:
            for band in bands:
                path = "DataMules/UMass/" + days[i] + "/1/Link_Exists/LE_" + str(startTime) + "_" + str(T) + "/" + protocol + "/" + band + "/" + str(num_mules) + "/" + str(num_messages) + "/"
                with open(path + metrics_file, "r") as f:
                    lines = f.readlines()[1:]

                for line in lines:
                    line_arr = line.strip().split()

                    if protocol == "XChant":
                        Xchants[t][i] = float(line_arr[p_id])
                    elif protocol == "SprayNWait":
                        SprayNWait_ALL[t][i] = float(line_arr[p_id])
                    elif protocol == "HotPotato":
                        HotPotato_ALL[t][i] == float(line_arr[p_id])

    t += 1

t = 0
#
# for i in range(len(days)):
#     for band in bands:
#         path = "DataMules/UMass/" + days[i] + "/1/Link_Exists/LE_" + str(startTime) + "_" + str(
#             T) + "/XChant/" + band + "/" + str(num_mules) + "/" + str(num_messages) + "/"
#         with open(path + "metrics_opt.txt", "r") as f:
#             lines = f.readlines()[1:]
#
#         for line in lines:
#             line_arr = line.strip().split()
#             Xchants_pk[t][i] = float(line_arr[p_id])
#
#     t += 1



if p_id == 3:
    for t in range(len(Xchants)):
        for run in range(runs):
            Xchants[t][run] = float(Xchants[t][run]) / 1000
            Xchants_pk[t][run] = float(Xchants_pk[t][run])/1000
            Epidemic_ALL[t][run] = float(Epidemic_ALL[t][run]) / 1000
            Epidemic_TV[t][run] = float(Epidemic_TV[t][run]) / 1000
            Epidemic_LTE[t][run] = float(Epidemic_LTE[t][run]) / 1000
            Epidemic_ISM[t][run] = float(Epidemic_ISM[t][run]) / 1000
            Epidemic_CBRS[t][run] = float(Epidemic_CBRS[t][run]) / 1000
            SprayNWait_ALL[t][run] = float(SprayNWait_ALL[t][run])/1000
            HotPotato_ALL[t][run] = float(HotPotato_ALL[t][run])/1000

Xchants_mean = []
Xchants_SD = []
Xchants_mean_pk = []
Xchants_SD_pk = []
Epidemic_ALL_mean = []
Epidemic_ALL_SD = []
Epidemic_CBRS_mean = []
Epidemic_CBRS_SD = []
Epidemic_ISM_mean = []
Epidemic_ISM_SD = []
Epidemic_LTE_mean = []
Epidemic_LTE_SD = []
Epidemic_TV_mean = []
Epidemic_TV_SD = []
SprayNWait_ALL_mean = []
SprayNWait_ALL_SD = []
HotPotato_ALL_mean = []
HotPotato_ALL_SD = []

for i in range(len(Xchants)):
    Xchants_mean.append(np.mean(Xchants[i]))
    Xchants_SD.append(np.std(Xchants[i]))
    Xchants_mean_pk.append(np.mean(Xchants_pk[i]))
    Xchants_SD_pk.append(np.std(Xchants_pk[i]))
    SprayNWait_ALL_mean.append(np.mean(SprayNWait_ALL[i]))
    SprayNWait_ALL_SD.append(np.std(SprayNWait_ALL[i]))
    HotPotato_ALL_mean.append(np.mean(HotPotato_ALL[i]))
    HotPotato_ALL_SD.append(np.std(HotPotato_ALL[i]))
    Epidemic_ALL_mean.append(np.mean(Epidemic_ALL[i]))
    Epidemic_ALL_SD.append(np.std(Epidemic_ALL[i]))
    Epidemic_CBRS_mean.append(np.mean(Epidemic_CBRS[i]))
    Epidemic_CBRS_SD.append(np.std(Epidemic_CBRS[i]))
    Epidemic_ISM_mean.append(np.mean(Epidemic_ISM[i]))
    Epidemic_ISM_SD.append(np.std(Epidemic_ISM[i]))
    Epidemic_LTE_mean.append(np.mean(Epidemic_LTE[i]))
    Epidemic_LTE_SD.append(np.std(Epidemic_LTE[i]))
    Epidemic_TV_mean.append(np.mean(Epidemic_TV[i]))
    Epidemic_TV_SD.append(np.std(Epidemic_TV[i]))


x = np.array([x for x in range(0,T +1, 15)])
print(len(x), len(Epidemic_ALL))
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.xticks(np.arange(1, 11, 2))
# plt.xlim(0,12)
fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Message delivery ratio', fontsize=25)
    plt.xlabel('Number of data mules', fontsize=25)
    plt.ylim(-0.05,1.25)
    fig_name = "Plots/pdr_nodes_UMass.eps"

if p_id == 2:
    plt.ylim(-1, 65)
    plt.ylabel('Network delay (min)', fontsize=25)
    plt.xlabel('Number of data mules', fontsize=25)

    fig_name = "Plots/latency_nodes_UMass.eps"

if p_id == 3:
    plt.ylabel('Energy expenditure (KJ)', fontsize=25)
    plt.xlabel('Number of data mules', fontsize=25)
    plt.ylim(-1, 13)
    fig_name = "Plots/energy_nodes_UMass.eps"

if p_id == 4:
    plt.ylabel('Message overhead', fontsize=25)
    plt.xlabel('Number of data mules', fontsize=25)
    plt.ylim(-1, 36)
    fig_name = "Plots/overhead_nodes_UMass.eps"

plt.errorbar(x, Epidemic_CBRS_mean, 0, marker='h', markersize=10, linestyle='--', linewidth=3)
plt.errorbar(x, Epidemic_ISM_mean, 0, marker='p', markersize=10, linestyle='--', linewidth=3)
plt.errorbar(x, Epidemic_LTE_mean, 0, marker='v', markersize=10, linestyle='--', linewidth=3)
plt.errorbar(x, Epidemic_TV_mean, 0, marker='<', markersize=10, linestyle='--', linewidth=3)
plt.errorbar(x, Xchants_mean, 0, marker='D', markersize=10, linestyle='-', linewidth=3, color="#813a5c")
plt.errorbar(x, Xchants_mean_pk, 0, marker='o',markersize=10, linestyle='-', linewidth=3, color="#49FF00")
plt.errorbar(x, Epidemic_ALL_mean, 0, marker='>', markersize=10, linestyle='-', linewidth=3)
plt.errorbar(x, SprayNWait_ALL_mean, 0, marker='^', markersize=10, linestyle='-', linewidth=3)
plt.errorbar(x, HotPotato_ALL_mean, 0, marker='x', markersize=10, linestyle='-', linewidth=3)



if p_id == 1:
    plt.legend([ "ER (CBRS)","ER (ISM)","ER (LTE)","ER (TV)","dDSAaR", "dDSAaR (Ideal)", "S-ER ","S-SnW ", "S-HP"], loc="center", bbox_to_anchor=(.5,0.9), fontsize=15, ncol = 3, frameon=False)
elif p_id == 2:
    plt.legend([  "ER (CBRS)","ER (ISM)","ER (LTE)","ER (TV)","dDSAaR", "dDSAaR (Ideal)", "S-ER ","S-SnW ", "S-HP"], loc="lower center", fontsize=15, ncol = 3, frameon=False)
elif p_id ==3:
    plt.legend([ "ER (CBRS)","ER (ISM)","ER (LTE)","ER (TV)","dDSAaR", "dDSAaR (Ideal)", "S-ER ","S-SnW ", "S-HP"], loc="upper left", fontsize=15, ncol = 3, frameon=False)
elif p_id ==4:
    plt.legend([  "ER (CBRS)","ER (ISM)","ER (LTE)","ER (TV)","dDSAaR", "dDSAaR (Ideal)", "S-ER ","S-SnW ", "S-HP"], loc="upper left", fontsize=15, ncol = 3, frameon=False)


plt.tight_layout()
plt.savefig(fig_name)

plt.show()