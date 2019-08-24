import re
import random
import pickle
import shutil
import numpy

from STB_help import *

def dist_between_first_last_coord(coords):
    start_coord = coords[0].strip().split()
    end_coord = coords[len(coords) - 1].strip().split()

    dist = euclideanDistance(float(start_coord[0]), float(start_coord[1]), float(end_coord[0]), float(end_coord[1]))
    return dist

def connect_close_trajectories(DM):
    newDMTrajectories = {}
    do_not_compare = []
    for i in DM.keys():
        if i not in do_not_compare:
            mule1 = DM[i]
            dm1_start = mule1[0].strip().split(" ")
            dm1_end = mule1[len(mule1) - 1].strip().split(" ")
            newDMTrajectories[i] = mule1
            for j in DM.keys():
                if i != j and j not in do_not_compare:

                    mule2 = DM[j]
                    dm2_start = mule2[0].strip().split(" ")
                    dm2_end = mule2[len(mule2) - 1].strip().split(" ")

                    dist1 = euclideanDistance(dm1_end[0], dm1_end[1], dm2_start[0], dm2_start[1])
                    dist2 = euclideanDistance(dm1_start[0], dm1_start[1], dm2_end[0], dm2_end[1])
                    dist3 = euclideanDistance(dm1_end[0], dm1_end[1], dm2_end[0], dm2_end[1])
                    dist4 = euclideanDistance(dm1_start[0], dm1_start[1], dm2_start[0], dm2_start[1])

                    if dist2 < 100:
                        new_mule = mule2 + mule1
                        newDMTrajectories[i] = new_mule
                        do_not_compare.append(j)
                        do_not_compare.append(i)

                    elif dist1 < 100:
                        new_mule = mule1 + mule2
                        newDMTrajectories[i] = new_mule
                        do_not_compare.append(j)
                        do_not_compare.append(i)

                    elif dist3 < 100:
                        new_mule = mule2 + mule1[::-1]
                        newDMTrajectories[i] = new_mule
                        do_not_compare.append(j)
                        do_not_compare.append(i)

                    elif dist4 < 100:
                        new_mule = mule2[::-1] + mule1
                        newDMTrajectories[i] = new_mule
                        do_not_compare.append(j)
                        do_not_compare.append(i)

    return newDMTrajectories

def connectTrajectories(DM):
    newDMTrajectories = {}
    do_not_compare = []
    for i in DM.keys():
        if i not in do_not_compare:
            mule1 = DM[i]
            dm1_start = mule1[0].strip().split(" ")
            dm1_end = mule1[len(mule1) - 1].strip().split(" ")
            newDMTrajectories[i] = mule1
            for j in DM.keys():
                if i != j and j not in do_not_compare:

                    mule2 = DM[j]
                    dm2_start = mule2[0].strip().split(" ")
                    dm2_end = mule2[len(mule2) - 1].strip().split(" ")

                    if dm1_start == dm2_end:
                        new_mule = mule2 + mule1
                        newDMTrajectories[i] = new_mule
                        do_not_compare.append(j)
                        do_not_compare.append(i)

                        break

                    elif dm2_start == dm1_end:
                        new_mule = mule1 + mule2
                        newDMTrajectories[i] = new_mule
                        do_not_compare.append(j)
                        do_not_compare.append(i)

                        break

                    elif dm2_start == dm1_start:
                        new_mule = mule2[::-1] + mule1
                        newDMTrajectories[i] = new_mule
                        do_not_compare.append(j)
                        do_not_compare.append(i)

                        break

                    elif dm2_end == dm1_end:
                        new_mule = mule2 + mule1[::-1]
                        newDMTrajectories[i] = new_mule
                        do_not_compare.append(j)
                        do_not_compare.append(i)

                        break






    return newDMTrajectories

def readTrajectoryFile():
    trajectories = {}
    filepath = "primaryRoads.osm.wkt"
    with open(filepath) as fp:
        lines = fp.readlines()

        for index in range(0, len(lines)):
            patternMatch = re.match(r'^LINESTRING \((.*)\)', lines[index], re.M | re.I)
            if patternMatch:
                # print ("Pattern 1: ", patternMatch.group(1))
                trajectoryCoord = patternMatch.group(1)
                trajCoordArr = trajectoryCoord.strip().split(',')
                # eachDM = trajCoordArr
                # start_coord = eachDM[0].strip().split(" ")
                # end_coord = eachDM[len(eachDM) - 1].strip().split(" ")
                # traj_len = euclideanDistance(start_coord[0], start_coord[1], end_coord[0], end_coord[1])
                # if traj_len > 1000:
                #     print("trajectory", index, "distance:", traj_len)

                if len(trajectoryCoord.strip().split(',')) > 1:
                # if dist_between_first_last_coord(trajCoordArr) > 1600:
                    trajectories[index] = trajectoryCoord.strip().split(',')

            else:
                print ("No Match !!!")

    fp.close()


    final_trajectories = connectTrajectories(trajectories)
    final_trajectories = connectTrajectories(final_trajectories)
    final_trajectories = connectTrajectories(final_trajectories)
    final_trajectories = connectTrajectories(final_trajectories)
    final_trajectories = connectTrajectories(final_trajectories)
    final_trajectories = connectTrajectories(final_trajectories)


    final_trajectories = connect_close_trajectories(final_trajectories)

    traj_list = []
    for i in final_trajectories.keys():
        if len(final_trajectories[i]) > 30:
            traj_list.append(final_trajectories[i])

    return traj_list



