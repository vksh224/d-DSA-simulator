import numpy
import math
import os
import random

from constants import *

# Get minimum of spectrum bandwidths available at two nodes i and j at time t
# This is important because we can only use the common channels (available at both the nodes) as the total bandwidth of the band
# Moreover, note that here we assumed that the channels available at the node (with lower bandwidth) is also existent at the node
# with higher bandwidth of a certain band

def getMinBWFromDMFiles(directory, i, j, s, t):
    with open(directory + "/" + str(i) + ".txt") as fi:
        next(fi)
        iLines = fi.readlines()
    fi.close()

    with open(directory + "/" + str(j) + ".txt") as fj:
        next(fj)
        jLines = fj.readlines()
    fj.close()

    currBW = 0
    for iLine in iLines:
        iLineArr = iLine.strip().split(' ')
        for jLine in jLines:
            jLineArr = jLine.strip().split(' ')
            # print ("At time " + str(t) + " Values: " + iLineArr[0] + " " + jLineArr[0])
            if int(iLineArr[0]) == t and int(jLineArr[0]) == t:
                # print("At time " + str(t) + " Values: " + iLineArr[3] + " " + jLineArr[3])
                if int(iLineArr[s + 3]) < int(jLineArr[s + 3]):
                    currBW = int(iLineArr[s + 3])
                    return currBW
                else:
                    currBW = int(jLineArr[s + 3])
                    return currBW
                    # else:
                    #     print (str(t) + " " + iLineArr[0] + " " + jLineArr[0])
    return currBW


# Compute tau defined as the least message transmission delay in transmitting a message of least size over the spectrum band with
# highest bandwidth across all times t = 0, 1, .... T
def computeTau():
    return 1


# Get the dynamic bandwidth of any given band in the set S, between any node pair at any time epoch t
def getSpecBW(V, S, T):
    specBW = numpy.zeros(shape=(V, V, numSpec, T))  # Initialize the dynamic spectrum bandwidth

    for i in range(V):
        for j in range(V):
            for s in range(len(S)):
                for t in range(0, T, tau):
                    specBW[i, j, s, t] = minBW[s]
                    # getMinBWFromDMFiles(directory, i, j, s, t)
                    # print ("SpecBW: i= " + str(i) + " j= " + str(j) + " s= " + str(s) + " t= " + str(t) + " BW= " + str(specBW[i, j, s, t]))
    return specBW


