from constants import *
import random


num_gen = 5


for i in range(num_gen):

    message_file = open("Generated_Messages/generated_messages" + str(i) + ".txt", "w")
    message_file.write("ID\ts\td\tTTL\tsize\tgenT\n")

    min_burst = 5
    max_burst = 20

    min_wait = 5
    max_wait = 15

    t = 0
    msg_count = 0

    small = [60, 600]
    large = [1500, 3000]

    while t < T - TTL:
        # print(t)
        num_msg_to_gen = random.randint(min_burst, max_burst)
        time_to_next_burst = random.randint(min_wait, max_wait)


        for i in range(num_msg_to_gen):

            p = random.randint(0,100)

            if p < 80:
                size = random.choice(small)

            else:
                size = random.choice(large)


            src = random.randint(0, NoOfSources - 1)
            dst = random.randint(NoOfSources, NoOfSources + NoOfDataCenters - 1)
            genT = t
            desired_TTL = random.randint(minTTL, TTL)


            line = str(msg_count) + "\t" + str(src) + "\t" + str(dst) + "\t" + str(TTL) + "\t" \
            + str(size) + "\t" + str(t) + "\n"

            message_file.write(line)

            msg_count += 1

        t += time_to_next_burst

    message_file.close()