def check_dist_between_all_src_des(vil_src, vil_des, new_src, new_des):
    add_new_src_des = True
    adequate_dist = 2000

    # if len(vil_src) == 0:
    #     return True

    for des in vil_des:
        dist = euclideanDistance(float(str(new_src).split()[0]), float(str(new_src).split()[1]), float(str(des).split()[0]),
                                 float(str(des).split()[1]))
        if dist < adequate_dist:
            add_new_src_des = False

    for src in vil_src:
        dist = euclideanDistance(float(str(src).split()[0]), float(str(src).split()[1]), float(str(new_des).split()[0]),
                                 float(str(new_des).split()[1]))
        if dist < adequate_dist:
            add_new_src_des = False

    dist = euclideanDistance(float(str(new_src).split()[0]), float(str(new_src).split()[1]), float(str(new_des).split()[0]),
                             float(str(new_des).split()[1]))

    if dist < adequate_dist:
        add_new_src_des = False

    return add_new_src_des

def getSourceDesCoordinates(src_start, src_end, des_end):

    if day_num == 1:

        bus_routes = pickle.load(open(DataMule_path + "bus_route_ids.pkl", "rb"))
        village_coors = []
        village_src = []
        village_des = []

        bus_routes = list(set(bus_routes))

        print("bus_routes", bus_routes)
        print(src_start, src_end, des_end)
        for srcID in range(src_start, src_end, 1):
            #Choose src and des from bus routes
            route_id = random.choice(bus_routes)
            #bus_routes.remove(route_id)
            print("routeID:", route_id)
            src = random.choice(DMTrajectories[route_id])

            if srcID + src_end >= des_end:
                village_coors[srcID] = src
                print("SRC Route ID", route_id, srcID, src)

            else:
                des = random.choice(DMTrajectories[route_id])
                dist = euclideanDistance(float(str(src).split()[0]), float(str(src).split()[1]), float(str(des).split()[0]), float(str(des).split()[1]))
                count = 0
                adequate_dist = random.randint(2000, 2500)
                while dist < adequate_dist and check_dist_between_all_src_des(village_src, village_des, src, des) == False:
                    count = count + 1
                    if count > len(DMTrajectories[route_id]):
                        route_id = random.choice(bus_routes)
                        # print(route_id)
                        count = 0

                    src = random.choice(DMTrajectories[route_id])
                    des = random.choice(DMTrajectories[route_id])
                    dist = euclideanDistance(float(str(src).split()[0]), float(str(src).split()[1]), float(str(des).split()[0]),
                                             float(str(des).split()[1]))
                    # print(route_id, dist)

                print("SRC Route ID", route_id, srcID, src)
                print("DES Route ID", route_id, srcID + src_end, des, "dist: ", dist, "\n")
                village_src.append(src)
                village_des.append(des)
                # village_coors[srcID] = src
                # village_coors[srcID + src_end] = des

        for x in range(len(village_src)):
            village_coors.append(village_src[x])

        for x in range(len(village_des)):
            village_coors.append(village_des[x])



        f = open(DataMule_path + "village_coor.pkl", 'wb')
        pickle.dump(village_coors, f)
        f.close()

    # else:
    #     dir1 = DataMule_path + "Day1/"
    #     dir2 = DataMule_path + "Day2/"
    #     if not os.path.exists(dir1):
    #         os.makedirs(dir1)
    #     if not os.path.exists(dir2):
    #         os.makedirs(dir2)
    #     for i in range(des_end):
    #         curr_dir = DataMule_path + "Day1/" + str(i) + ".txt"
    #         new_dir = DataMule_path + "Day2/" + str(i) + ".txt"
    #         shutil.copyfile(curr_dir, new_dir)

def getBusRoutes(bus_end):
    bus_routes = []
    num_buses = 0
    srcID = 0

    while num_buses < bus_end:
        bus_routes.append(srcID)
        num_buses += 1
        if srcID == len(DMTrajectories)-1:
            srcID = 0
        else:
            srcID += 1

    f = open(DataMule_path +  "bus_route_ids.pkl", 'wb')
    print("bus route IDs:", bus_routes)
    pickle.dump(bus_routes, f)
    f.close()

