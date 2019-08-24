import pickle
from constants import *


LINK_EXISTS = pickle.load(open(link_exists_folder + "LINK_EXISTS.pkl", "rb"))

window = 10


for t in [x for x in range(15, 240, 15)]:

    num_links = 0

    for ts in range(t - window, t + 1):

        for i in range(V):
            for j in range(V):
                for s in range(len(S)):

                    if i != j and LINK_EXISTS[i][j][s][ts] == 1:
                        num_links += 1


    print(t, num_links)
