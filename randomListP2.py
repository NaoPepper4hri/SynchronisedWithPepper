import random
generatedList = range(1, 20)
random.shuffle(generatedList)

asynchList = []
synchList = []
i = 0
for item in generatedList:
    if i:
        asynchList.append(item)
        i = 0
    else:
        synchList.append(item)
        i = 1

blindingFile = open("blindSetup.py", "wb")
blindingFile.write("asynchList = %s\n" % asynchList)
blindingFile.write("synchList = %s\n" % synchList)
blindingFile.close()

    