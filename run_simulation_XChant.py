from create_constants import *
from constants import *
from misc_sim_funcs import *
import os

def run_simulation(DataSet, Day_Or_NumMules, Round, Protocol, Band, t, ts, v, generate_LE, Max_Nodes, pkl_fold_num, perfect_knowledge,src_dst,speed, num_mes, num_chan, num_puser, smart_setting, num_fwd, msg_round, puser_round, msg_mean, ttl, max_mem, replicas, priority_queue_active, routing_opt, wei_param, num_trans, is_boot_round):

    # a bunch of variables for the constant file
    dir = "DataMules/"              #Starting Directory
    num_messages = num_mes          # not needed anymore
    debug_message = -1              # if a certain msg # needs to be debugged put it here and include if statement in area to debug
    debug_mode = -1                 # same as above but for more general debug purposes
    metric_interval = 30            # interval in which metrics should be generated: every "metric interval" tau
    limited_time_to_transfer = True        # finite resources enabled
    restrict_band_access = False     # for xchants, forget how it works
    restrict_channel_access = True  # is there a limited amount of channels
    dataset = DataSet                   #UMass or Lexington
    day_or_numMules = Day_Or_NumMules   #date (UMass) or number of mules (Lexington)(for lexington this number really doesn't mean anything it is just needed for the file structure)
    round = Round                       #Round number (also not too important anymore, but can be used to keep information from current simulation settings if you want to regenerate a link exist without losing current metrics)
    protocol = Protocol                         # not used anymore, didn't take out in case it is needed again for xchants
    band = Band                    #bands to use in set of [ALL, TV, LTE, ISM, CBRS]
    T = t                         #Length of Simulation
    V = v                          #Number of dataMules
    NoOfSources = src_dst[0]        # # of sources
    NoOfDataCenters = src_dst[1]    # # of destinations
    start_time = ts                 # start time
    max_nodes = Max_Nodes                  #All nodes include src and des
    geo_routing = False
    broadcast = False
    num_nodes_to_fwd = -1

    #dataset is the "LEX" or "UMass", day_or_numMules is the "2007-11-01", and round is the simulation round.
    dataMule_path = dir + dataset + "/" + str(day_or_numMules) + "/" + str(round) + "/"

    # creates multiple file paths based on the dataset and the variables assigned above
    if dataset == "UMass":
        link_exists_path = dataMule_path + "Link_Exists/" + "LE_" + str(start_time) + "_" + str(T) + "/"
        path_to_folder = link_exists_path + protocol + "/mules_" + str(V) + "/channels_" + str(num_chan) + "/P_users_" + str(num_puser)

        path_to_metrics = path_to_folder + "/msgfile_" + str(msg_round) + "_" + str(msg_mean) + "/puserfile_" \
                           + str(puser_round) + "/TTL_" + str(ttl) + "/BuffSize_" + str(mem_size) +"/" + "numTransceivers_"\
                            + str(num_trans) + "/"
        path_to_save_LLC = link_exists_path

        if pkl_fold_num == 1:
            path_to_day1_LLC = link_exists_path

        else:
            boot_round_length = 180
            path_to_day1_LLC = dataMule_path + "Link_Exists/LE_" + str(start_time - boot_round_length) + "_" + str(boot_round_length) + "/"

    elif dataset == "Lexington":
        if pkl_fold_num == 1:
            link_exists_path = dataMule_path + "Link_Exists/" + "LE_1_"  + str(T) + "/"
            path_to_day1_LLC = link_exists_path
            path_to_folder = link_exists_path + protocol + "/mules_" + str(V) + "/channels_" + str(num_chan) + "/P_users_" + str(num_puser)
            path_to_metrics = path_to_folder + "/msgfile_" + str(msg_round) + "_" + str(msg_mean) + "/puserfile_" \
                           + str(puser_round) + "/TTL_" + str(ttl) + "/BuffSize_" + str(mem_size) +"/" + "numTransceivers_"\
                            + str(num_trans) + "/"

        else:
            link_exists_path = dataMule_path + "Link_Exists/" + "LE_2_" + str(T) + "/"
            path_to_folder = link_exists_path + protocol + "/mules_" + str(V) + "/channels_" + str(num_chan) + "/P_users_" + str(num_puser)
            path_to_metrics = path_to_folder + "/msgfile_" + str(msg_round) + "_" + str(msg_mean) + "/puserfile_" \
                              + str(puser_round) + "/TTL_" + str(ttl) + "/BuffSize_" + str(mem_size) + "/" + "numTransceivers_"\
                            + str(num_trans) + "/"

            path_to_day1_LLC = dataMule_path + "Link_Exists/LE_1_" + str(T) + "/"

        path_to_save_LLC = link_exists_path


    else:
        print("Invalid Dataset")
        return -1

    # creates a list of spectrums based on bands being used and the current smart setting
    if protocol == "XChant":
        S = [0, 1, 2, 3]
    elif band == "ALL":
        w1 = wei_param
        w2 = 1 - wei_param
        S = get_suitable_spectrum_list(smart_setting, w1, w2)
    elif band == "TV":
        S = [0, 0, 0, 0]
    elif band == "ISM":
        S = [1, 1, 1, 1]
    elif band == "LTE":
        S = [2, 2, 2, 2]
    elif band == "CBRS":
        S = [3, 3, 3, 3]
    else:
        S = []
        print("Invalid Band Type")

    # create the constants file based on all of these parameters
    create_constants(T, V, S, start_time, dataset, max_nodes, dataMule_path, path_to_folder, path_to_metrics, link_exists_path,
                     debug_message, protocol, NoOfDataCenters, NoOfSources, generate_LE, generate_messages, num_messages,
                     pkl_fold_num, path_to_day1_LLC, perfect_knowledge, speed, limited_time_to_transfer, restrict_band_access,
                     restrict_channel_access, generate_new_primary_users, num_chan, num_puser, path_to_save_LLC, smart_setting,
                     priority_queue_active, broadcast, geo_routing, num_nodes_to_fwd, msg_round, puser_round, debug_mode, metric_interval,
                     msg_mean, ttl, max_mem, replicas, num_trans)

    # generate a link exists if needed
    if generate_LE == True and max_nodes == V + NoOfSources + NoOfDataCenters:

        if dataset == "UMass":
            # os.system("python3 create_pickles.py")
            os.system("python3 computeLINKEXISTS_UMass.py")
            os.system("python3 STB_main_path.py")
            if is_boot_round == True:
                os.system("python3 GenerateMessagesFromLLC.py")


        elif dataset == "Lexington":
            os.system("python3 readLexingtonData_Fixed.py")
            os.system("python3 create_pickles_Lex.py")
            os.system("python3 computeLINKEXISTS_Lex.py")
            os.system("python3 computeSpecBW.py")
            os.system("python3 STB_main_path.py")


    # run the simulation and metrics if you are not generating link exists
    if generate_LE == False:
        if dataset == "UMass" and is_boot_round == False:
            print("Compute round 2 link exists\n")
            os.system("python3 computeLINKEXISTS_UMass.py")
            os.system("python3 STB_main_path.py")

        os.system("python3 main.py")
        os.system("python3 metrics.py")


