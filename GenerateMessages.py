from constants import *
import random
import os

def get_possible_msgs(t, path_lines):
    msgs = []
    for line in path_lines:
        line_arr = line.strip().split()

        if int(line_arr[2]) < t + 5 and int(line_arr[2]) > t - 5 and int(line_arr[0]) < NoOfSources \
                and int(line_arr[1]) < NoOfSources + NoOfDataCenters and int(line_arr[1]) >= NoOfSources \
                and len(line_arr) > 8:

                msgs.append(line)


            # path_lines.remove(line)
    return msgs


num_gen = 10

for i in range(num_gen):
    print(i)

    #We need this, to ensure that the generated messages at a certain source node has a potential path to the destined node.
    # This becomes crucial because the buses travel on a pre-defined route, and it may so happen that there never exists a path for
    # a certain message from its source to destination, esp, in case of optimistic approaches.

    # with open(path_to_LLC + "LLC_PATH.txt", "r") as fp:
    #     path_lines = fp.readlines()[1:]
    # fp.close()

    min_burst = 10
    max_burst = 30

    min_wait = 10
    max_wait = 20

    msg_file_path = "Generated_Messages/mean" + str(int((min_wait + max_wait)/ 2))
    if not os.path.exists(msg_file_path):
        os.makedirs(msg_file_path)
    message_file = open(msg_file_path + "/generated_messages" + str(i) + ".txt", "w")
    message_file.write("ID\ts\td\tTTL\tsize\tgenT\n")

    t = 0
    msg_count = 0

    while t < 300:
        # print(t)
        num_msg_to_gen = random.randint(min_burst, max_burst)
        time_to_next_burst = random.randint(min_wait, max_wait)

        # msgs = get_possible_msgs(t, path_lines)

        for i in range(num_msg_to_gen):
            #if len(msgs) > 0:
            # msg_line = random.choice(msgs)
            # msgs.remove(msg_line)

            # msg_line_arr = msg_line.strip().split()

            # src = int(msg_line_arr[0])
            # dst = int(msg_line_arr[1])
            # genT = int(msg_line_arr[2])
            # desired_TTL = random.randint(minTTL, TTL)

            src = random.randint(0, NoOfSources - 1)
            des = random.randint(NoOfSources, NoOfSources + NoOfDataCenters - 1)
            desired_TTL = random.randint(minTTL, TTL)
            genT = t
            p = random.randint(0, 100)
            if p < 70:
                size = random.choice(M[:2])
            else:
                size = random.choice(M[2:])

            line = str(msg_count) + "\t" + str(src) + "\t" + str(des) + "\t" + str(TTL) + "\t" \
                   + str(size) + "\t" + str(t) + "\n"

            message_file.write(line)

            msg_count += 1

        t += time_to_next_burst

    message_file.close()







