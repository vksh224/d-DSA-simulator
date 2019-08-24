import pickle
import os

from STB_help import *
from LLC_path import *
# /\from TLEC_path import *
from constants import *

# tau = computeTau()                              # Get the discrete time interval period

#create the folder if it does not exist
if not os.path.exists(path_to_folder):
    os.makedirs(path_to_folder)

# print("Spectrum bandwidth assigned: ")
# specBW = getSpecBW(lex_data_directory, V, S, T)             # Get the dynamic spectrum bandwidth
specBW = pickle.load(open(link_exists_folder + "specBW.pkl", "rb"))

# print("Load LINK Exists: ")

# LINK_EXISTS = createLinkExistenceADJ()   # only for sample graphs
LINK_EXISTS = pickle.load(open(link_exists_folder + "LINK_EXISTS.pkl", "rb"))

# print("Initialization started: ")

ADJ_T, Parent, Spectrum, ADJ_E = computeADJ_T_2(specBW, LINK_EXISTS)

#============== For LLC case =======================

# print("LLC path computation started: ")
LLC_Path, Parent, Spectrum, ELC_Path = LLC_PATH_ADJ_2(ADJ_T, ADJ_E, Parent, Spectrum, V, T, M)

# ADJ_T_file = open(path_to_folder + "ADJ_T.pkl", 'wb')
# pickle.dump(ADJ_T, ADJ_T_file)
# ADJ_T_file.close()
#
# ADJ_E_file = open(path_to_folder + "ADJ_E.pkl", 'wb')
# pickle.dump(ADJ_E, ADJ_E_file)
# ADJ_E_file.close()
#
# save_4D_in_file(path_to_folder + "ADJ_T.txt", LLC_Path)
# save_4D_in_file(path_to_folder + "ADJ_E.txt", ELC_Path)
#
# spec_file = open(path_to_folder + "Spectrum.pkl", 'wb')
# pickle.dump(Spectrum, spec_file)
# spec_file.close()
#
# save_4D_in_file(path_to_folder + "Parent.txt", Parent)
# save_4D_in_file(path_to_folder+ "Spectrum.txt", Spectrum)

# print("LLC paths being calculated: ")
# PRINT_LLC_PATH_FILE(LLC_Path, ELC_Path, Parent, Spectrum)
# PRINT_PATH_FILE_backup(LLC_Path, Parent, Spectrum)

PRINT_LLC_PATH_FILE_3(LLC_Path, ELC_Path, Parent, Spectrum, ADJ_T)

#================ FOR TLEC case ========================

# print("TLEC path computation started: ")
# ADJ_TE, Parent_TE, Spectrum_TE, ADJ_TL = computeADJ_T_TE(specBW, LINK_EXISTS, tau)
# TLEC_Path, Parent_TE, Spectrum_TE, TLLC_Path = TLEC_PATH_ADJ_2(ADJ_TL, ADJ_TE, Parent_TE, Spectrum_TE)
#
# ADJ_TE_file = open(path_to_folder + "ADJ_TE.pkl", 'wb')
# pickle.dump(ADJ_TE, ADJ_TE_file)
# ADJ_TE_file.close()
#
# ADJ_TL_file = open(path_to_folder + "ADJ_TL.pkl", 'wb')
# pickle.dump(ADJ_TL, ADJ_TL_file)
# ADJ_TL_file.close()
#
# save_5D_in_file("ADJ_TE.txt", ADJ_TE)
# save_5D_in_file("ADJ_TL.txt", ADJ_TL)
#
# #TODO: ADJ_TE and TLEC_Path files are identical and so on. So commented the followings
# TLEC_path_file = open(path_to_folder + "TLEC.pkl", 'wb')
# pickle.dump(TLEC_Path, TLEC_path_file)
# TLEC_path_file.close()
#
# TLLC_path_file = open(path_to_folder + "TLLC.pkl", 'wb')
# pickle.dump(TLLC_Path, TLLC_path_file)
# TLLC_path_file.close()
#
# save_5D_in_file("TLEC.txt", TLEC_Path)
# save_5D_in_file("TLLC.txt", TLLC_Path)
#
# save_5D_in_file("Spectrum_TE.txt", Spectrum_TE)
# save_5D_in_file("Parent_TE.txt", Parent_TE)
#
# print("\nTLEC paths are: ")
# PRINT_TLEC_PATH_FILE_3(TLEC_Path, TLLC_Path, Parent_TE, Spectrum_TE)
#
