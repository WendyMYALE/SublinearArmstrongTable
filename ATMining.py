import csv
import datetime

import FunctionSet

def ATMining(ATFile):
    """
    :param ATFile: Armstrong Table in csv format
    :return: Agree sets dictionary with tuples pair as key
    """

    ATList = []
    with open(ATFile, newline='', encoding="utf8", errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            ATList.append(row)
    print('ATList(col * row):', len(ATList[0]), '*', len(ATList))

    n = len(ATList)
    R = []
    Dom = [{} for i in range(len(ATList[0]))]
    for i in range(len(ATList[0])):
        R.append('C' + str(i + 1) + '~')
        Dom[i][ATList[0][i]] = [0]

    #Attributes scanning for domains
    for i in range(n - 1):
        for j in range(len(R)):
            if ATList[i + 1][j] not in Dom[j].keys():
                Dom[j][ATList[i + 1][j]] = [i + 1]
            else:
                Dom[j][ATList[i + 1][j]].append(i + 1)

    AgSDict = dict()
    for a in range(len(R)):
        for v in Dom[a].keys():
            if len(Dom[a][v]) > 2:
                for i in range(len(Dom[a][v]) - 1):
                    for j in range(len(Dom[a][v]) - (i + 1)):
                        nKey = (Dom[a][v][i], Dom[a][v][i + j + 1])
                        if nKey not in AgSDict.keys():
                            AgSDict[nKey] = R[a]
                        else:
                            AgSDict[nKey] += R[a]
            elif len(Dom[a][v]) == 2:
                nKey = (Dom[a][v][0], Dom[a][v][1])
                if nKey not in AgSDict.keys():
                    AgSDict[nKey] = R[a]
                else:
                    AgSDict[nKey] += R[a]

    AgList = []
    for key in AgSDict.keys():
        if AgSDict[key] not in AgList:
            AgList.append(AgSDict[key])

    AgSList = []
    for i in range(len(AgList)):
        AgSList.append(FunctionSet.StringToBit(R, AgList[i]))

    # Bitwise AND to find common attributes, hence generated agree sets
    c1 = 0
    c2 = 0
    c3 = 0
    c4 = 0
    GenSets = {}
    for A in AgSList:
        # Supersets searching for each Agree Set
        for B in [item for item in AgSList if item not in A]:
            if bin(int(A, 2) & int(B, 2)) == bin(int(A, 2)):
                if A not in GenSets.keys():
                    GenSets[A] = []
                    c1 += 1
                GenSets[A].append(B)

        if A in GenSets.keys():
            if len(GenSets[A]) > 1:
                InSect = bin(int(GenSets[A][0], 2))
                for i in range(len(GenSets[A]) - 1):
                    InSect = bin(int(InSect,2) & int(GenSets[A][i + 1], 2))
                if InSect != bin(int(A, 2)):
                    del GenSets[A]
                    c3 += 1
                else:
                    c4 += 1
            else:
                del GenSets[A]
                c2 += 1

    c5 = len(AgSList)
    AgSList = list(set(AgSList) - set(GenSets.keys()))
    F = ''
    for i in range(len(R)):
        F += '1'
    if F in AgSList: AgSList.remove(F)
    AgSList = sorted(AgSList)

    for k in AgSDict.copy().keys():
        if AgSDict[k] not in [FunctionSet.BitToString(R, a) for a in AgSList]:
            del AgSDict[k]

    return {1:AgSList, 2:R, 3: AgSDict}

f = 'iris'
pa = "/Users/wye1/Documents/Armstrong/DataSets/naumann_small/"
#pa = "D:/Wendy/Armstrong/DataSets/naumann_small/"
ATFile = pa + f + '.csv'

# Main
if __name__ == "__main__":
    with open("Output.txt", "w") as text_file:
        Start  = datetime.datetime.now()
        print('Dataset:', f)
        result = ATMining(ATFile)
        print('R', result[2])
        print('AgSList(', len(result[1]), ')', [FunctionSet.BitToString(result[2], a) for a in result[1]])
        print('AgSDict(', len(result[3]), ')', result[3])
        #print(*ATMining(ATFile)[1], sep="\n", file=text_file)
        End = datetime.datetime.now()
        #print("Time of running: {}".format(End - Start), file=text_file)

    print("Time of running: ", End - Start)

#print(*ATMining(ATFile)[1], sep = "\n")
