To start DSA routing simulations

Generate link exists:

    1. in run_simulation set generate_LE = True
    2. Set num_mules to max # of data mules
    3. Set src_dst array to # of srcs and destinations you need
    4. Set speed array to max and min speed values for data mules
    * all other variables do not matter for generating link exists *

Generate Messages:

     1. From GenerateMessages.py scroll down and change generation variables if needed
        - max/min burst
        - max/min wait
     2. Set # of files with those settings you want generated in num_gen variable

Generate Primary Users:

    1. From generate_primary_users.py scroll down and change generation variables if needed
        - max_puser = the largest amount of primary users you would want in a simulation, so better to over estimate then under
        - rounds = # of primary user files you want to generate

Run Simulation:

    1. Make sure generate_LE = False
    2. Change simulation settings as needed:
        - num_mules = # of datamules to run with
        - num_Pusers = # of primary users, cant be > number of primary users generated in file
        - num_channels = # of channels for each spectrum
        - nodes_to_fwd_to = 0 for epidemic or 1 for geographic. This is handled in function run_various_sims if you need
          to run our basic settings of geo [optimistic, pessimistic] and epi [optimistic, pessimistic, TV, LTE, CBRS, ISM]
          the variable is only needed if not using run_various_sims.
        - msg_round = if you have multiple generated msg files for a single msg mean, this will give you a different msg
          file in that mean. (must be generated prior to running)
        - puser_round = same as msg_round but for primary users
        - msg_mean = choose a message mean to run a message file. all message means that are generated can be found in
          the GeneratedMessages directory.
        - ttl = time to live for a generated packet
        - mem_size = max # of packets allowed in a nodes buffer