def getLocationsOfSourcesAndDataCenters(startIndex, endIndex):
    # create file for Sources. Though the source location are fixed, the spectrum bandwidth changes over time
    # Hence, it is important to save it as a file
    if not os.path.exists(DataMule_path + "Day" + str(day_num)):
        os.makedirs(DataMule_path + "Day" + str(day_num))

    villageCoor = pickle.load(open(DataMule_path + "village_coor.pkl", "rb"))
    for srcID in range(startIndex, endIndex, 1):

        # villageCoor = random.choice(DMTrajectories[srcID%len(DMTrajectories)])
        srcLocationX = villageCoor[srcID].strip().split(" ")[0]
        srcLocationY = villageCoor[srcID].strip().split(" ")[1]
        # print("Location: " + villageCoor[srcID] + " " + srcLocationX + " " + srcLocationY)

        with open(DataMule_path + "Day" + str(day_num) + "/" + str(srcID) + ".txt", "w") as srcP:
            srcP.write("T X Y ")
            for s in S:
                srcP.write("S" + str(s) + " ")
            srcP.write("\n")

            for t in range(0, 2*T, dt):
                srcP.write(str(t) + " " + str(srcLocationX) + " " + str(srcLocationY) + " ")

                # Change the bandwidth of each spectrum at each DSA node at each time epoch
                specBW = [minBW[s] for s in S]
                # print ("Length of spectrum: " + str(S))
                for sBW in specBW:
                    srcP.write(str(sBW) + " ")
                srcP.write("\n")
        srcP.close()


def getLocationsOfDMs(DMTrajectories, startIndex, endIndex):
    dmID = startIndex + NoOfSources + NoOfDataCenters - 1
    num_busses_per_traj = math.floor(V / len(DMTrajectories))

    num_mules_on_traj = {}
    wait_interval = 10
    bus_route_ids = pickle.load(open(DataMule_path+ "bus_route_ids.pkl", "rb"))

    for ind in range(startIndex, endIndex, 1):
        dmID = dmID + 1
        dmSpeed = random.randint(VMIN, VMAX)

        chosen_trajectory_id  = bus_route_ids[ind]
        eachDM = DMTrajectories[chosen_trajectory_id]

        # update wait time dictionary to keep track of buses on same trajectory
        if chosen_trajectory_id in num_mules_on_traj:
            num_mules_on_traj[chosen_trajectory_id] += 1
            currCoorID = math.floor(len(DMTrajectories[chosen_trajectory_id]) * (num_mules_on_traj[chosen_trajectory_id] / num_busses_per_traj))
            if currCoorID == len(DMTrajectories[chosen_trajectory_id]) - 1 or currCoorID == len(DMTrajectories[chosen_trajectory_id]):
                currCoorID -= len(DMTrajectories[chosen_trajectory_id]) - 2
            nextCoorID = currCoorID + 1
        else:
            num_mules_on_traj[chosen_trajectory_id] = 0
            currCoorID = 0
            nextCoorID = currCoorID + 1


        currTime = 0

        # print("Traj:", chosen_trajectory_id, "startCoord:", currCoorID)

        villageCoor = pickle.load(open(DataMule_path + "village_coor.pkl", "rb"))

        # print("Village coors", villageCoor)
        # print("Bus route ", bus_route_ids[ind], DMTrajectories[bus_route_ids[ind]], "\n")

        # print("Trajectory " +  str(len(eachDM)) + " : " + str(eachDM))

        with open(DataMule_path + "Day" + str(day_num) +"/"+ str(dmID)+".txt", "w") as dmP:
            # print ("For DM: " + str(dmID) + " Speed: " + str(dmSpeed))
            dmP.write("T X Y ");
            for s in S:
                dmP.write("S"+ str(s) + " ")
            dmP.write("\n")

            # By default, move in the forward direction
            isDirectionForward = True

            chosen_wait_time = random.choice(wait_time)

            for t in range(currTime, T, dt):
                prevCoors = eachDM[currCoorID].strip().split(' ')
                currCoors = eachDM[nextCoorID].strip().split(' ')

                consumedTime = euclideanDistance(prevCoors[0], prevCoors[1], currCoors[0], currCoors[1])/dmSpeed
                # print("Curr " + str(currCoorID) + " Next " + str(nextCoorID) + " consTime: " + str(consumedTime))
                # if consumedTime > 1:
                #     print("dist:", euclideanDistance(prevCoors[0], prevCoors[1], currCoors[0], currCoors[1]), "speed:", dmSpeed, "consumed time:", consumedTime)

                # if prevCoors in villageCoor:
                if eachDM[currCoorID] in villageCoor and chosen_wait_time > 0:
                    chosen_wait_time -= 1
                    dmP.write(str(t) + " " + eachDM[currCoorID].strip() + " ")
                    # if chosen_wait_time == 1:
                    #     print("Bus ", chosen_trajectory_id, " Time: " , t, " Coor: ", prevCoors, " Cons Time: ", consumedTime)

                elif consumedTime > t or t == T- dt:
                    # Stay in the same location
                    # print (str(t) + " " + str(eachDM[currCoorID]))
                    dmP.write(str(t) + " " + eachDM[currCoorID].strip() + " ")

                else:
                    # Move to the next location
                    dmP.write(str(t) + " " + eachDM[nextCoorID].strip() + " ")

                    #Set the current ID and next ID appropriately
                    currCoorID = nextCoorID

                    #repeat from start of the trajectory (if currently at the end of the trajectory)
                    # Each trajectory is periodic
                    if currCoorID == len(eachDM) - 1:
                        isDirectionForward = False

                    if currCoorID == 0:
                        isDirectionForward = True

                    if isDirectionForward:
                        nextCoorID = currCoorID + 1

                    else:
                        nextCoorID = currCoorID - 1

                # Change the bandwidth of each spectrum at each DSA node at each time epoch
                specBW = [minBW[s] for s in S]
                # print ("Length of spectrum: " + str(S))
                for sBW in specBW:
                    dmP.write(str(sBW) + " ")
                dmP.write("\n")
        dmP.close()