# function to run simulations for ISC2 paper
def run_various_sims(sim_round, num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl, mem_size, num_replicas):
    for band in bands:
        # print("Band:", band, "MSG round:", msg_round, "MSG mean:", msg_mean)

        #For all bands, do smart epidemic and Geographic routing (1 stands for geo, and 0 for epidemic)
        if band == "ALL":
            priority_queue_active = True
            for routing_opt in ["Geo"]:
                print("Routing:", routing_opt)

                #print("Weighted")
                run_simulation(data, day, sim_round, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                               pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                               "weighted", nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size,
                               num_replicas, priority_queue_active, routing_opt)
                # print()
                # print("Optimistic")
                run_simulation(data, day, sim_round, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                               pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                               "optimistic", nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size, num_replicas, priority_queue_active, routing_opt)
                # print()
                # print("Pessimistic")
                run_simulation(data, day, sim_round, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                            pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                            "pessimistic", nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size, num_replicas, priority_queue_active, routing_opt)


        else:
                priority_queue_active = False
                #For single bands, lets only do basic epidemic routing - 0 stands for epidemic routing
                for routing_opt in ["Epi"]:
                    print("Band:", band, "Routing:", routing_opt)
                    run_simulation(data, day, sim_round, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                                   pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                                   band, nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size, num_replicas, priority_queue_active, routing_opt)


