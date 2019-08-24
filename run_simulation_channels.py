from create_constants import *
from constants import *
from misc_sim_funcs import *
import os

def run_simulation(DataSet, Day_Or_NumMules, Round, Protocol, Band, t, ts, v, generate_LE, Max_Nodes, pkl_fold_num, perfect_knowledge,src_dst,speed, num_mes, num_chan, num_puser, smart_setting, num_fwd, msg_round, puser_round, msg_mean, ttl, max_mem, replicas, priority_queue_active, routing_opt, wei_param, num_trans):

    # a bunch of variables for the constant file
    dir = "DataMules/"              #Starting Directory
    num_messages = num_mes          # not needed anymore
    debug_message = -1              # if a certain msg # needs to be debugged put it here and include if statement in area to debug
    debug_mode = -1                 # same as above but for more general debug purposes
    metric_interval = 30            # interval in which metrics should be generated: every "metric interval" tau
    limited_time_to_transfer = True        # finite resources enabled
    restrict_band_access = True     # for xchants, forget how it works
    restrict_channel_access = True  # is there a limited amount of channels
    # priority_queue_active = True    # do you want to order the msgs in a nodes buffer in some way and send to destination first
    if routing_opt == "Epi":  # if/else statement for epidemic protocol vs forwarding, 0 = broadcast/epidemic
        broadcast = True
        geo_routing = False
        num_replicas_val = "broadcast"

    elif routing_opt == "SnW":
        broadcast = False
        geo_routing = False
        num_replicas_val = "SnW_" + str(replicas)

    else:
        broadcast = False
        geo_routing = True
        num_replicas_val = "geo_" + str(replicas)

    num_nodes_to_fwd = num_fwd      # if forwarding, how many do you want to forward to, 0 = broadcast/epidemic

    #num_replicas_val = "broadcast" if broadcast == True else "geo_" + str(replicas) # create part of dynamic file directory for metrics

    dataset = DataSet                   #UMass or Lexington
    day_or_numMules = Day_Or_NumMules   #date (UMass) or number of mules (Lexington)(for lexington this number really doesn't mean anything it is just needed for the file structure)
    round = Round                       #Round number (also not too important anymore, but can be used to keep information from current simulation settings if you want to regenerate a link exist without losing current metrics)
    if Protocol == "Epidemic_Smart":
        protocol = Protocol + "_" + smart_setting    #Protocol in set of [Optimistic, Pessimistic, TV, LTE, ISM, CBRS]
    else:
        protocol = Protocol                         # not used anymore, didn't take out in case it is needed again for xchants

    if priority_queue_active == True:               # if testing with or without priority queue, another part of dynamic file directory for metrics
        buffer = "PQ"
    else:
        buffer = "FIFO"
    band = Band                    #bands to use in set of [ALL, TV, LTE, ISM, CBRS]
    #generate_link_exists = Gen_LE   # is a new link exist being generated
    T = t                         #Length of Simulation
    V = v                          #Number of dataMules
    NoOfSources = src_dst[0]        # # of sources
    NoOfDataCenters = src_dst[1]    # # of destinations
    start_time = ts                 # start time
    max_nodes = Max_Nodes                  #All nodes include src and des

    # creates multiple file paths based on the dataset and the variables assigned above
    if dataset == "UMass":
        dataMule_path = dir + dataset + "/" + day_or_numMules + "/" + str(round) + "/"
        link_exists_path = dataMule_path + "Link_Exists/" + "LE_" + str(start_time) + "_" + str(T) + "/"
        path_to_metrics = link_exists_path + protocol + "/" + buffer + "/" + num_replicas_val +"/mules_" + str(V) + "/channels_" + str(num_chan) + "/P_users_" + str(num_puser) + "/"
        path_to_save_LLC = link_exists_path + protocol + "/" + buffer + "/mules_" + str(V) + "/"
        if pkl_fold_num == 1:
            path_to_day1_LLC = link_exists_path + protocol + "/" + buffer + "/mules_" + str(V) + "/"
        else:
            path_to_day1_LLC = dataMule_path + "Link_Exists/LE_" + str(start_time - T) + "_" + str(T) + "/" + protocol + "/" + buffer + "/mules_" + str(V) + "/"

    elif dataset == "Lexington":
        dataMule_path = dir + dataset + "/" + day_or_numMules + "/" + str(round) + "/"
        if pkl_fold_num == 1:
            link_exists_path = dataMule_path + "Link_Exists/" + "LE_1_"  + str(T) + "/"
            path_to_day1_LLC = link_exists_path
            path_to_folder = link_exists_path + protocol + "/" + buffer + "/" + num_replicas_val + "/mules_" + str(
                V) + "/channels_" + str(num_chan) + "/P_users_" + str(num_puser)
            path_to_metrics = path_to_folder + "/msgfile_" + str(msg_round) + "_" + str(msg_mean) + "/puserfile_" \
                           + str(puser_round) + "/TTL_" + str(ttl) + "/BuffSize_" + str(mem_size) +"/"

        else:
            link_exists_path = dataMule_path + "Link_Exists/" + "LE_2_" + str(T) + "/"
            path_to_folder = link_exists_path + protocol + "/" + buffer + "/" + num_replicas_val + "/mules_" + str(
                V) + "/channels_" + str(num_chan) + "/P_users_" + str(num_puser)
            path_to_metrics = path_to_folder + "/msgfile_" + str(msg_round) + "_" + str(msg_mean) + "/puserfile_" \
                              + str(puser_round) + "/TTL_" + str(ttl) + "/BuffSize_" + str(mem_size) + "/"
            path_to_day1_LLC = dataMule_path + "Link_Exists/LE_2_" + str(
                T) + "/" + protocol + "/" + buffer + "/mules_" + str(V) + "/"

        path_to_save_LLC = link_exists_path

    else:
        print("Invalid Dataset")
        return -1

    # creates a list of spectrums based on bands being used and the current smart setting
    if band == "ALL":
        w1 = wei_param
        w2 = 1 - w1
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
            os.system("python3 create_pickles.py")
            os.system("python3 computeLINKEXISTS_UMass.py")

        elif dataset == "Lexington":
            os.system("python3 readLexingtonData_Fixed.py")
            os.system("python3 create_pickles_Lex.py")
            os.system("python3 computeLINKEXISTS_Lex.py")
            os.system("python3 computeSpecBW.py")

    # run the simulation and metrics if you are not generating link exists
    if generate_LE == False:
        os.system("python3 main.py")
        os.system("python3 metrics.py")


