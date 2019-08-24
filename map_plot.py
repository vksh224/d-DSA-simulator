from gmplot import gmplot
import os
import numpy
import random
import math

def getPath():
    pathToFolder = "DataMules/Lexington/50/1/Day1"


def findfiles(directory):
    objects = os.listdir(directory)  # find all objects in a dir

    files = []
    for i in objects:  # check if very object in the folder ...
        if isFile(directory + i):  # ... is a file.
            files.append(i)  # if yes, append it.
    return files

def isFile(object):
    try:
        os.listdir(object)  # tries to get the objects inside of this object
        return False  # if it worked, it's a folder
    except Exception:  # if not, it's a file
        return True

def readFile(fileName):
    currPath = []
    with open(fileName) as f:
        listOfLines = f.readlines()[1:]
        count = 0

        for line in listOfLines:
            lineStr = line.strip()
            lineStr = lineStr.split()
            # if count%2 == 0:
            # print(lineStr[3])
            # if(float(lineStr[0]) >= 840) and float(lineStr[0]) <= 1020:
            if (float(lineStr[0]) >= 660) and float(lineStr[0]) <= 840:
            # if (float(lineStr[0]) >= 0):

                currPath.append((float(lineStr[2]), float(lineStr[3])))

                count += 1
            # with open("UMASS/" + busName + ".txt", "a") as fw:
            #     newStr = lineStr[1] + " , " + lineStr[2]
            #     fw.write( newStr + "\n")
            #     count = count + 1
    # fw.close()
    f.close()
    return currPath


allPaths = []
#NOTE: RUN THIS ONE TIME
directory = "DataMules/UMass/2007-11-06/1/"
#generateData(directory)
#
# folders = findfiles(directory)
# folders.sort()
#
# folderLen = len(folders)

#print("All folders: "  + str(folders))

# curr = os.getcwd()


#    if ".DS_Store" not in folders:
#       print("Current Folder " + folders[ind])

#  print("Folder is: " + str(folders[ind]))

currFiles = findfiles(directory)

currFiles.sort()
print(currFiles)
# For all days
allPaths = []
numOfFiles = len(currFiles)

#For each day
for fInd in range(0, numOfFiles):
    filePath = directory + "/" + currFiles[fInd]

    if currFiles[fInd]  not in ["0.txt", "1.txt", "2.txt", "3.txt", "4.txt", "5.txt", "6.txt", "7.txt", "8.txt"]:
    # if currFiles[fInd] in ["16.txt"]:
        currPath = readFile(filePath)
        allPaths.append(currPath)


# import pygmaps
# Place map
gmap = gmplot.GoogleMapPlotter(42.393658, -72.53295, 12)
# gmap = pygmaps.maps(42.340382, -72.496819, 15)

        # 0            1        2           3           4              5          6          7           8           9             10
          #Lime        Gold     Dark Red   Deep Pink  Forest Green   Blue       Black     Chocolate  Magneta  Royal blue  Brown
colors = ['#00FF00', '#FFD700', '#8B0000', '#FF1493', '#228B22', '#0000FF', '#000000', '#A52A2A', '#FF0000', '#00008B', '#4169E1','#00008B', '#4169E1'] #, '#8B008B', '#4169E1','#FF0000' ]
count = 0

if not os.path.exists("HTML"):
    os.makedirs("HTML")
os.chdir("HTML")

for pInd in range(len(allPaths)):
    # gmap = gmplot.GoogleMapPlotter(42.393658, -72.53295, 12)

    # if pInd == 1 or pInd == 4 or pInd == 6 : #or pInd == 6 or pInd > 0
    # print(str(pInd) + " " + str(len(allPaths[pInd])) + " " + str(allPaths[pInd]))
    path_lats, path_lons = zip(* allPaths[pInd])
    colorInd = int(pInd)
    # print ("index: ", colorInd)
    gmap.scatter(path_lats, path_lons, colors[colorInd], size=60, marker=False)

    # Draw
    # gmap.draw(str(pInd) + "_" + "round1.html")
    # os.chdir(curr)

gmap.draw("test.html")