def remove_uneeded_coords(dm_traj):
    new_dm_traj = []
    for mule in dm_traj:
        dmSpeed = random.randint(VMIN, VMAX)
        new_traj = []
        prev_coord = mule[0].strip().split(' ')
        i = 0
        while i < len(mule) - 1:
            new_traj.append(prev_coord[0] + " " + prev_coord[1])
            i += 1
            next_coord = mule[i].strip().split(" ")

            consumed_time = euclideanDistance(prev_coord[0], prev_coord[1], next_coord[0], next_coord[1])/dmSpeed

            while consumed_time < .75:
                i += 1
                if i >= len(mule):
                    break
                prev_coord = mule[i - 1].strip().split(" ")
                next_coord = mule[i].strip().split(" ")
                consumed_time += euclideanDistance(prev_coord[0], prev_coord[1], next_coord[0], next_coord[1]) / dmSpeed

            prev_coord = next_coord

        new_dm_traj.append(new_traj)

    return new_dm_traj


#
# def copy_files():
#     # for run in range(1, 11, 1):
#     for i in range(V):
#         run = lex_data_directory_day.split("/")[2]
#         day = lex_data_directory_day.split("/")[3]
#         # print("Current run is: ", run)
#         src = "../Lexington" + str(max_nodes) + "/" + str(run) + "/" + day  + "/" + str(i) + ".txt"
#         dst = lex_data_directory_day + str(i) + ".txt"
#         copyfile(src, dst)

# Main starts here

#change the directory to the parent one
#We want same source, destination, and bus routes irrespective of number of runs and days

# This function is independent of tau
LINK_EXISTS = numpy.empty(shape=(V + NoOfSources + NoOfDataCenters, V + NoOfSources + NoOfDataCenters, numSpec, int(T/dt)))
LINK_EXISTS.fill(math.inf)

T = T + 30

if not os.path.exists(DataMule_path):
    os.makedirs(DataMule_path)


# Read trajectory for each data mule
DMTrajectories = readTrajectoryFile()
DMTrajectories = remove_uneeded_coords(DMTrajectories)

for i in range(len(DMTrajectories)):
    eachDM = DMTrajectories[i]
    print("Trajectory", i, "length:", len(eachDM))



print("Length of DM trajectories: ", len(DMTrajectories))

if V + NoOfDataCenters + NoOfSources == max_nodes:

    #TODO: Run it only for Day1

    if generate_link_exists == True:
        print("New locations generated\n")
        getBusRoutes(V)
        getSourceDesCoordinates(0, NoOfSources, (NoOfSources + NoOfDataCenters))

    # Randomly place sources and destination nodes (index from 0 to S -1)
    if pkl_folder == 2 and protocol == "XChant":
        if not os.path.exists(DataMule_path + "Day2/"):
            os.makedirs(DataMule_path+ "Day2/")
        for i in range(NoOfSources + NoOfDataCenters):
            os.system("cp " + DataMule_path + "Day1/" + str(i) + ".txt " + DataMule_path + "Day2/")
    else:
        getLocationsOfSourcesAndDataCenters(0, NoOfSources + NoOfDataCenters)


    # Place DMs on selected Routes (index from (S - DM)
    getLocationsOfDMs(DMTrajectories, 0, V)