# function to run simulations for ISC2 paper
def run_various_sims_geo(sim_round, num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl, mem_size,
                         num_replicas, puser_round, wei_param, num_transceivers):
    for band in bands:
        print("Geo: Msg round", msg_round, "PU round", puser_round, " No. Replica", num_replicas, "Channels", num_channels)

        if band == "ALL":
            priority_queue_active = False
            for routing_opt in ["Geo"]:
                print("Routing:", routing_opt, "W", wei_param)

                # print("Weighted")
                run_simulation(data, day, sim_round, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                               pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                               "weighted" + "_" + str(wei_param), nodes_tofwd, msg_round, puser_round, msg_mean, ttl,
                               mem_size, num_replicas, priority_queue_active, routing_opt, wei_param, num_transceivers)
        else:
            priority_queue_active = False
            # For single bands, lets only do basic epidemic routing - 0 stands for epidemic routing
            for routing_opt in ["Geo"]:
                print("Band:", band, "Routing:", routing_opt)
                run_simulation(data, day, sim_round, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                               pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                               band, nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size, num_replicas,
                               priority_queue_active, routing_opt, wei_param, num_transceivers)


def run_various_sims_snw(sim_round, num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl, mem_size,
                         num_replicas, puser_round, wei_param, num_transceivers):
    for band in ["ALL"]:
        print("Geo: Msg round", msg_round, "PU round", puser_round, " No. Replica", num_replicas, "Channels", num_channels)

        if band == "ALL":
            priority_queue_active = False
            for routing_opt in ["SnW"]:
                print("Routing:", routing_opt, "W", wei_param)

                # print("Weighted")
                run_simulation(data, day, sim_round, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                               pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                               "weighted" + "_" + str(wei_param), nodes_tofwd, msg_round, puser_round, msg_mean, ttl,
                               mem_size, num_replicas, priority_queue_active, routing_opt, wei_param, num_transceivers)
        else:
            priority_queue_active = False
            # For single bands, lets only do basic epidemic routing - 0 stands for epidemic routing
            for routing_opt in ["SnW"]:
                print("Band:", band, "Routing:", routing_opt)
                run_simulation(data, day, sim_round, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                               pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                               band, nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size, num_replicas,
                               priority_queue_active, routing_opt, wei_param, num_transceivers)


