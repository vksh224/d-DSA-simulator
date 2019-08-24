from constants import *
import math


time_window = T
print_metrics = True

def create_new_delivered_file():
    output_file = open(path_to_metrics + delivered_file, "w")
    output_file.write("ID\ts\td\tts\tte\tLLC\tsize\tband usage\n")
    output_file.write("----------------------------------------------------\n")



    with open(generated_messages_file, "r") as f:
        msg_lines = f.readlines()[1:]

    with open(path_to_metrics + packet_delivered_file, 'r') as f:
        lines = f.readlines()

    for msg_line in msg_lines:
        msg_arr = msg_line.strip().split()
        msg_id = msg_arr[0]
        msg_size = msg_arr[4]
        num_packets_recieved = 0
        num_packets = math.ceil(int(msg_size) / int(packet_size))
        packetIDs = [x for x in range(num_packets)]
        bands_used = [0, 0, 0, 0]


        for line in lines:
            line_arr = line.strip().split()

            if line_arr[0] == msg_id and int(line_arr[6]) in packetIDs:
                num_packets_recieved += 1
                bands_used[0] += int(line_arr[9])
                bands_used[1] += int(line_arr[10])
                bands_used[2] += int(line_arr[11])
                bands_used[3] += int(line_arr[12])

                packetIDs.remove(int(line_arr[6]))

            if num_packets_recieved == num_packets and len(packetIDs) == 0:
                delivered_line = line_arr[0] + "\t" + line_arr[1] + "\t" + line_arr[2] + "\t" + line_arr[3] + "\t" + line_arr[4] + "\t" + \
                                 line_arr[5] + "\t" + line_arr[7] + "\t" + str(bands_used[0]) + "\t" + str(bands_used[1]) + "\t" + str(bands_used[2]) \
                                 + "\t" + str(bands_used[3]) + "\n"
                output_file.write(delivered_line)
                break


def find_num_msg_gen(t):
    with open(generated_messages_file, "r") as f:
        msg_lines = f.readlines()[1:]

    num_msg = 0
    for line in msg_lines:
        line_arr = line.strip().split()
        if int(line_arr[5]) <= t and int(line_arr[5]) >= t - time_window:
            num_msg += 1

    return num_msg

def compute_overhead_new(time):

    if protocol == "XChant" or protocol == "HotPotato":
        return 1

    with open(generated_messages_file, 'r') as f:
        msg_lines = f.readlines()[1:]

    with open(path_to_metrics + not_delivered_file, "r") as f:
        not_del_lines = f.readlines()[2:]

    with open(path_to_metrics + packet_delivered_file, "r") as f2:
        del_lines = f2.readlines()[1:]

    gen_packets_until_t = 0
    packets_delivered_until_t = 0
    packets_not_delivered_until_t = 0

    for msg in msg_lines:
        msg_arr = msg.strip().split()
        size = int(msg_arr[4])
        gen_t = int(msg_arr[5])
        if gen_t <= time:
            num_of_packets = math.ceil(size/packet_size)
            gen_packets_until_t += num_of_packets

    for line in del_lines:
        line_arr = line.strip().split()
        if(int(line_arr[4]) <= time):
            packets_delivered_until_t += 1

    for line in not_del_lines:
        line_arr = line.strip().split()
        if (int(line_arr[4]) <= time):
            packets_not_delivered_until_t += 1

    if gen_packets_until_t == 0:
        return 0
    else:
        return round(float(packets_not_delivered_until_t)/gen_packets_until_t, 2)

def compute_overhead(time):

    if protocol == "XChant" or protocol == "HotPotato":
        return 1

    with open(path_to_metrics + not_delivered_file, "r") as f:
        not_del_lines = f.readlines()[2:]

    with open(path_to_metrics + packet_delivered_file, "r") as f2:
        del_lines = f2.readlines()[1:]

    packets_delivered = 0
    packets_not_delivered = 0

    for line in del_lines:
        line_arr = line.strip().split()
        if(int(line_arr[4]) <= time):
            packets_delivered += 1

    for line in not_del_lines:
        line_arr = line.strip().split()
        if (int(line_arr[4]) <= time):
            packets_not_delivered += 1

    if(packets_delivered == 0):
        return 0
    else:
        return round(float(packets_not_delivered/packets_delivered), 2)


def find_avg_energy(num_delivered_messages, time):

    with open(path_to_metrics + consumed_energy_file, 'r') as f:
        lines = f.readlines()[1:]

    for line in lines:
        line_arr = line.strip().split()
        if (int(line_arr[0]) == int(time) or int(line_arr[0]) == T - 1):
            # float(line_arr[2]) == 0 ||
            if(num_delivered_messages == 0):
                return 0
            else:
                return round(float(line_arr[1])/num_delivered_messages, 2)

