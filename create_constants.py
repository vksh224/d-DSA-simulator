#Create Constant file for simulation

def create_constants(T, V, S, start_time, dataset, max_nodes, DataMule_dir, path_to_folder, path_to_metrics, link_exists_folder, debug_message,\
                     protocol, NoOfDataCenters, NoOfSources, generate_link_exists, generate_messages, num_messages,\
                     pkl_folder_num, path_to_day1_LLC, perfect_knowledge, speed, limited_time_to_transfer, restrict_band_access, \
                     restrict_channel_access, generate_new_primary_users, num_chan, num_puser, path_to_save_LLC, \
                     smart_setting, priority_queue_active, broadcast, geo_routing, num_nodes_to_fwd, msg_file, puser_file, \
                     debug_m, metric_int, msg_mean, ttl, mem_size, num_replicas, num_trans):

    f = open("constants.py", "w")

    T_line = "T = " + str(T) + "\n"
    V_line = "V = " + str(V) + "\n"
    S_line = "S = " + str(S) + "\n"
    src_line = "NoOfSources = " + str(NoOfSources) + "\n"
    dc_line = "NoOfDataCenters = " + str(NoOfDataCenters) + "\n"
    ds_line = "dataset = " + "\"" +  str(dataset) + "\"" + "\n"
    mn_line = "max_nodes = " + str(max_nodes) + "\n"
    dmd_line = "DataMule_path = \'" + str(DataMule_dir) + "\'\n"
    ptf_line = 'path_to_folder = \'' + str(path_to_folder) + "\'\n"
    st_line = "StartTime = " + str(start_time) + "\n"
    dm_line = "debug_message = " + str(debug_message) + "\n"
    lef_line = "link_exists_folder = \'" + str(link_exists_folder) + "\'\n"
    ptm_line = 'path_to_metrics = \'' + str(path_to_metrics) + "\'\n"

    #ptm_line = "path_to_metrics = '" + path_to_folder + "/msgfile" + str(msg_file) +"_" + str(msg_mean) + "/puserfile" \
               # + str(puser_file) + "/TTL_" + str(ttl) + "/BuffSize_" + str(mem_size) + "/\'\n"

    limited_time_to_transfer_line = "limited_time_to_transfer = " + str(limited_time_to_transfer) + "\n"
    rb_line = "restrict_band_access = " + str(restrict_band_access) + "\n"
    rc_line = "restrict_channel_access = " + str(restrict_channel_access) + "\n"
    pq_line = "priority_queue = " + str(priority_queue_active) + "\n"
    b_line = "broadcast = " + str(broadcast) + "\n"
    geo_line = "geographical_routing = " + str(geo_routing) + "\n"
    gpu_line = "generate_new_primary_users = " + str(generate_new_primary_users) + "\n"
    generated_messages_file = "Generated_Messages/mean" + str(msg_mean) +"/generated_messages" + str(msg_file) + ".txt'\n"
    gen_LE_line = "generate_link_exists = " + str(generate_link_exists) + "\n"
    gen_mes_line = "generate_messages = " + str(generate_messages) + "\n"
    num_mes_line = "num_messages = " + str(num_messages) + "\n"
    pkl_line = "pkl_folder = \'Day" + str(pkl_folder_num) + "_pkl/\'\n"
    chan_line = "num_channels = " + str(num_chan) + "\n"
    puser_line = "num_primary_users = " + str(num_puser) + "\n"
    pts_line = "path_to_save_LLC = \'" + path_to_save_LLC + "\'\n"
    ss_line = "smart_setting = \'" + smart_setting + "\'\n"
    ntf_line = "num_nodes_to_fwd = " + str(num_nodes_to_fwd) + "\n"
    puser_round = "puser_round = " + str(puser_file) + "\n"
    debug_mode = "debug_mode = " + str(debug_m) + "\n"
    oh_file = "overhead_file = 'overhead.txt'\n"
    met_int = "metric_interval = " + str(metric_int) + "\n"
    ttl_line = "TTL = " + str(ttl) + "\n"
    mem_line = "max_packets_in_buffer = " + str(mem_size) + "\n"
    rep_line = "num_replicas = " + str(num_replicas) + "\n"
    trans_line = "num_transceivers = " + str(num_trans) + "\n"
    sec_per_tau_line = "num_sec_per_tau = " + str(60) + "\n"
    if perfect_knowledge == True and protocol == "XChant":
        delivered_file = "delivered_messages_opt.txt"
        consumed_energy_file = "energy_metrics_opt.txt"
        not_delivered_file = "not_delivered_opt.txt"
        metrics_file = "metrics_opt.txt"
        LLC_line = "path_to_LLC = \'" + path_to_folder + "\'\n"
        packet_delivered_file = "packets_delivered_opt.txt"


    else:
        delivered_file = "delivered_messages.txt"
        consumed_energy_file = "energy_metrics.txt"
        not_delivered_file = "not_delivered.txt"
        metrics_file = "metrics.txt"
        packet_delivered_file = "packets_delivered.txt"
        LLC_line = "path_to_LLC = \'" + str(path_to_day1_LLC) + "\'\n"

    # Computed Range = TV : 1452 meter, LTE = 840 meter, ISM = 133 meter, and CBRS = 188 meter
    # Resultant Bit rate = TV: 12 Mbps, LTE = 41 Mbps, ISM = 16 Mbps, and CBRS = 82 Mbps

    # Modified: TV = 12 Mbps, LTE = 20 Mbps, ISM = 10 Mbps, and CBRS = 62 Mbps, corresponding to
    # Channel BW: TV = 6 MHz, LTE = 10 MHz, ISM = 8 MHz, and CBRS = 30 MHz
    # Sensing duration = 0.1 sec, switching energy = 1 mJ, sensing power = 0.4 mW,


    f.write("numSpec = 4\ndt = 1\ntau = 1\n")
    f.write("minBW = [12, 40, 20, 82]\nmaxBW = [12, 40, 20, 82]\nspectRange = [2224, 204, 1286, 288]\nspectPower = [4,1,4,10]\nepsilon = 0.5\n")
    # f.write("minBW = [12, 10, 20, 62]\nmaxBW = [12, 10, 20, 62]\nspectRange = [1330, 200, 770, 125]\nspectPower = [1,1,1,1]\nepsilon = 0.5\n")

    f.write("t_sd = 0.1\nt_td = 1\nidle_channel_prob = 1\nswitching_energy = 0.0001\nsensing_power = 0.00004\nlambda_val = 1\nmessageBurst = [2, 5]\n\n")
    f.write("minTTL=15\nmaxTau = 1\ndefault_num_channels = 10\nM = [120, 1200, 2400, 3600]\npacket_size = 300\nactive_channel_prob = 1\n")

    f.write(T_line)
    f.write(V_line)
    f.write(src_line)
    f.write(dc_line)
    f.write(S_line)
    f.write(mn_line)
    f.write(st_line)
    f.write(dm_line)
    f.write(ds_line)
    f.write(gen_LE_line)
    f.write(gen_mes_line)
    f.write(num_mes_line)
    f.write(dmd_line)
    f.write(ptf_line)
    f.write(ptm_line)
    f.write(pkl_line)
    f.write(LLC_line)
    f.write(rep_line)
    f.write(limited_time_to_transfer_line)
    f.write(rb_line)
    f.write(rc_line)
    f.write(pq_line)
    f.write(b_line)
    f.write(geo_line)
    f.write(ntf_line)
    f.write(gpu_line)
    f.write(chan_line)
    f.write(puser_line)
    f.write(pts_line)
    f.write(puser_round)
    f.write(ttl_line)
    f.write(mem_line)
    f.write(trans_line)
    f.write(sec_per_tau_line)


    f.write(lef_line)
    f.write("delivered_file = \'" + delivered_file + "\'\n")
    f.write("consumed_energy_file = \'" + consumed_energy_file + "\'\n")
    f.write("not_delivered_file = \'" + not_delivered_file + "\'\n")
    f.write("generated_messages_file = \'" + generated_messages_file + "\n")
    f.write("metrics_file = \'" + metrics_file + "\'\n")
    f.write("packet_delivered_file = \'" + packet_delivered_file + "\'\n")
    f.write("protocol = \'" + protocol + "\'\n")
    f.write(ss_line)
    f.write(debug_mode)
    f.write(oh_file)
    f.write(met_int)

    if dataset == "Lexington":
        f.write("\nVMIN = " + str(speed[0]) + "\n")
        f.write("VMAX = " + str(speed[1]) +"\n")
        f.write("wait_time = [2,7]\n")
        f.write("route_start_time1 = 0\nroute_start_time2 = 5\n")
        f.write("lex_data_directory = \'Lexington/\'\n")
        f.write("day_num = " + str(pkl_folder_num) + "\n")

    f.close()