# (DataSet, Day_Or_NumMules, Round, Protocol, Band, t, ts, v, Gen_LE, Max_Nodes, pkl_fold_num, perfect_knowledge,
#  src_dst_arr, speed_arr, num messages, num channels, num primary users, smart setting (optional))


# RF parameter setting
# Freq: TV = 600 MHz, LTE = 900 MHz, ISM = 2.4 GHz, and CBRS = 3.5 GHz
# Path loss factor = 2.8 (sub-urban, LEXINGTON) and 2.5 (rural UMass)
# Receiver Sensitivity = -95 dBm
# White noise = -100 dB
# SNR = 5 dB
# Transmitter Antenna Gain = 0 dBi
# Receiver Antenna Gain = 0 dBi
# Transmit power = TV, and LTE = 4 Watt, ISM = 1 Watt, CBRS = 100 Watt
# Channel Bandwidth = Tv = 6 MHz, LTE = 20 MHz, ISM = 8 MHz, and CBRS = 40 MHz

# Computed Range = TV : 1452 meter, LTE = 840 meter, ISM = 133 meter, and CBRS = 188 meter
# Resultant Bit rate = TV: 12 Mbps, LTE = 41 Mbps, ISM = 16 Mbps, and CBRS = 82 Mbps

#### For Day 2
#1. start_time = 840,
#2. pkl_ID = 2
#3. is_boot_round = False
#4. len_T = 240

start_time = 660                #start time (to find Link Exists)
is_boot_round = False           #which day or round
pkl_ID = 1                      #pkl folder ID if Link Exists is being generated
len_T = 240
generate_LE = False             #generate Link Exists

data = "UMass"
day = "2007-11-01"
                   #length of simulation
bands = ["ALL", "LTE", "TV", "CBRS", "ISM"]  #which bands to use
num_mules = 10                  #number of data mules to use
perfect_knowledge = False       #Xchant only
src_dst = [5, 4]                #num src and dst
max_v = num_mules + src_dst[0] + src_dst[1]                     #max number of datamules + src + dst
speed = [135, 400]                  #Lex data only
proto = "XChant"        #[Epidemic_Smart, XChant, SprayNWait (in progress)]
num_Pusers = 0
num_channels = 10
nodes_tofwd = -1
routing_opt = "Epi"
msg_round = 1
puser_round = 0
msg_mean = 7
ttl = 90
mem_size = -1
num_replicas = 1       # number of replicas/copies for geographic SnW
sim_round = 1
priority_queue_active = False
compute_spec_BW = False
num_transceivers = 1


if compute_spec_BW == True:
    os.system("python3 computeSpecBW.py")

else:
    if generate_LE == False :

        for num_transceivers in [1, 8]:
            print("Num Transceivers:", num_transceivers)
            run_simulation(data, day, sim_round, proto, "ALL", len_T, start_time, num_mules, generate_LE, max_v,
                           pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                           "optimistic", nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size, num_replicas,
                           priority_queue_active, routing_opt,0, num_transceivers, is_boot_round)

    #Generate Link exists
    else:
        if data == "Lexington":
            run_simulation(data, day, sim_round, proto, "ALL", len_T, start_time, num_mules, generate_LE, max_v,
                                           1, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                                       "optimistic", nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size, num_replicas, priority_queue_active, routing_opt, 0, num_transceivers)
            run_simulation(data, day, sim_round, proto, "ALL", len_T, start_time, num_mules, generate_LE, max_v,
                           2, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                           "optimistic", nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size, num_replicas,
                           priority_queue_active, routing_opt, 0, num_transceivers, is_boot_round)
        else:
            run_simulation(data, day, sim_round, proto, "ALL", len_T, start_time, num_mules, generate_LE, max_v,
                           pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                           "optimistic", nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size, num_replicas,
                           priority_queue_active, routing_opt, 0, num_transceivers, is_boot_round)
