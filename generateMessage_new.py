from constants import *
import random

message_file = open(DataMule_path + "Link_Exists/generated_messages.txt", "w")

with open(path_to_LLC + "LLC_PATH.txt", "r") as fp:
    path_lines = fp.readlines()[1:]
fp.close()

id = 0
count_messages = 0

message_file.write("ID\ts\td\tTTL\tsize\tgenT\n")
while count_messages < num_messages:
    line = random.choice(path_lines)
    path_lines.remove(line)
    line_arr = line.strip().split()
    # random.shuffle(line_arr)
    src = int(line_arr[0])
    des = int(line_arr[1])
    genT = int(line_arr[2])
    size = int(line_arr[3])
    desired_TTL = random.randint(minTTL, TTL)

    path = line_arr[5:]

    generateMessage = False

    if len(set(path)) >2:
        for nodeId in path:
            if int(nodeId) > NoOfSources + NoOfDataCenters:
                generateMessage = True

    t = random.randint(int(0.1 * T), int(0.3 * T))

    prob_message_size = random.uniform(0, 1)
    if prob_message_size < 0.7 and size >= M[3]:
        size = random.choice(M[:3])

    if generateMessage == True and src < NoOfSources and des >= NoOfSources and des < NoOfSources + NoOfDataCenters and genT <= 0.3 * T:

        p = random.uniform(0, 1)

        if p < 0.05:
            message_file.write(
                str(id) + "\t" + str(src) + "\t" + str(des) + "\t" + str(desired_TTL) + "\t" + str(size) + "\t" + str(
                    t) + "\n")
        else:
            message_file.write(
                str(id) + "\t" + str(src) + "\t" + str(des) + "\t" + str(desired_TTL) + "\t" + str(size) + "\t" + str(
                    genT) + "\t" + line_arr[4] + "\t" + str(path) + "\n")

        # print(str(id) + "\t" + str(src) + "\t" + str(des) + "\t" + str(desired_TTL) + "\t" + str(size) + "\t" + str(genT) )

        id += 1
        count_messages += 1
message_file.close()

