import copy
import datetime

import FunctionSet
import ATMining
import Hauristic
import Domination
import Domination0
import Domination1

f = 'abalone'
pa = "/Users/wye1/Documents/Armstrong/DataSets/naumann_small/"
path = "/users/wye1/Documents/Armstrong/Informative/WorkFolder/"
#pa = "D:/Wendy/Armstrong/DataSets/naumann_small/"
#path = "D:/Wendy/Armstrong/Informative/WorkFolder/"
ATFile = pa + f + '.csv'
rCounter = 10
if rCounter > 1:
    OutFile = path + f + ".txt"
else:
    OutFile = path + f + "_result.txt"

# Main
if __name__ == "__main__":
    Start  = datetime.datetime.now()

    MineResult = ATMining.ATMining(ATFile)
    AgSList = MineResult[1]
    R = MineResult[2]
    AgSDict = MineResult[3]

    AgS = {}
    for i in range(len(AgSList)):
        AgS[FunctionSet.BitToString(R, AgSList[i])] = [0, []]

    V = []
    NewDict = {}
    for k in AgSDict.keys():
        if AgSDict[k] in AgS.keys():
            AgS[AgSDict[k]][0] += 1
            AgS[AgSDict[k]][1].append(k)

            if k[0] not in V: V.append(k[0])
            if k[1] not in V: V.append(k[1])
            NewDict[k] = AgSDict[k]

    #print("New Agree sets Dictionary ({}): {}".format(len(NewDict), NewDict))
    print("Agree sets occurrence ({}): {}".format(len(AgS), AgS))
    V = sorted(V)
    print("Unisolated Vertexes({}): {}".format(len(V), V))

    Start1  = datetime.datetime.now()
    copyAgS = copy.deepcopy(AgS)
    V1 = Hauristic.EdgeNumber(copyAgS)
    End1 = datetime.datetime.now()
    print("Runs for: ", End1 - Start1)

    Start2  = datetime.datetime.now()
    copyAgS = copy.deepcopy(AgS)
    V2 = Hauristic.KeyVertex(copyAgS)
    End2 = datetime.datetime.now()
    print("Runs for: ", End2 - Start2)

    Start3  = datetime.datetime.now()
    copyAgS = copy.deepcopy(AgS)
    V3 = Hauristic.EdgeRank(copyAgS)
    End3 = datetime.datetime.now()
    print("Runs for: ", End3 - Start3)

    Start4  = datetime.datetime.now()
    copyAgS = copy.deepcopy(AgS)
    V4 = Hauristic.WeightedEdgeRank(copyAgS)
    End4 = datetime.datetime.now()
    print("Runs for: ", End4 - Start4)

    # Start50  = datetime.datetime.now()
    # copyAgS = copy.deepcopy(AgS)
    # copyV = copy.deepcopy((V))
    # Outcome = Domination0.Domination(copyAgS, copyV)
    # V50 = Outcome[1]
    # dCounter50 = Outcome[2]
    # End50 = datetime.datetime.now()
    # print("Runs for: ", End50 - Start50)

    Start5  = datetime.datetime.now()
    dOutcome5 = []
    for i in range(rCounter):
        copyAgS = copy.deepcopy(AgS)
        Outcome5 = Domination1.Domination1(copyAgS)
        V5 = Outcome5[1]
        dCounter = Outcome5[2]
        counter = Outcome5[3]
        dOutcome5.append([i + 1, len(V5), dCounter, counter])
        i += 1
    print(dOutcome5)
    End5 = datetime.datetime.now()
    print("Runs for: ", End5 - Start5)

    # Start6  = datetime.datetime.now()
    # dOutcome6 = []
    # for i in range(rCounter):
    #     copyAgS = copy.deepcopy(AgS)
    #     V6 = Hauristic.VertexRank(copyAgS)
    #     dOutcome6.append([i + 1, len(V6)])
    #     i += 1
    # print(dOutcome6)
    # End6 = datetime.datetime.now()
    # print("Runs for: ", End6 - Start6)

    Start7  = datetime.datetime.now()
    dOutcome7 = []
    for i in range(rCounter):
        copyAgS = copy.deepcopy(AgS)
        V7 = Hauristic.WeightedVertexRank(copyAgS)
        dOutcome7.append([i + 1, len(V7)])
        i += 1
    print(dOutcome7)
    End7 = datetime.datetime.now()
    print("Runs for: ", End7 - Start7)

    # Start8  = datetime.datetime.now()
    # dOutcome8 = []
    # for i in range(rCounter):
    #     copyAgS = copy.deepcopy(AgS)
    #     Outcome8 = Domination.Domination(copyAgS)
    #     V8 = Outcome8[1]
    #     dCounter = Outcome8[2]
    #     counter = Outcome8[3]
    #     dOutcome8.append([i + 1, len(V8), dCounter, counter])
    #     i += 1
    # print(dOutcome8)
    # End8 = datetime.datetime.now()
    # print("Runs for: ", End8 - Start8)

    with open(OutFile, "w") as text_file:
        print("EDGE NUMBER: {}".format(len(V1)), sep="\n", file=text_file)
        if rCounter == 1: print(V1, sep="\n", file=text_file)
        print("KEY VERTEX: {}".format(len(V2)), sep="\n", file=text_file)
        if rCounter == 1: print(V2, sep="\n", file=text_file)
        print("EDGE RANK: {}".format(len(V3)), sep="\n", file=text_file)
        if rCounter == 1: print(V3, sep="\n", file=text_file)
        print("WIGHTED EDGE RANK: {}".format(len(V4)), sep="\n", file=text_file)
        if rCounter == 1: print(V4, sep="\n", file=text_file)
        #print("DOMINATION + WEIGHTED EDGE RANK: {}; Domination Occur: {}".format(len(V50), dCounter50), sep="\n", file=text_file)
        if rCounter > 1:
            print("DOMINATION by Agree sets + WEIGHTED VERTEX RANK: ", sep="\n", file=text_file)
            print("[#, Output, Domination Occur, Total checks]", sep="\n", file=text_file)
            print(*['\n'.join([str(e) for e in dOutcome5])], sep="\n", file=text_file)
        else:
            print("DOMINATION by Agree sets + WEIGHTED VERTEX RANK: {}".format(dOutcome5[0][1]), sep="\n", file=text_file)
            print(V5, sep="\n", file=text_file)
        # print("VERTEX RANK: ", sep="\n", file=text_file)
        # print("[#, Output]", sep="\n", file=text_file)
        # print(*['\n'.join([str(e) for e in dOutcome6])], sep="\n", file=text_file)
        if rCounter > 1:
            print("WEIGHTED VERTEX RANK: ", sep="\n", file=text_file)
            print("[#, Output]", sep="\n", file=text_file)
            print(*['\n'.join([str(e) for e in dOutcome7])], sep="\n", file=text_file)
        else:
            print("WIGHTED VERTEX RANK: {}".format(dOutcome7[0][1]), sep="\n", file=text_file)
            print(V7, sep="\n", file=text_file)
        # if rCounter > 1:
        #     print("DOMINATION by Vertexes + WEIGHTED VERTEX RANK: ", sep="\n", file=text_file)
        #     print("[#, Output, Domination Occur, Total checks]", sep="\n", file=text_file)
        #     print(*['\n'.join([str(e) for e in dOutcome8])], sep="\n", file=text_file)
        # else:
        #     print("DOMINATION by Agree sets + WEIGHTED VERTEX RANK: {}".format(dOutcome8[0][1]), sep="\n", file=text_file)
        #     print(V8, sep="\n", file=text_file)

    End = datetime.datetime.now()

    print("Time of running: ", End - Start)
