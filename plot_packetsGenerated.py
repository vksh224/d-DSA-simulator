import numpy as np
import matplotlib.pyplot as plt

msg_files = 1

num_packets = []

path = "Generated_Messages/generated_messages"

for t in [x for x in range(0, 181, 15)]:
    packets_at_t = []
    for i in range(msg_files):
        num_packets_infile = 0
        full_path = path + str(i) + ".txt"
        with open(full_path) as f:
            lines = f.readlines()[1:]

        for line in lines:
           line_arr = line.strip().split()
           if int(line_arr[5]) <= t and int(line_arr[5]) >= t - 15:
               if int(line_arr[4]) == 60:
                   num_packets_infile += 1
               else:
                   pkts = int(line_arr[4]) / 300
                   num_packets_infile += pkts

        packets_at_t.append(num_packets_infile)

    num_packets.append(packets_at_t)

num_packets_mean = []
num_packets_sd = []

for i in range(len(num_packets)):
    num_packets_mean.append(np.mean(num_packets[i]))
    num_packets_sd.append(np.std(num_packets[i]))

x = np.array([x for x in range(0, 181, 15)])
plt.xticks(fontsize=20)
plt.yticks(fontsize=25)
plt.xticks(np.arange(0, 181, 30))


plt.ylabel('Packets generated', fontsize=25)
plt.xlabel('Time (min)', fontsize=25)
fig_name = "Plots/packets_gen.png"

plt.errorbar(x, num_packets_mean, num_packets_sd, marker='o', markersize=3, linestyle='-', linewidth=1, color="red")
plt.tight_layout()
plt.savefig(fig_name)

plt.show()