# Check if a pair of nodes i and j are sufficienctly in communication range over any band type s, starting at time ts until time te
def createLinkExistenceADJ():

    LINK_EXISTS = numpy.empty(shape=(V, V, numSpec, T, T))
    LINK_EXISTS.fill(math.inf)

    for i in range(V):
        for s in S:
            for t in range(T - 1, 1):
                LINK_EXISTS[i, i, s, t, t + 1] = 1

    # # t = [0,1]
    # LINK_EXISTS[0, 1, 0, 0, 1] = 1
    # LINK_EXISTS[1, 0, 0, 0, 1] = 1
    # LINK_EXISTS[0, 1, 1, 0, 1] = 1
    # LINK_EXISTS[1, 0, 1, 0, 1] = 1
    # LINK_EXISTS[1, 3, 0, 0, 1] = 1
    # LINK_EXISTS[3, 1, 0, 0, 1] = 1
    #
    # #t = [1,2]
    # LINK_EXISTS[1, 3, 0, 1, 2] = 1
    # LINK_EXISTS[3, 1, 0, 1, 2] = 1
    # LINK_EXISTS[1, 3, 1, 1, 2] = 1
    # LINK_EXISTS[3, 1, 1, 1, 2] = 1
    # LINK_EXISTS[2, 3, 0, 1, 2] = 1
    # LINK_EXISTS[3, 2, 0, 1, 2] = 1
    # LINK_EXISTS[2, 3, 1, 1, 2] = 1
    # LINK_EXISTS[3, 2, 1, 1, 2] = 1
    #
    # # t= [2,3]
    # LINK_EXISTS[0, 1, 0, 2, 3] = 1
    # LINK_EXISTS[1, 0, 0, 2, 3] = 1
    # LINK_EXISTS[1, 3, 0, 2, 3] = 1
    # LINK_EXISTS[3, 1, 0, 2, 3] = 1
    # LINK_EXISTS[2, 3, 0, 2, 3] = 1
    # LINK_EXISTS[3, 2, 0, 2, 3] = 1
    # LINK_EXISTS[2, 3, 1, 2, 3] = 1
    # LINK_EXISTS[3, 2, 1, 2, 3] = 1
    #
    # # t = [3,4]
    # LINK_EXISTS[0, 3, 0, 3, 4] = 1
    # LINK_EXISTS[3, 0, 0, 3, 4] = 1
    # LINK_EXISTS[0, 3, 1, 3, 4] = 1
    # LINK_EXISTS[3, 0, 1, 3, 4] = 1
    # LINK_EXISTS[2, 3, 0, 3, 4] = 1
    # LINK_EXISTS[3, 2, 0, 3, 4] = 1

    # t = [0,1]
    LINK_EXISTS[0, 1, 0, 0, 1] = 1
    LINK_EXISTS[0, 1, 1, 0, 1] = 1
    LINK_EXISTS[0, 2, 0, 0, 1] = 1
    LINK_EXISTS[0, 2, 1, 0, 1] = 1
    LINK_EXISTS[0, 4, 2, 0, 1] = 1
    LINK_EXISTS[1, 2, 0, 0, 1] = 1
    LINK_EXISTS[1, 0, 0, 0, 1] = 1
    LINK_EXISTS[1, 0, 1, 0, 1] = 1
    LINK_EXISTS[2, 0, 0, 0, 1] = 1
    LINK_EXISTS[2, 0, 1, 0, 1] = 1
    LINK_EXISTS[2, 1, 0, 0, 1] = 1
    LINK_EXISTS[2, 3, 1, 0, 1] = 1
    LINK_EXISTS[3, 2, 1, 0, 1] = 1
    LINK_EXISTS[4, 0, 2, 0, 1] = 1

    # t = [1,2]
    LINK_EXISTS[0, 2, 0, 1, 2] = 1
    LINK_EXISTS[0, 3, 2, 1, 2] = 1
    LINK_EXISTS[0, 4, 1, 1, 2] = 1
    LINK_EXISTS[0, 4, 2, 1, 2] = 1
    LINK_EXISTS[1, 2, 1, 1, 2] = 1
    LINK_EXISTS[1, 2, 2, 1, 2] = 1
    LINK_EXISTS[2, 0, 0, 1, 2] = 1
    LINK_EXISTS[2, 1, 1, 1, 2] = 1
    LINK_EXISTS[2, 1, 2, 1, 2] = 1
    LINK_EXISTS[2, 3, 1, 1, 2] = 1
    LINK_EXISTS[3, 0, 2, 1, 2] = 1
    LINK_EXISTS[3, 2, 1, 1, 2] = 1
    LINK_EXISTS[3, 4, 2, 1, 2] = 1
    LINK_EXISTS[4, 0, 0, 1, 2] = 1
    LINK_EXISTS[4, 0, 1, 1, 2] = 1
    LINK_EXISTS[4, 3, 2, 1, 2] = 1

    # t = [2,3]
    LINK_EXISTS[0, 3, 0, 2, 3] = 1
    LINK_EXISTS[0, 3, 1, 2, 3] = 1
    LINK_EXISTS[0, 3, 2, 2, 3] = 1
    LINK_EXISTS[0, 4, 0, 2, 3] = 1
    LINK_EXISTS[0, 4, 1, 2, 3] = 1
    LINK_EXISTS[0, 4, 2, 2, 3] = 1
    LINK_EXISTS[1, 2, 0, 2, 3] = 1
    LINK_EXISTS[2, 1, 0, 2, 3] = 1
    LINK_EXISTS[3, 0, 0, 2, 3] = 1
    LINK_EXISTS[3, 0, 1, 2, 3] = 1
    LINK_EXISTS[3, 0, 2, 2, 3] = 1
    LINK_EXISTS[3, 4, 0, 2, 3] = 1
    LINK_EXISTS[3, 4, 1, 2, 3] = 1
    LINK_EXISTS[3, 4, 2, 2, 3] = 1
    LINK_EXISTS[4, 0, 0, 2, 3] = 1
    LINK_EXISTS[4, 0, 1, 2, 3] = 1
    LINK_EXISTS[4, 0, 2, 2, 3] = 1
    LINK_EXISTS[4, 3, 0, 2, 3] = 1
    LINK_EXISTS[4, 3, 1, 2, 3] = 1
    LINK_EXISTS[4, 3, 2, 2, 3] = 1

    # t = [3,4]
    LINK_EXISTS[0, 1, 0, 3, 4] = 1
    LINK_EXISTS[0, 3, 1, 3, 4] = 1
    LINK_EXISTS[1, 0, 0, 3, 4] = 1
    LINK_EXISTS[1, 3, 0, 3, 4] = 1
    LINK_EXISTS[1, 3, 2, 3, 4] = 1
    LINK_EXISTS[2, 4, 1, 3, 4] = 1
    LINK_EXISTS[3, 0, 1, 3, 4] = 1
    LINK_EXISTS[3, 1, 0, 3, 4] = 1
    LINK_EXISTS[3, 1, 2, 3, 4] = 1
    LINK_EXISTS[4, 2, 1, 3, 4] = 1

    # t = [4,5]
    LINK_EXISTS[0, 1, 0, 4, 5] = 1
    LINK_EXISTS[0, 1, 1, 4, 5] = 1
    LINK_EXISTS[1, 0, 0, 4, 5] = 1
    LINK_EXISTS[1, 0, 1, 4, 5] = 1
    LINK_EXISTS[1, 3, 2, 4, 5] = 1
    LINK_EXISTS[2, 3, 0, 4, 5] = 1
    LINK_EXISTS[3, 1, 2, 4, 5] = 1
    LINK_EXISTS[3, 2, 0, 4, 5] = 1
    LINK_EXISTS[3, 4, 0, 4, 5] = 1
    LINK_EXISTS[4, 3, 0, 4, 5] = 1

    return LINK_EXISTS


def funHaversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    # Radius of earth in kilometers is 6371
    m = 1000 * 6371* c
    # print(" dist: " + str(km))
    return m

def euclideanDistance(coor1X, coor1Y, coor2X, coor2Y):
    return (math.sqrt((float(coor1X) - float(coor2X))**2 + (float(coor1Y) - float(coor2Y))**2))

def isFile(object):
    try:
        os.listdir(object)  # tries to get the objects inside of this object
        return False  # if it worked, it's a folder
    except Exception:  # if not, it's a file
        return True


def findfiles(directory):
    # if directory is not 'DieselNet-2007/gps_logs/.DS_Store':
    objects = os.listdir(directory)  # find all objects in a dir

    files = []
    for i in objects:  # check if very object in the folder ...
        if isFile(directory + i):  # ... is a file.
            files.append(i)  # if yes, append it.
    return files

def print5d(adj):
    #print("i j ts m x")
    for i in range(len(adj)):
        for j in range(len(adj[0])):
            for s in range(len(adj[0][0])):
                for ts in range(len(adj[0][0][0])):
                    for te in range(len(adj[0][0][0][0])):
                        if adj[i, j, s, ts, te] != math.inf:
                            print(str(i) + " " + str(j) + " " + str(s) + "  " + str(ts) + " " + str(te) + " = " + str(adj[i, j, s, ts, te]))


def print4d(adj, adj2):
    # print("i j ts m x")
    for i in range(len(adj)):
        for j in range(len(adj[0])):
            for ts in range(len(adj[0][0])):
                for m in range(len(adj[0][0][0])):
                    if (adj[i, j, ts, m] != math.inf or adj2[i, j, ts, m]!= math.inf):
                        print(str(i) + " " + str(j) + " " + str(ts) + " " + str(M[m]) + " = " + str(adj[i, j, ts, m]) + " " + str(adj2[i, j, ts, m]))


def save_4D_in_file(filename, adj):
    #adj[i, j, s, t] for specBW, adj[i, j, t, m] for ADJ_T
    with open(filename, "w") as f:
        f.write("#i j s t\n")
        for i in range(len(adj)):
            for j in range(len(adj[0])):
                for s in range(len(adj[0][0])):
                    for t in range(len(adj[0][0][0])):
                        if adj[i, j, s, t] != math.inf and i != j and adj[i, j, s, t] != -1:
                            f.write(str(i) + " " + str(j) + " " + str(s) + " " + str(t) + " = " + str(adj[i, j, s, t]) + "\n")

    f.close()

def save_5D_in_file(filename, adj):
    with open(path_to_folder + filename, "w") as f:
        f.write("#i j t dt m\n")
        for i in range(len(adj)):
            for j in range(len(adj[0])):
                for t in range(len(adj[0][0])):
                    for dt in range(len(adj[0][0][0])):
                        for m in range(len(adj[0][0][0][0])):
                            if adj[i, j, t, dt, m] != math.inf and i != j:
                                f.write(str(i) + " " + str(j) + " " + str(t) + " " + str(dt) + " " + str(m) + " = " + str(adj[i, j, t, dt, m]) + "\n")

    f.close()

def save_in_file(filename, adj):
    with open(filename, "w") as f:
        f.write("#i j s ts \n")
        for i in range(len(adj)):
            for j in range(len(adj[0])):
                for s in range(len(adj[0][0])):
                    for ts in range(len(adj[0][0][0])):
                        # for te in range(len(adj[0][0][0])):
                        if (adj[i, j, s, ts] != math.inf and i != j):
                            f.write(str(i) + " " + str(j) + " " + str(s) + " " + str(ts) + " = " + str(
                                    adj[i, j, s, ts]) + "\n")

    f.close()

def print3D(adj):
    for i in range(len(adj)):
        for j in range(len(adj[0])):
            for t in range(len(adj[0][0])):
                print(str(i) + " " + str(j) + " " + str(t) + " = " + str(adj[i, j, t]))
