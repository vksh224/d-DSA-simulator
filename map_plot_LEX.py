import matplotlib.pyplot as plt
import os


startTime = 180
endTime = 180




def isFile(object):
    try:
        os.listdir(object)  # tries to get the objects inside of this object
        return False  # if it worked, it's a folder
    except Exception:  # if not, it's a file
        return True


def findfiles(directory):
    objects = os.listdir(directory)  # find all objects in a dir

    files = []
    for i in objects:  # check if very object in the folder ...
        if isFile(directory + i):  # ... is a file.
            files.append(i)  # if yes, append it.
    return files

def readFile(fileName):
    currPath = []
    with open(fileName) as f:
        listOfLines = f.readlines()[1:]
        count = 0

        for line in listOfLines:
            lineStr = line.strip().split()

            if (float(lineStr[0]) >= startTime and float(lineStr[0]) <= endTime):

                currPath.append([float(lineStr[1]), float(lineStr[2])])

                count += 1
    f.close()
    return currPath

#Get filnames
directory = "DataMules/Lexington/50/3/Day1/"
currFiles = findfiles(directory)
currFiles.sort()

legend = []
# For all days
allPaths = []
numOfFiles = len(currFiles)

#For each day
for fInd in range(0, numOfFiles, 1):
    filePath = directory + "/" + currFiles[fInd]

    # for i in range(0, 100, 10):

    if currFiles[fInd] in ["3.txt", "4.txt", "5.txt"]:
        currPath = readFile(filePath)
        allPaths.append(currPath)


for route in allPaths:
    x = []
    y = []

    for i in range(len(route)):
        x.append(route[i][0])
        y.append(route[i][1])


    plt.scatter(x, y)

# plt.legend(legend)
plt.title(str(len(allPaths)))
plt.savefig("LexRouteTraj.png")
plt.show()