def message_info(mes_list):
    with open(link_exists_folder + generated_messages_file, 'r') as f:
        lines = f.readlines()

    file = open("NOT_delivered.txt", 'w')

    for id in mes_list:
        for line in lines:
            line_arr = line.strip().split()
            if int(id) == int(line_arr[0]):
                file.write(line)
    file.close()

#For X-CHANT only
def compute_band_usage(delivery_time, spec_lines):
    band_usage = [0, 0, 0, 0, 0]
    for sLine in spec_lines:
        sLine = sLine.strip().split()
        sLine = [int(obj) for obj in sLine]

        if sLine[2] + sLine[4] <= delivery_time:
            bands_arr = sLine[5:]
            # print(bands_arr)
            for band in bands_arr:
                if int(band) < 5:
                    band_usage[int(band) - 1] += 1
                else:
                    band_usage[4] += int(int(band)/10)
                    band_usage[int(band)%10 - 1] += 1


    total = sum(band_usage)
    if total > 0:
        band_usage = [round(100*ele/total,2) for ele in band_usage]

    print("Band usage: ",  band_usage, "\n")
    return band_usage

def packets_per_taue(t):
    with open(path_to_metrics + "packets_per_tau.txt", "r") as f:
        lines = f.readlines()[1:]
        packets = 0
        parallel_coms = 0
        for line in lines:
            line_arr = line.strip().split()
            if int(line_arr[0]) <= t:
                packets += int(line_arr[1])
                parallel_coms += int(line_arr[2])
    if t > 0:
        return round(packets/t, 2), round(parallel_coms/t, 2), packets
    else:
        return 0, 0, 0

def compute_ave_hop_count(t):

    with open(path_to_metrics + packet_delivered_file, 'r') as f:
        delivered_lines = f.readlines()[1:]

    num_msg = 0
    total_hops = 0

    maxhop = 0

    for line in delivered_lines:
        line_arr = line.strip().split()
        if int(line_arr[4]) <= t:
            num_msg += 1
            total_hops += int(line_arr[8])
            if int(line_arr[8]) > int(maxhop):
                maxhop = line_arr[8]

    if num_msg > 0:
        return round(total_hops / num_msg, 2), num_msg
    else:
        return 0, num_msg

def compute_hop_counts(t):

    with open(path_to_metrics + packet_delivered_file, 'r') as f:
        delivered_lines = f.readlines()[1:]

    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count_above4 = 0

    for line in delivered_lines:
        line_arr = line.strip().split()
        if int(line_arr[4]) <= t:
            if int(line_arr[8]) == 1:
                count_1 += 1
            elif int(line_arr[8]) == 2:
                count_2 += 1
            elif int(line_arr[8]) == 3:
                count_3 += 1
            elif int(line_arr[8]) == 4:
                count_4 += 1
            else:
                count_above4 += 1
    return count_1, count_2, count_3, count_4, count_above4

def compute_total_band_usage(t):
    bands_used = [0, 0, 0, 0]

    with open(path_to_metrics + delivered_file, "r") as f:
        lines = f.readlines()[2:]
        for line in lines:
            line_arr = line.strip().split()
            if int(line_arr[4]) <= t:
                bands_used[0] += int(line_arr[7])
                bands_used[1] += int(line_arr[8])
                bands_used[2] += int(line_arr[9])
                bands_used[3] += int(line_arr[10])

    with open(path_to_metrics + not_delivered_file, "r") as f:
        lines = f.readlines()[2:]
        for line in lines:
            line_arr = line.strip().split()
            if int(line_arr[4]) <= t:
                bands_used[0] += int(line_arr[10])
                bands_used[1] += int(line_arr[11])
                bands_used[2] += int(line_arr[12])
                bands_used[3] += int(line_arr[13])

    total = bands_used[0] + bands_used[1] + bands_used[2] + bands_used[3]
    if total > 0:
        print([band/total for band in bands_used] )
    return bands_used


    # with open(path_to_metrics + "band_usage.txt", "w") as f:
    #     for band in bands_used:
    #         if total > 0:
    #             f.write(str(band/total) + "\n")