# function to run simulations for ISC2 paper
def run_various_sims(sim_round, num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl, mem_size, num_replicas, puser_round, wei_param, num_transceivers):
    for band in ["ALL"]:
        print(band, "Msg round", msg_round, "PU round", puser_round, "Channels", num_channels)

        #For all bands, do smart epidemic and Geographic routing (1 stands for geo, and 0 for epidemic)
        if band == "ALL":
            priority_queue_active = False
            for routing_opt in ["Epi"]:
                print("Routing:", routing_opt, "W", wei_param)

                #print("Weighted")
                run_simulation(data, day, sim_round, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                               pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                               "weighted" + "_" + str(wei_param), nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size,
                               num_replicas, priority_queue_active, routing_opt, wei_param, num_transceivers)

        else:
                priority_queue_active = False
                #For single bands, lets only do basic epidemic routing - 0 stands for epidemic routing
                for routing_opt in ["Epi"]:
                    print("Band:", band, "Routing:", routing_opt)
                    run_simulation(data, day, sim_round, proto, band, len_T, start_time, num_mules, generate_LE, max_v,
                                   pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                                   band, nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size, num_replicas,
                                   priority_queue_active, routing_opt, wei_param, num_transceivers)


# (DataSet, Day_Or_NumMules, Round, Protocol, Band, t, ts, v, Gen_LE, Max_Nodes, pkl_fold_num, perfect_knowledge,
#  src_dst_arr, speed_arr, num messages, num channels, num primary users, smart setting (optional))

# RF parameter setting
# Freq: TV = 600 MHz, LTE = 900 MHz, ISM = 2.4 GHz, and CBRS = 3.5 GHz
# Path loss factor = 2.8 (sub-urban)
# Receiver Sensitivity = -95 dBm
# White noise = -100 dB
# SNR = 5 dB
# Transmitter Antenna Gain = 0 dBi
# Receiver Antenna Gain = 0 dBi
# Transmit power = TV, and LTE = 4 Watt, ISM = 1 Watt, CBRS = 100 Watt
# Channel Bandwidth = Tv = 6 MHz, LTE = 20 MHz, ISM = 8 MHz, and CBRS = 40 MHz

# Computed Range = TV : 1452 meter, LTE = 840 meter, ISM = 133 meter, and CBRS = 188 meter
# Resultant Bit rate = TV: 12 Mbps, LTE = 41 Mbps, ISM = 16 Mbps, and CBRS = 82 Mbps

data = "Lexington"
day = "50"
len_T = 360                     #length of simulation
start_time = 0                #start time (to find Link Exists)
bands = ["ALL", "LTE", "TV", "CBRS", "ISM"]  #which bands to use
num_mules = 128                  #number of data mules to use
generate_LE = False             #generate Link Exists
pkl_ID = 1                      #pkl folder ID if Link Exists is being generated
perfect_knowledge = False       #Xchant only
src_dst = [3, 3]                #num src and dst
max_v = num_mules + src_dst[0] + src_dst[1]                     #max number of datamules + src + dst
speed = [135, 400]                  #Lex data only
proto = "Epidemic_Smart"        #[Epidemic_Smart, XChant, SprayNWait (in progress)]
num_Pusers = 200
num_channels = 6
nodes_tofwd = 1
routing_opt = "SnW"
msg_round = 0
puser_round = 0
msg_mean = 15
ttl = 180
mem_size = 100
num_replicas = 5       # number of replicas/copies for geographic SnW
sim_round = 6
priority_queue_active = False
compute_spec_BW = False
num_transceivers = 1

if compute_spec_BW == True:
    os.system("python3 computeSpecBW.py")


