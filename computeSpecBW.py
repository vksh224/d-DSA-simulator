import pickle
import numpy
import math
from STB_help import *
from constants import *

print("Spectrum bandwidth assigned: ", V + NoOfDataCenters + NoOfSources)
specBW = getSpecBW(V + NoOfDataCenters + NoOfSources, S, T)             # Get the dynamic spectrum bandwidth

specBW_file = open(link_exists_folder + "specBW.pkl", 'wb')
pickle.dump(specBW, specBW_file, protocol = 4)
specBW_file.close()

save_4D_in_file(link_exists_folder + "specBW.txt", specBW)
