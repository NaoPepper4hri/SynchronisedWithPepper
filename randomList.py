import random
# You can change this range yourself
#for e.g. "range(11, 21)" will give you equal number of participant for synchrony and asynchrony for numbers 11-20 
generatedList = range(320, 401)
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

    