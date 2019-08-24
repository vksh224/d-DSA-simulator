from misc_sim_funcs import *
from network import *
from constants import  *


initialize_output_files()

#create/init network
net = Network()
net.fill_network(V + NoOfSources + NoOfDataCenters)
net.load_primary_users()

#Open LLC_path.txt, LLC_spectrum.txt, generated_messages, specBW, LINK_EXISTS
path_lines, spec_lines, msg_lines, specBW, LINK_EXISTS = get_data_structs()

#loop thru each tau
for t in range(0, T, tau):
    # print("TIME:", t)
    # net.network_status()
    # does all routing and sending of packets in the tau = t
    net.network_GO(t, specBW, path_lines, spec_lines, msg_lines, LINK_EXISTS)

#creates not_delivered.txt for overhead computation
net.not_delivered_messages()
# Handle messages that got delivered
net.messages_delivered()
# saves packets per tau and parallel communications
net.save_packets_per_tau()
# net.print_bandusage()



