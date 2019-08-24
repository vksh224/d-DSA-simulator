
num_messages = 150
num_packets = 10
num_replicas = 1
msg_count = [[0 for packet in range(num_packets + 1)] for msg in range(num_messages + 1)]

generated_messages_file = 'Generated_Messages/mean15/generated_messages0.txt'
with open(generated_messages_file, "r") as f:
    msg_lines = f.readlines()[1:]

print("total message lines", len(msg_lines))
#ID	s	d	TTL	size	genT

path_to_metrics = 'DataMules/Lexington/50/3/Link_Exists/LE_1_360/Epidemic_Smart_optimistic/PQ/geo_5/mules_48/channels_6/P_users_150/msgfile_0_15/puserfile_0/TTL_216/BuffSize_150/'
which_file = "packets_delivered.txt"

with open(path_to_metrics + which_file, "r") as f:
    lines = f.readlines()[1:]
print("Total lines", len(lines))

for msg_line in msg_lines:
    msg_line_arr = msg_line.strip().split()
    gen_msg_id = msg_line_arr[0]
    gen_msg_src = msg_line_arr[1]
    gen_msg_des = msg_line_arr[2]

    for gen_packet_id in range(num_packets):
        for line in lines:
            line_arr = line.strip().split()
            msg_id = line_arr[0]
            src = line_arr[1]
            des = line_arr[2]
            ts = line_arr[3]
            te = line_arr[4]
            #packet_id = line_arr[8] #in not_delivered_file
            packet_id = line_arr[6]
            if int(gen_msg_id) == int(msg_id) and int(gen_packet_id) == int(packet_id):
                msg_count[int(msg_id)][int(packet_id)] += 1

                # if int(msg_id) == 2 and int(packet_id) == 0:
                #     print(line)
                # print("Msg ID ", msg_id, " Packet ID", packet_id)


total_count = 0
greater_than = 0
for msg_id in range(num_messages):
    for packet_id in range(num_packets):
        total_count += msg_count[msg_id][packet_id]

        if msg_count[msg_id][packet_id] > num_replicas:
            print("Msg ID", msg_id, " Packet ID", packet_id, "Count ", msg_count[msg_id][packet_id])
            greater_than += 1

print ("Total count", total_count, greater_than)