else:
    if generate_LE == False :

        for msg_round in range(0, 5):
            for puser_round in range(0, 5):

                # for mem_size in [100, 25, 50, 200, -1]:
                #     print("Msg round", msg_round, "Memory", mem_size)
                #     for wei_param in [0.5]:
                #         # For Epidemic Routing
                #         run_various_sims(sim_round, num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl,
                #                          mem_size, num_replicas, puser_round, wei_param, num_transceivers)
                #         # For Geo and Spray and Wait
                #         for num_replicas in [5]:  # 1, 5
                #             run_various_sims_geo(sim_round, num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl,
                #                                  mem_size, num_replicas, puser_round, wei_param, num_transceivers)

                # for num_mules in [92, 8, 16, 32, 64, 128]:
                #      for wei_param in [0.2]:
                        
                #          # For Geo and Spray and Wait
                #         for num_replicas in [5]: #1, 5
                #             run_various_sims_geo(sim_round, num_mules, num_channels, num_Pusers, msg_round,
                #                                      msg_mean, ttl, mem_size, num_replicas, puser_round, wei_param, num_transceivers)
                #         # For Epidemic Routing
                #         run_various_sims(sim_round, num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl,
                #                          mem_size, num_replicas, puser_round, wei_param, num_transceivers)

                #         for num_replicas in [20]: #1, 5
                #             run_various_sims_snw(sim_round, num_mules, num_channels, num_Pusers, msg_round,
                #                                      msg_mean, ttl, mem_size, num_replicas, puser_round, wei_param, num_transceivers)


                # for msg_mean in [15, 7, 25, 35, 45]:
                #     for wei_param in [0.5]:
                #         # For Epidemic Routing
                #         run_various_sims(sim_round, num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl,
                #                          mem_size, num_replicas, puser_round, wei_param, num_transceivers)
                #         # For Geo and Spray and Wait
                #         for num_replicas in [5]: #1, 5
                #             run_various_sims_geo(sim_round, num_mules, num_channels, num_Pusers, msg_round,
                #                                     msg_mean, ttl, mem_size, num_replicas, puser_round, wei_param, num_transceivers)

                # for ttl in [180, 30, 60, 90, 240, 360]:
                #     for wei_param in [0.5]:
                #         # For Epidemic Routing
                #         run_various_sims(sim_round, num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl,
                #                          mem_size, num_replicas, puser_round, wei_param, num_transceivers)
                #         # For Geo and Spray and Wait
                #         for num_replicas in [5]: #1, 5
                #             run_various_sims_geo(sim_round, num_mules, num_channels, num_Pusers, msg_round, msg_mean,
                #                                  ttl, mem_size, num_replicas, puser_round, wei_param, num_transceivers)

                num_mules = 92
                for num_channels in [6, 2, 4, 8, 10]:
                    for wei_param in [0.5]:
                        
                         # For Geo and Spray and Wait
                        for num_replicas in [1, 5]: #1, 5
                            run_various_sims_geo(sim_round, num_mules, num_channels, num_Pusers, msg_round,
                                                     msg_mean, ttl, mem_size, num_replicas, puser_round, wei_param, num_transceivers)
                        # For Epidemic Routing
                        run_various_sims(sim_round, num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl,
                                         mem_size, num_replicas, puser_round, wei_param, num_transceivers)

                        for num_replicas in [20]: #1, 5
                            run_various_sims_snw(sim_round, num_mules, num_channels, num_Pusers, msg_round,
                                                     msg_mean, ttl, mem_size, num_replicas, puser_round, wei_param, num_transceivers)

                # for num_Pusers in [50, 100, 200, 300, 400, 500]:
                #     for wei_param in [0.5]:
                #         # For Epidemic Routing
                #         run_various_sims(sim_round, num_mules, num_channels, num_Pusers, msg_round, msg_mean, ttl,
                #                          mem_size, num_replicas, puser_round, wei_param, num_transceivers)
                #         # For Geo and Spray and Wait
                #         for num_replicas in [5]: #1, 5
                #             run_various_sims_geo(sim_round, num_mules, num_channels, num_Pusers, msg_round, msg_mean,
                #                                  ttl, mem_size, num_replicas, puser_round, wei_param, num_transceivers)

    #Generate Link exists
    else:
        run_simulation(data, day, sim_round, proto, "ALL", len_T, start_time, num_mules, generate_LE, max_v,
                       pkl_ID, perfect_knowledge, src_dst, speed, num_messages, num_channels, num_Pusers,
                       "weighted", nodes_tofwd, msg_round, puser_round, msg_mean, ttl, mem_size, num_replicas,
                       priority_queue_active, routing_opt, 0, num_transceivers)