def compute_metrics(lines, total_messages, delivery_time, spec_lines):

    delivered = 0
    latency = 0
    energy = 0
    mes_IDs = []
    #band_usage = [0, 0, 0, 0]

    #all_IDs = [x for x in range(num_messages)]
    unique_messages = []

    for line in lines:
        line_arr = line.strip().split()
        if int(line_arr[4]) <= delivery_time and int(line_arr[4]) >= delivery_time - time_window and int(line_arr[3]) <= delivery_time and int(line_arr[3]) >= delivery_time - time_window and int(line_arr[0]) not in mes_IDs:
            delivered += 1
            latency += int(line_arr[5])
            # energy += float(line_arr[7])
            unique_messages.append(line_arr)
            mes_IDs.append(int(line_arr[0]))
            # band_usage[0] += int(line_arr[7])
            # band_usage[1] += int(line_arr[8])
            # band_usage[2] += int(line_arr[9])
            # band_usage[3] += int(line_arr[10])

    band_usage = compute_total_band_usage(delivery_time)

    total = band_usage[0] + band_usage[1] + band_usage[2] + band_usage[3]
    if total > 0:
        band_usage = [ele/ total for ele in band_usage]

    if protocol == "XChant":
        band_usage = compute_band_usage(delivery_time, spec_lines)

    if delivered > 0:
        latency = round(float(latency)/delivered, 2)
        # energy = float(energy)/delivered

    avg_energy = find_avg_energy(delivered, delivery_time)

    if total_messages > 0:
        delivered = round(float(delivered) / total_messages, 2)

    overhead = compute_overhead_new(delivery_time)

    avg_hops_per_packet, num_packets = compute_ave_hop_count(delivery_time)

    count_1, count_2, count_3, count_4, count_above4 = compute_hop_counts(delivery_time)

    pkt_per_tau, parallel_coms, num_transmissions = packets_per_taue(delivery_time)


    # if num_packets > 0:
    #     eng = round(avg_energy/num_packets, 2)
    # else:
    #     eng = 0

    if print_metrics == True:

        print("t: ", t, " msg: ", total_messages, " del: ", delivered, "lat: ", latency, " Overhead: ", overhead, "Energy: ",\
              avg_energy, "AVG hops:", avg_hops_per_packet, "#hops [2,3,4,5+]: [", count_2, count_3, count_4, count_above4, "], PPT: ", pkt_per_tau, "PC:", parallel_coms, "num trans:", num_transmissions)
        # print("band usage:", band_usage[0], band_usage[1], band_usage[2], band_usage[3])

    return delivered, latency, avg_energy, mes_IDs, unique_messages, overhead, band_usage, avg_hops_per_packet, pkt_per_tau, parallel_coms, num_transmissions

#Main starts here

# create_new_delivered_file()

with open(generated_messages_file, "r") as f:
    msg_lines = f.readlines()[1:]

total_messages = len(msg_lines) - 1

metric_file = open(path_to_metrics + metrics_file, "w")
with open(path_to_metrics + delivered_file, "r") as f:
    lines = f.readlines()[2:]

if protocol == "XChant":
    with open(path_to_LLC + "LLC_Spectrum.txt", "r") as f:
        spec_lines = f.readlines()[1:]
else:
    spec_lines = []


fsorted = open(path_to_metrics + "sorted_delivery.txt", "w")
#sort the lines based on LLC i.e., column 5

fsorted.write("ID	s	d	ts	te	LLC	size	parent	parentTime	replica\n")

lines = sorted(lines, key=lambda line: int(line.split()[5]))

for line in lines:
    fsorted.write(line)
fsorted.close()

delivery_times = [i for i in range(0, T + 10, metric_interval)]

metric_file.write("#t\tPDR\tLatency\tEnergy\tOverhead\tHops\tBand Usage\t\t\t\tPacket per tau\tParallel Communications\t Num Transmissions\n")
for t in delivery_times:

    num_msgs_gen = find_num_msg_gen(t)

    avg_pdr, avg_latency, avg_energy, mes_IDs, unique_messages, overhead, band_usage, hops, pkt_per_tau, parallel_coms, num_trans = compute_metrics(lines, num_msgs_gen, t, spec_lines)
    metric_file.write(
        str(t) + "\t" + str(avg_pdr) + "\t" + str(avg_latency) + "\t" + str(avg_energy) + "\t" + str(overhead) + "\t" + str(hops) + "\t" +
        str(round(band_usage[0],3)) + "\t" + str(round(band_usage[1], 3)) + "\t" + str(round(band_usage[2], 3)) + "\t" + str(round(band_usage[3], 3)) + "\t" + str(pkt_per_tau) + "\t" + str(parallel_coms) + "\t" + str(num_trans) +"\n")

metric_file.close()
# print("Delivered messages", sorted(mes_IDs))

# compute_total_band_usage()

with open(path_to_metrics + "unique_messages.txt", "w") as f:
    f.write("ID\ts\td\tts\tte\tLLC\tsize\n")
    f.write("------------------------------\n")

    for msg_line in unique_messages:
        for word in msg_line[:7]:
            f.write(str(word) + "\t")
        f.write("\n")

# message_info(all_IDs)

