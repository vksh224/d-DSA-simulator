from STB_help import *

class PrimaryUser(object):

    def __init__(self):
        self.band = -1
        self.channel = -1
        self.x = -1
        self.y = -1
        self.on_off = []
        self.active = False

    def place(self):
        files = findfiles(DataMule_path)
        chosen_file = random.choice(files)

        with open(DataMule_path + chosen_file, 'r') as f:
            lines = f.readlines()[1:]


        rand_index = random.randint(0, len(lines) - 1)
        line_arr = lines[rand_index].strip().split()

        x = float(line_arr[2])
        y = float(line_arr[3])

        while int(x) == 0:
            rand_index = random.randint(0, len(lines) - 1)
            line_arr = lines[rand_index].strip().split()

            x = float(line_arr[2])
            y = float(line_arr[3])

        self.x = x
        self.y = y

    def set(self, x, y, channel, band):
        self.x = x
        self.y = y
        self.channel = channel
        self.band = band

    def flip_is_active(self):
        if self.active == True:
            self.active = False
        else:
            self.active = True

    def is_active(self):
        return self.active

    def get_channel(self):
        return self.channel

    def get_band(self):
        return self.band