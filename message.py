class Message(object):                                                                          #Message Object
    def __init__(self, ID, src, des, genT, size, prev_bands_used, bands, path, replica, packet_id, hops):
        self.ID = int(ID)
        self.src = int(src)
        self.des = int(des)
        self.genT = int(genT)
        self.size = int(size)
        self.band_usage = prev_bands_used
        self.bands = bands
        self.path = path
        self.curr = int(src)
        self.last_sent = -1
        self.totalEnergy = 0
        self.replica = replica
        self.packet_id = packet_id
        self.num_copies = 1
        self.hops = hops

    def set(self, lastSent, copies, curr):
        self.last_sent = lastSent
        self.num_copies = copies
        self.curr = curr
        self.hops += 1

    def change_num_copies(self, copies):
        self.num_copies = copies

    def band_used(self, s):
        self.band_usage[s] += 1

    def create_copies(self, nc):
        self.num_copies = nc

    def get_num_copies(self):
        return self.num_copies