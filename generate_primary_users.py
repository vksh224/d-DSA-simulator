from constants import *
from STB_help import *



def pu_on_off_arr():
    on_off_arr = []
    t = T

    while t > 0:
        rand = random.randint(1, 4)
        on_off_arr.append(rand)
        t -= rand

    return on_off_arr



max_puser = 500
rounds = 1
files = findfiles(DataMule_path + "Day1/")

if dataset == "UMass":
    PU_filename = "primary_usersUMass"
    x_pos = 2
    y_pos = 3
else:
    PU_filename = "primary_usersLEX"
    x_pos = 1
    y_pos = 2

for it in range(rounds):
    file_path = "Primary_Users/" + dataset + "/" + str(it)

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    for x in range(max_puser):
        chosen_file = random.choice(files)

        with open(DataMule_path + "Day1/" + chosen_file, 'r') as f:
            lines = f.readlines()[1:]


        rand_index = random.randint(0, len(lines) - 1)
        line_arr = lines[rand_index].strip().split()
        # print(line_arr)

        x = float(line_arr[x_pos])
        y = float(line_arr[y_pos])

        while int(x) == 0:
            rand_index = random.randint(0, len(lines) - 1)
            line_arr = lines[rand_index].strip().split()

            x = float(line_arr[x_pos])
            y = float(line_arr[y_pos])

        band = random.choice([0, 2, 3])
        channel = random.randint(0, default_num_channels - 1)

        p_line = str(x) + "\t" + str(y) + "\t" + str(channel) + "\t" + str(band) + "\n"

        f = open(file_path + "/" + PU_filename + ".txt", "a")
        f.write(p_line)
        f.close()

    for x in range(default_num_channels, 0, -1):
        with open(file_path + "/" + PU_filename + ".txt", "r") as f:
            lines = f.readlines()

            f2 = open(file_path + "/" + PU_filename + "_" + str(x) + ".txt", "w")

            for line in lines:
                line_arr = line.strip().split()

                if int(line_arr[2]) >= x:
                    line_arr[2] = random.randint(0, x - 1)

                new_line = str(line_arr[0]) + "\t" + str(line_arr[1]) + "\t" + str(line_arr[2]) + "\t" + str(line_arr[3]) + "\n"
                f2.write(new_line)

            f2.close()


    o_f_times = open(file_path + "/on_off_times.txt", "a")

    for i in range(500):
        on_off_arr = pu_on_off_arr()
        for j in range(len(on_off_arr)):
            o_f_times.write(str(on_off_arr[j]) + " ")
        o_f_times.write("\n")

    o_f_times.close()



