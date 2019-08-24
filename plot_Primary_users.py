import numpy as np
import matplotlib.pyplot as plt


time_epochs = 5
runs = 1

Xchants = np.zeros(shape=(time_epochs, runs))
Xchants_pk = np.zeros(shape=(time_epochs, runs))
Epidemic_ALL = np.zeros(shape=(time_epochs, runs))
Epidemic_LTE = np.zeros(shape=(time_epochs, runs))
Epidemic_TV = np.zeros(shape=(time_epochs, runs))
Epidemic_CBRS = np.zeros(shape=(time_epochs, runs))
Epidemic_ISM = np.zeros(shape=(time_epochs, runs))
SprayNWait_ALL = np.zeros(shape=(time_epochs, runs))
HotPotato_ALL = np.zeros(shape=(time_epochs, runs))

T = 180
startTime = [660, 840]
num_messages = 100
num_mules = 10
num_channel = 10

path = "DataMules/UMass/2007-11-06/1/Link_Exists/"

p_id = 1

pusers = [x for x in range(20, 110, 20)]


for time in startTime:
    t = 0
    for puser in pusers:

        path_to_metrics = path + "LE_" + str(time) + "_" + str(T) + "/" + "XChant/ALL/mules_" + \
                          str(num_mules) + "/channels_" + str(num_channel) + "/P_users_" + str(puser) + \
                          "/" + str(num_messages) + "/metrics.txt"

        with open(path_to_metrics, "r") as f:
            lines = f.readlines()[1:]

        for line in lines:
            line_arr = line.strip().split()

            if "180" in line_arr:
                if time == 660:
                    Xchants_pk[t][0] = line_arr[p_id]
                elif time == 840:
                    Xchants[t][0] = line_arr[p_id]

        t += 1


x = np.array([x for x in range(20,110, 20)])
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.xticks(np.arange(20, 110, 20))
# plt.xlim(0,12)
fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Message delivery ratio', fontsize=25)
    plt.xlabel('Number of primary users', fontsize=25)
    plt.ylim(-0.05,1)
    fig_name = "Plots/pdr_num_Puser_UMass.eps"

if p_id == 2:
    plt.ylim(-1, 65)
    plt.ylabel('Network delay (min)', fontsize=25)
    plt.xlabel('Number of primary users', fontsize=25)

    fig_name = "Plots/latency_num_Puser_UMass.eps"

if p_id == 3:
    plt.ylabel('Energy expenditure (KJ)', fontsize=25)
    plt.xlabel('Number of primary users', fontsize=25)
    plt.ylim(-1, 13)
    fig_name = "Plots/energy_num_Puser_UMass.eps"

if p_id == 4:
    plt.ylabel('Message overhead', fontsize=25)
    plt.xlabel('Number of primary users', fontsize=25)
    plt.ylim(-1, 36)
    fig_name = "Plots/overhead_num_Puser_UMass.eps"

# plt.errorbar(x, Epidemic_CBRS, 0, marker='h', markersize=10, linestyle='--', linewidth=3)
# plt.errorbar(x, Epidemic_ISM, 0, marker='p', markersize=10, linestyle='--', linewidth=3)
# plt.errorbar(x, Epidemic_LTE, 0, marker='v', markersize=10, linestyle='--', linewidth=3)
# plt.errorbar(x, Epidemic_TV, 0, marker='<', markersize=10, linestyle='--', linewidth=3)
plt.errorbar(x, Xchants, 0, marker='D', markersize=10, linestyle='-', linewidth=3, color="#813a5c")
plt.errorbar(x, Xchants_pk, 0, marker='o',markersize=10, linestyle='-', linewidth=3, color="#49FF00")
# plt.errorbar(x, Epidemic_ALL, 0, marker='>', markersize=10, linestyle='-', linewidth=3)
# plt.errorbar(x, SprayNWait_ALL, 0, marker='^', markersize=10, linestyle='-', linewidth=3)
# plt.errorbar(x, HotPotato_ALL, 0, marker='x', markersize=10, linestyle='-', linewidth=3)

# plt.legend(["ER (CBRS)", "ER (ISM)", "ER (LTE)", "ER (TV)", "dDSAaR", "dDSAaR (Ideal)", "S-ER ", "S-SnW ", "S-HP"],
#            loc="center", bbox_to_anchor=(.5, 0.9), fontsize=15, ncol=3, frameon=False)

if p_id == 1:
    plt.legend([ "dDSAaR", "dDSAaR (Ideal)"], loc="center", bbox_to_anchor=(.5,0.9), fontsize=15, ncol = 3, frameon=False)
elif p_id == 2:
    plt.legend([ "dDSAaR", "dDSAaR (Ideal)"], loc="center", bbox_to_anchor=(.5,0.9), fontsize=15, ncol = 3, frameon=False)
elif p_id ==3:
    plt.legend([ "dDSAaR", "dDSAaR (Ideal)"], loc="center", bbox_to_anchor=(.5,0.9), fontsize=15, ncol = 3, frameon=False)
elif p_id ==4:
    plt.legend([ "dDSAaR", "dDSAaR (Ideal)"], loc="center", bbox_to_anchor=(.5,0.9), fontsize=15, ncol = 3, frameon=False)


plt.tight_layout()
plt.savefig(fig_name)

plt.show()





