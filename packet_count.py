

path = "Generated_Messages/generated_messages"
max = 0
min = 99999
avg = 0

for i in range(100):
    file = path + str(i) + ".txt"

    with open(file) as f:
        lines = f.readlines()[1:]

    total_mb = 0
    for line in lines:
        line_arr = line.strip().split()

        if int(line_arr[4]) == 60:
            total_mb += 300
        else:
            total_mb += int(line_arr[4])

    packets = total_mb/300
    avg += packets

    if packets > max:
        max = packets
    if packets < min:
        min = packets

print("Max:", max, "Min:", min, "AVG:", avg/100)
