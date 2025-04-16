import csv
import datetime

import FunctionSet

def InitGraph(ATFile, ASFile):
    """
    :param ATFile: Armstrong Table in csv format
    :param ASFile: Minded maximal agree sets
    :return: Agree sets dictionary with tuples pair as key
    """
    ATList = []
    with open(ATFile, newline='', encoding="utf8", errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            ATList.append(row)
    print('ATList(col * row):', len(ATList[0]), '*', len(ATList))

    R = []
    for i in range(len(ATList[0])):
        R.append('C' + str(i + 1) + '~')

    file = open(ASFile, 'r')
    AgSList = []
    for line in file:
        AgSList.append(line.rstrip())
    print('AgSList', len(AgSList), [FunctionSet.BitToString(R, a) for a in AgSList])

    ASDict = {}
    for i in range(len(AgSList)):
        ASDict[AgSList[i]] = []
        aSetDict = {}
        for a in range(len(ATList)):
            aSet = []
            for j in range(len(AgSList[i])):
                if AgSList[i][j] == '1':
                    aSet.append(ATList[a][j])
            if tuple(aSet) not in aSetDict.keys():
                aSetDict[tuple(aSet)] = [a]
            else:
                aSetDict[tuple(aSet)].append(a)
        #print('aSetDict', aSetDict)
        for b in aSetDict.keys():
            if len(aSetDict[b]) > 1:
                ASDict[AgSList[i]].append(aSetDict[b])
        #print('ASDict', ASDict) #{'11000': [[0, 1], [2, 3, 4]]}

    AgSDict = {}
    for k in ASDict.keys():
        for h in range(len(ASDict[k])):
            for i in range(len(ASDict[k][h]) - 1):
                for j in range(len(ASDict[k][h]) - i - 1):
                    AgreeOnOther = False
                    for l in range(len(k)):
                        if k[l] == '0':
                            if ATList[ASDict[k][h][i]][l] == ATList[ASDict[k][h][j + i + 1]][l]:
                                AgreeOnOther = True
                                break
                    if AgreeOnOther == False:
                        AgSDict[(ASDict[k][h][i], ASDict[k][h][j + i + 1])] = FunctionSet.BitToString(R, k)

    return {1:AgSList, 2:R, 3: AgSDict}

f = 'iris'
pa1 = "/Users/wye1/Documents/Armstrong/DataSets/naumann_small/"
pa2 = "/Users/wye1/Documents/Armstrong/DataSets/naumann_mined_agree_sets/"
#pa1 = "D:/Wendy/Armstrong/DataSets/naumann_small/"
ATFile = pa1 + f + '.csv'
ASFile = pa2 + f + '.txt'

# Main
if __name__ == "__main__":
    with open("Output.txt", "w") as text_file:
        Start  = datetime.datetime.now()
        print('Dataset:', f)
        result = InitGraph(ATFile, ASFile)
        print('R', result[2])
        print('AgSList(', len(result[1]), ')', result[1])
        print('AgSDict(', len(result[3]), ')') #, result[3])
        End = datetime.datetime.now()

    print("Time of running: ", End - Start)
