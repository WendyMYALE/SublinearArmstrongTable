import csv
import datetime

import FunctionSet
import Function4Null

def powerset(l, s):
    x = len(l)
    ps = []
    for i in range(1 << x):
        ps.append([l[j] for j in range(x) if (i & (1 << j))])

    return [item for item in ps if len(item) >= s]

def InitGraph(ATFile, StrongAS, WeakAS, W):
    """
    :param ATFile: Armstrong Table in csv format
    :param StrongAS: Minded strong maximal agree sets
    :param WeakAS: Minded weak maximal agree sets
    :param W: Null set
    :return: Agree sets dictionary with tuples pair as key
    """
    ToDebug = 0   # Flag to print for debugging

    ATList = []
    with open(ATFile, newline='', encoding="utf8", errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            ATList.append(row)
    print('ATList(col * row):', len(ATList[0]), '*', len(ATList))

    R = []
    for i in range(len(ATList[0])):
        R.append('C' + str(i + 1) + '~')

    commonAS = [item for item in StrongAS if item in WeakAS]
    if len(commonAS) > 0:
        WeakAS = [item for item in WeakAS if item not in commonAS]
        print(commonAS, "are removed from Weak agree sets as they exist in Strong agree set")

    if len(WeakAS) < 1:
        print("No weak agree set left.")
        return {1: -1}
    else:
        ASList = [FunctionSet.StringToBit(R, a) for a in StrongAS]
        AWList = [FunctionSet.StringToBit(R, b) for b in WeakAS]

        sASDict = {}
        newC = 0
        for i in range(len(ASList)):
            sASDict[ASList[i]] = []
            aSetDict = {}
            for a in range(len(ATList)):
                aSet = []
                NullDeteced = False
                for j in range(len(ASList[i])):
                    if ASList[i][j] == '1':
                        if ATList[a][j] != 'NULL':
                            aSet.append(ATList[a][j])
                        else:
                            NullDeteced = True
                            break
                if not NullDeteced:
                    if tuple(aSet) not in aSetDict.keys():
                        aSetDict[tuple(aSet)] = [a]
                    else:
                        aSetDict[tuple(aSet)].append(a)
            #print('Debugging: aSetDict', aSetDict)
            for b in aSetDict.keys():
                if len(aSetDict[b]) > 1:
                    sASDict[ASList[i]].append(aSetDict[b])
            #print('Debugging: sASDict', len(sASDict), sASDict) #{'11000': [[0, 1], [2, 3, 4]]}
            if len(sASDict[ASList[i]]) == 0:
                cols = [idx for idx, value in enumerate(ASList[i]) if value == '1']
                print("??", ASList[i], ASList[i].count('1'), cols, ) #len(powerset(cols, 3)))
                #newC += len(powerset(cols, 3))
        #print("??", newC)

        wASDict = {}
        for i in range(len(AWList)):
            wASDict[AWList[i]] = []
            bSetDict = {}
            for a in range(len(ATList)):
                bSet = []
                for j in range(len(AWList[i])):
                    if AWList[i][j] == '1':
                        if W[j] == 0:
                            bSet.append(ATList[a][j])
                        else:
                            bSet.append('NULL')
                if tuple(bSet) not in bSetDict.keys():
                    bSetDict[tuple(bSet)] = [a]
                else:
                    bSetDict[tuple(bSet)].append(a)
            if ToDebug: print('Debugging: bSetDict', bSetDict)
            for b in bSetDict.keys():
                if len(bSetDict[b]) > 1:
                    wASDict[AWList[i]].append(bSetDict[b])
            if ToDebug: print('Debugging: wASDict', wASDict) #{'11000': [[0, 1], [2, 3, 4]]}

        AgSDict = {}
        for k in sASDict.keys():
            for h in range(len(sASDict[k])):
                for i in range(len(sASDict[k][h]) - 1):
                    for j in range(len(sASDict[k][h]) - i - 1):
                        AgreeOnOther = False
                        NullDetected = False
                        for l in range(len(k)):
                            if k[l] == '0':
                                if ATList[sASDict[k][h][i]][l] == ATList[sASDict[k][h][j + i + 1]][l] != 'NULL':
                                    AgreeOnOther = True
                                    break
                            elif ATList[sASDict[k][h][i]][l] == 'NULL' or ATList[sASDict[k][h][j + i + 1]][l] == 'NULL':
                                NullDetected = True
                                break
                        if not AgreeOnOther and not NullDetected:
                            AgSDict[(sASDict[k][h][i], sASDict[k][h][j + i + 1])] = [FunctionSet.BitToString(R, k), '']
        print("??", sum(len(x) == 0 for x in sASDict.values()))

        for k in wASDict.keys():
            for h in range(len(wASDict[k])):
                for i in range(len(wASDict[k][h]) - 1):
                    for j in range(len(wASDict[k][h]) - i - 1):
                        AgreeOnOther = False
                        WeaklyAgree = False
                        for l in range(len(k)):
                            if k[l] == '0':
                                if ATList[wASDict[k][h][i]][l] == 'NULL' or ATList[wASDict[k][h][j + i + 1]][l] == 'NULL' or ATList[wASDict[k][h][i]][l] == ATList[wASDict[k][h][j + i + 1]][l]:
                                    AgreeOnOther = True
                                    break
                            elif W[l] == 1:
                                if ATList[wASDict[k][h][i]][l] == 'NULL' or ATList[wASDict[k][h][j + i + 1]][l] == 'NULL' or ATList[wASDict[k][h][i]][l] == ATList[wASDict[k][h][j + i + 1]][l]:
                                    WeaklyAgree = True
                        if WeaklyAgree and not AgreeOnOther:
                            if (wASDict[k][h][i], wASDict[k][h][j + i + 1]) not in AgSDict.keys():
                                AgSDict[(wASDict[k][h][i], wASDict[k][h][j + i + 1])] = ['', FunctionSet.BitToString(R, k)]
                            else:
                                AgSDict[(wASDict[k][h][i], wASDict[k][h][j + i + 1])][1] = FunctionSet.BitToString(R, k)
        print("??", sum(len(x) == 0 for x in wASDict.values()))

        V = {}
        for k in AgSDict.keys():
            if k[0] not in V.keys(): V[k[0]] = [1 if i == 'NULL' else 0 for i in ATList[k[0]]]
            if k[1] not in V.keys(): V[k[1]] = [1 if i == 'NULL' else 0 for i in ATList[k[1]]]
            #if len(AgSDict[k][0]) > 0 and len(AgSDict[k][1]) > 0: print('Debugging: AS + AW', k, AgSDict[k])
        if ToDebug: print("Initial Graph has", len(V), "vertexes.")

        return {1: R, 2: ASList, 3: AWList, 4: AgSDict, 5: V}

source = 'Hockey.Scoring'
path1 = "/Users/wye1/Documents/Armstrong/DataSets/Hockey/"
path2 = "/Users/wye1/Documents/Armstrong/DataSets/Hocky_Parameters/"
path_out = "/Users/wye1/Documents/Armstrong/InformativeWithNull/WorkFolder/"
#pa1 = "D:/Wendy/Armstrong/DataSets/naumann_small/"
ATFile = path1 + source + '.csv'

# Main
if __name__ == "__main__":
    ToDebug = 1   # Flag to print for debugging

    FileName = path2 + source + '.main'
    para = Function4Null.FindParameters(FileName)
    R = para[1]
    StrongAS = para[2]
    WeakAS = para[3]
    W = para[6]

    commonAS = [item for item in StrongAS if item in WeakAS]
    if len(commonAS) > 0:
        WeakAS = [item for item in WeakAS if item not in commonAS]
        print(commonAS, "are removed from Weak agree sets as they exist in Strong agree set")

    if ToDebug:
        print('R', R)
        print('StrongAS', len(StrongAS), StrongAS)
        print('WeakAS', len(WeakAS), WeakAS)
        print('W', W)

    with open(path_out + source + "_Output.txt", "w") as text_file:
        Start  = datetime.datetime.now()
        print('Dataset:', source, file=text_file)
        print(sep="\n")
        result = InitGraph(ATFile, StrongAS, WeakAS, W)
        print('R', result[1], file=text_file)
        print(sep="\n")
        print('ASList(', len(result[2]), ')', result[2], file=text_file)
        print(sep="\n")
        print('AWList(', len(result[3]), ')', result[3], file=text_file)
        print(sep="\n")
        print('AgSDict(', len(result[4]), ')', result[4], file=text_file)
        print(sep="\n")
        print('Vertex matrix (', len(result[5]), ')', result[5], file=text_file)
        End = datetime.datetime.now()

    print("Time of running: ", End - Start)
