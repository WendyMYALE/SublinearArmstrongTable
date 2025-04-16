import logging
import datetime
import math
import copy
import random
import itertools

import FunctionSet
import ATMining
import InitFromAgS

#logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.WARNING)
logging.getLogger('Informative').setLevel(logging.DEBUG)


def EdgeNumber(AgS):
    """
    :param AgS: Agree sets occurence
    :return: Vertexes list
    """

    V = []
    for k in AgS.keys():
        i = AgS[k][1][0][0]
        j = AgS[k][1][0][1]
        n = math.ceil(j * (j - 1) / 2) + i
        if AgS[k][0] > 1:
            for a in range(AgS[k][0] - 1):
                i1 = AgS[k][1][a][0]
                j1 = AgS[k][1][a][1]
                if math.ceil(j1 * (j1 - 1) / 2) + i1 < n:
                    i = i1
                    j = j1

        if i not in V: V.append(i)
        if j not in V: V.append(j)

    print("EDGE NUMBER: {} vertexes left: {}".format(len(V), sorted(V)))

    return sorted(V)

def KeyVertex(AgS):
    """
    :param AgS: Agree sets occurence
    :return: Vertexes list
    """

    V = []
    ## For agree sets only appear once
    for k in AgS.keys():
        if AgS[k][0] == 1:
            i = AgS[k][1][0][0]
            j = AgS[k][1][0][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)

    ## For agree sets appear more than once
    for k in AgS.keys():
        if AgS[k][0] > 1:
            n = -1
            for a in range(AgS[k][0]):
                ## Both vertexes already in graph
                if AgS[k][1][a][0] in V and AgS[k][1][a][1] in V:
                    i = AgS[k][1][a][0]
                    j = AgS[k][1][a][1]
                    n = math.ceil(j * (j - 1) / 2) + i
                    break
                ## Only one vertex in graph
                elif AgS[k][1][a][0] in V or AgS[k][1][a][1] in V:
                    i = AgS[k][1][a][0]
                    j = AgS[k][1][a][1]
                    n = math.ceil(j * (j - 1) / 2) + i

            ## None of vertexes in graph, pick first edge
            if n == -1:
                i = AgS[k][1][0][0]
                j = AgS[k][1][0][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)

    print("KEY VERTEX: {} vertexes left: {}".format(len(V), sorted(V)))

    return sorted(V)

def EdgeRank(AgS):
    """
    :param AgS: Agree sets occurence
    :return: Vertexes list
    """

    VDict = {}
    for k in AgS.keys():
        for a in range(AgS[k][0]):
            if AgS[k][1][a][0] not in VDict.keys():
                VDict[AgS[k][1][a][0]] = [k]
            elif k not in VDict[AgS[k][1][a][0]]:
                VDict[AgS[k][1][a][0]].append(k)

            if AgS[k][1][a][1] not in VDict.keys():
                VDict[AgS[k][1][a][1]] = [k]
            elif k not in VDict[AgS[k][1][a][1]]:
                VDict[AgS[k][1][a][1]].append(k)

    V = []
    for k in AgS.keys():
        i = AgS[k][1][0][0]
        j = AgS[k][1][0][1]
        r = max(len(VDict[i]), len(VDict[j]))
        if AgS[k][0] > 1:
            for a in range(AgS[k][0] - 1):
                i1 = AgS[k][1][a][0]
                j1 = AgS[k][1][a][1]
                if max(len(VDict[i1]), len(VDict[j1])) > r:
                    i = i1
                    j = j1

        if i not in V: V.append(i)
        if j not in V: V.append(j)

    #print("Vertex dictionary ({}): {}".format(len(VDict), VDict))
    print("EDGE RANK: {} vertexes left: {}".format(len(V), sorted(V)))

    return sorted(V)

def WeightedEdgeRank(AgS):
    """
    :param AgS: Agree sets occurence
    :return: Vertexes list
    """

    VDict = {}
    for k in AgS.keys():
        for a in range(AgS[k][0]):
            if AgS[k][1][a][0] not in VDict.keys():
                VDict[AgS[k][1][a][0]] = [k]
            elif k not in VDict[AgS[k][1][a][0]]:
                VDict[AgS[k][1][a][0]].append(k)

            if AgS[k][1][a][1] not in VDict.keys():
                VDict[AgS[k][1][a][1]] = [k]
            elif k not in VDict[AgS[k][1][a][1]]:
                VDict[AgS[k][1][a][1]].append(k)

    V = []
    ## For agree sets only appear once
    for k in AgS.keys():
        if AgS[k][0] == 1:
            i = AgS[k][1][0][0]
            j = AgS[k][1][0][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)

    ## For agree sets appear more than once
    weight = (len(VDict) + sum(AgS[item][0] for item in AgS)) * 10
    for k in AgS.keys():
        if AgS[k][0] > 1:
            r = -1
            for a in range(AgS[k][0]):
                ## Both vertexes already in graph
                if AgS[k][1][a][0] in V and AgS[k][1][a][1] in V:
                    i1 = AgS[k][1][a][0]
                    j1 = AgS[k][1][a][1]
                    if max(len(VDict[i1]), len(VDict[j1])) + weight * 2  > r:
                        i = i1
                        j = j1
                        r = max(len(VDict[i]), len(VDict[j])) + weight * 2
                ## Only one vertex in graph
                elif AgS[k][1][a][0] in V or AgS[k][1][a][1] in V:
                    i1 = AgS[k][1][a][0]
                    j1 = AgS[k][1][a][1]
                    if max(len(VDict[i1]), len(VDict[j1])) + weight > r:
                        i = i1
                        j = j1
                        r = max(len(VDict[i]), len(VDict[j])) + weight
                ## None of vertexes in graph
                else:
                    i1 = AgS[k][1][a][0]
                    j1 = AgS[k][1][a][1]
                    if max(len(VDict[i1]), len(VDict[j1])) > r:
                        i = i1
                        j = j1
                        r = max(len(VDict[i]), len(VDict[j]))

            if i not in V: V.append(i)
            if j not in V: V.append(j)

    print("WIGHTED EDGE RANK: {} vertexes left: {}".format(len(V), sorted(V)))

    return sorted(V)

def VertexRank(AgS):
    """
    :param AgS: Agree sets occurence
    :return: Vertexes list
    """
    p = 0   # Flag to print for debugging

    VDict = {}
    for k in AgS.keys():
        for a in range(AgS[k][0]):
            if AgS[k][1][a][0] not in VDict.keys():
                VDict[AgS[k][1][a][0]] = [k]
            elif k not in VDict[AgS[k][1][a][0]]:
                VDict[AgS[k][1][a][0]].append(k)

            if AgS[k][1][a][1] not in VDict.keys():
                VDict[AgS[k][1][a][1]] = [k]
            elif k not in VDict[AgS[k][1][a][1]]:
                VDict[AgS[k][1][a][1]].append(k)

    V = []
    ## For agree sets only appear once
    for k in AgS.keys():
        if AgS[k][0] == 1:
            i = AgS[k][1][0][0]
            j = AgS[k][1][0][1]

            if i not in V: V.append(i)
            if i in VDict.keys(): del VDict[i]
            if j not in V: V.append(j)
            if j in VDict.keys(): del VDict[j]

    ## Randomly choose highest rank vertexes
    DupList = [item for item in AgS.keys() if AgS[item][0] > 1]
    if len(DupList) > 0:
        sVDict = {}
        for k in VDict.keys():
            sVDict[k] = VDict[k]
        sVDict = {k: v for k, v in sorted(sVDict.items(), key=lambda item: len(item[1]), reverse=True)}
        candidateV = [item for item in sVDict.keys()]

    while len(DupList) > 0:
        maxL = len(sVDict[list(sVDict.keys())[0]])
        pool = [item for item in VDict.keys() if len(VDict[item]) == maxL and item in candidateV]
        if p: print("Candidate vertexes pool: ", pool)

        if len(pool) > 1:
            chosenV = random.choice(pool)
        else:
            chosenV = pool[0]
        if chosenV not in V: V.append(chosenV)
        if chosenV in VDict.keys(): del VDict[chosenV]

        ## Check agree sets appearance
        for k in AgS.keys():
            if AgS[k][0] > 1:
                tempAgS = copy.deepcopy(AgS[k])
                for i in range(tempAgS[0]):
                    if tempAgS[1][i][0] in V and tempAgS[1][i][1] in V:
                        # to remove unchosen edges from the graph!!
                        AgS[k][0] = 1
                        AgS[k][1].clear()
                        AgS[k][1].append((tempAgS[1][i][0], tempAgS[1][i][1]))
                        break

        DupList = [item for item in AgS.keys() if AgS[item][0] > 1]
        if len(DupList) > 0:
            candidateV = []
            for Key in AgS.keys():
                if AgS[Key][0] > 1:
                    l = list(set(itertools.chain(*AgS[Key][1])))
                    candidateV = candidateV + list(set(l) - set(candidateV))

            sVDict = {}
            for a in VDict.keys():
                if a in candidateV:
                    sVDict[a] = VDict[a]
            sVDict = {k: v for k, v in sorted(sVDict.items(), key=lambda item: len(item[1]), reverse=True)}

    print("VERTEX RANK: {} vertexes left: {}".format(len(V), sorted(V)))

    return sorted(V)

def WeightedVertexRank_Update(AgS): ## Dynamic update
    """
    :param AgS: Agree sets occurence
    :return: Vertexes list
    """
    p = 0   # Flag to print for debugging

    V = []
    ## For agree sets only appear once
    for k in AgS.keys():
        if AgS[k][0] == 1:
            i = AgS[k][1][0][0]
            j = AgS[k][1][0][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)

    weight = sum(AgS[item][0] for item in AgS) * 10
    DupList = [item for item in AgS.keys() if AgS[item][0] > 1]

    VDict = {}
    for d in range(len(DupList)):  ## each duplicate agree set
        k = DupList[d]
        for a in range(AgS[k][0]):  ## each vertexes pair
            if AgS[k][1][a][0] not in VDict.keys():
                VDict[AgS[k][1][a][0]] = [[k], [(k, AgS[k][1][a][1])], [v for v in V if v == AgS[k][1][a][1]]] ## add VDict key with first vertex
            else:
                if k not in VDict[AgS[k][1][a][0]][0]:
                    VDict[AgS[k][1][a][0]][0].append(k)  ## add unique adjacent AgS
                if (k, AgS[k][1][a][1]) not in VDict[AgS[k][1][a][0]][1]:
                    VDict[AgS[k][1][a][0]][1].append((k, AgS[k][1][a][1]))  ## add adjacent AgS & neighbour vertex pair
                if AgS[k][1][a][1] in V and AgS[k][1][a][1] not in VDict[AgS[k][1][a][0]][2]:
                    VDict[AgS[k][1][a][0]][2].append(AgS[k][1][a][1])   ## weighted vertex

            if AgS[k][1][a][1] not in VDict.keys():
                VDict[AgS[k][1][a][1]] = [[k], [(k, AgS[k][1][a][0])], [v for v in V if v == AgS[k][1][a][0]]]  ## add VDict key with second vertex
            else:
                if k not in VDict[AgS[k][1][a][1]][0]:
                    VDict[AgS[k][1][a][1]][0].append(k)
                if (k, AgS[k][1][a][0]) not in VDict[AgS[k][1][a][1]][1]:
                    VDict[AgS[k][1][a][1]][1].append((k, AgS[k][1][a][0]))
                if AgS[k][1][a][0] in V and AgS[k][1][a][0] not in VDict[AgS[k][1][a][1]][2]:
                    VDict[AgS[k][1][a][1]][2].append(AgS[k][1][a][0])

    for i in range(len(V)):
        if V[i] in VDict.keys(): del VDict[V[i]]

    if p:
        print("AgS(", len(AgS), "):", AgS)
        print("V(", len(V), "):", V)
        print("weight =", weight)
        print("DupList(", len(DupList), "):", DupList)
        print("VDict(", len(VDict), "):", VDict)

    chosenV = None
    #for x in range(2):
    while len(DupList) > 0:
        sVDict = {}
        for k in VDict.keys():
            sVDict[k] = len(VDict[k][0]) + len(VDict[k][2]) * weight
        sVDict = {k: v for k, v in sorted(sVDict.items(), key=lambda item: item[1], reverse=True)}
        candidateV = [item for item in sVDict.keys()]

        maxL = sVDict[list(sVDict.keys())[0]]
        pool = [item for item in sVDict.keys() if sVDict[item] == maxL and item in candidateV]
        if p:
            print("sVDict(", len(sVDict), "):", sVDict)
            print("pool(", len(pool), "):", pool)

        chosenV = random.choice(pool)
        if chosenV not in V: V.append(chosenV)
        if chosenV in VDict.keys(): del VDict[chosenV]
        if p: print("{} is chosen.".format(chosenV))

        ## Check Duplist
        ToRemove = []
        for i in range(len(DupList)):    ## each duplicate agree set
            for j in range(AgS[DupList[i]][0]): ## each vertexes pair
                if AgS[DupList[i]][1][j][0] in V and AgS[DupList[i]][1][j][1] in V:  ## both vertexes in V
                    ToRemove.append(DupList[i])
                    #AgS[DupList[i]] = [1, [(AgS[DupList[i]][1][j][0], AgS[DupList[i]][1][j][1])]]
                    if p: print("Duplicate of ", DupList[i], "has been removed.")
                    break

        DupList = [item for item in DupList if item not in ToRemove]

        ToDelete = []
        for k in VDict.keys():
            VDict[k][0] = [item for item in VDict[k][0] if item not in ToRemove]    ##remove AgS becomes unique
            if len(VDict[k][0]) == 0:
                ToDelete.append(k)
                if p: print(k, "has been deleted from VDict")
            else:
                for i in range(len(VDict[k][1])):
                    ## duplicate AgS adjacent to vertex in V
                    if VDict[k][1][i][0] not in ToRemove and chosenV == VDict[k][1][i][1] and chosenV not in VDict[k][2]:
                        VDict[k][2].append(chosenV)
                    ## unique AgS with neighbor vertex already in V
                    elif VDict[k][1][i][0] in ToRemove and VDict[k][1][i][1] in VDict[k][2]:
                        VDict[k][2].remove(VDict[k][1][i][1])

        for i in range(len(ToDelete)):
           if ToDelete[i] in VDict.keys(): del VDict[ToDelete[i]]

        if p:
            print("V(", len(V), ")", V)
            print("DupList(", len(DupList), ")", DupList)
            print("VDict(", len(VDict))#, "):", VDict)

    print("WEIGHTED VERTEX RANK: {} vertexes left: {}".format(len(V), sorted(V)))

    return sorted(V)

def WeightedVertexRank_old(AgS):
    """
    :param AgS: Agree sets occurence
    :return: Vertexes list
    """
    p = 0  # Flag to print for debugging

    VDict = {}
    for k in AgS.keys():
        for a in range(AgS[k][0]):
            if AgS[k][1][a][0] not in VDict.keys():
                VDict[AgS[k][1][a][0]] = ([k], [AgS[k][1][a][1]])
            elif k not in VDict[AgS[k][1][a][0]][0]:
                VDict[AgS[k][1][a][0]][0].append(k)
                if AgS[k][1][a][1] not in VDict[AgS[k][1][a][0]][1]:
                    VDict[AgS[k][1][a][0]][1].append(AgS[k][1][a][1])

            if AgS[k][1][a][1] not in VDict.keys():
                VDict[AgS[k][1][a][1]] = ([k], [AgS[k][1][a][0]])
            elif k not in VDict[AgS[k][1][a][1]][0]:
                VDict[AgS[k][1][a][1]][0].append(k)
                if AgS[k][1][a][0] not in VDict[AgS[k][1][a][1]][1]:
                    VDict[AgS[k][1][a][1]][1].append(AgS[k][1][a][0])

    V = []
    ## For agree sets only appear once
    for k in AgS.keys():
        if AgS[k][0] == 1:
            i = AgS[k][1][0][0]
            j = AgS[k][1][0][1]

            if i not in V: V.append(i)
            if i in VDict.keys(): del VDict[i]
            if j not in V: V.append(j)
            if j in VDict.keys(): del VDict[j]

    weight = (len(VDict) + sum(AgS[item][0] for item in AgS)) * 10
    DupList = [item for item in AgS.keys() if AgS[item][0] > 1]

    ## Randomly choose highest rank vertexes
    while len(DupList) > 0:
        sVDict = {}
        for k in VDict.keys():
            sVDict[k] = len(VDict[k][0]) + len([item for item in VDict[k][1] if item in V]) * weight
        sVDict = {k: v for k, v in sorted(sVDict.items(), key=lambda item: item[1], reverse=True)}
        candidateV = [item for item in sVDict.keys()]

        maxL = sVDict[list(sVDict.keys())[0]]
        pool = [item for item in sVDict.keys() if sVDict[item] == maxL and item in candidateV]
        if p:
            print("sVDict", sVDict)
            print("pool: ", pool)

        chosenV = random.choice(pool)
        if p: print("{} is chosen.".format(chosenV))
        if chosenV not in V: V.append(chosenV)
        if chosenV in VDict.keys(): del VDict[chosenV]

        ## Check agree sets appearance
        for k in AgS.keys():    ## for each AgS
            if AgS[k][0] > 1:
                tempAgS = copy.deepcopy(AgS[k]) ##eg. tempAgS = [2, [(70, 126), (70, 138)]]
                for i in range(tempAgS[0]):
                    if tempAgS[1][i][0] in V and tempAgS[1][i][1] in V: ## both vertexes in V
                        ## Take off removed egdes from VDict - cList = [70, 126, 138] - [70, 126]
                        cList = [item for item in list(set(itertools.chain(*AgS[k][1]))) if item not in tempAgS[1][i]]
                        for j in range(len(cList)):
                            if cList[j] in VDict.keys():
                                tempV = copy.deepcopy(VDict[cList[j]])
                                for ki in range(len(tempV[0])):
                                    if tempV[0][ki] == k:
                                        VDict[cList[j]][0].remove(k)
                                        VDict[cList[j]][1].remove(tempV[1][ki])

                        AgS[k][0] = 1
                        AgS[k][1].clear()
                        AgS[k][1].append((tempAgS[1][i][0], tempAgS[1][i][1]))

                        break

        DupList = [item for item in AgS.keys() if AgS[item][0] > 1]
        if len(DupList) > 0:
            candidateV = []
            for Key in AgS.keys():
                if AgS[Key][0] > 1:
                    l = list(set(itertools.chain(*AgS[Key][1])))
                    candidateV = candidateV + list(set(l) - set(candidateV))

            sVDict = {}
            for a in VDict.keys():
                if a in candidateV:
                    sVDict[a] = len(VDict[a][0]) + len([item for item in VDict[a][1] if item in V]) * weight
            sVDict = {k: v for k, v in sorted(sVDict.items(), key=lambda item: item[1], reverse=True)}

    print("WEIGHTED VERTEX RANK: {} vertexes left: {}".format(len(V), sorted(V)))
    if p: print("Final graph", AgS)

    return sorted(V)

def WeightedVertexRank(AgS):
    """
    :param AgS: Agree sets occurence
    :return: Vertexes list
    """
    p = 0   # Flag to print for debugging

    V = []
    ## For agree sets only appear once
    for k in AgS.keys():
        if AgS[k][0] == 1:
            i = AgS[k][1][0][0]
            j = AgS[k][1][0][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)

    weight = sum(AgS[item][0] for item in AgS) * 10
    DupList = [item for item in AgS.keys() if AgS[item][0] > 1]

    if p:
        print("AgS(", len(AgS), "):", AgS)
        print("V(", len(V), "):", V)
        print("weight =", weight)
        print("DupList(", len(DupList), "):", DupList)

    #for x in range(2):
    while len(DupList) > 0:
        VDict = {}
        for d in range(len(DupList)):  ## each duplicate agree set
            k = DupList[d]
            for a in range(AgS[k][0]):  ## each vertexes pair
                if AgS[k][1][a][0] not in V:
                    if AgS[k][1][a][0] not in VDict.keys():
                        VDict[AgS[k][1][a][0]] = ([k], [v for v in V if v == AgS[k][1][a][1]])  ## add VDict key with first vertex
                    else:
                        if k not in VDict[AgS[k][1][a][0]][0]:
                            VDict[AgS[k][1][a][0]][0].append(k)  ## add unique adjacent AgS
                        if AgS[k][1][a][1] in V and AgS[k][1][a][1] not in VDict[AgS[k][1][a][0]][1]:
                            VDict[AgS[k][1][a][0]][1].append(AgS[k][1][a][1])  ## weighted vertex

                if AgS[k][1][a][1] not in V:
                    if AgS[k][1][a][1] not in VDict.keys():
                        VDict[AgS[k][1][a][1]] = ([k], [v for v in V if v == AgS[k][1][a][0]]) ## add VDict key with second vertex
                    else:
                        if k not in VDict[AgS[k][1][a][1]][0]:
                            VDict[AgS[k][1][a][1]][0].append(k)
                        if AgS[k][1][a][0] in V and AgS[k][1][a][0] not in VDict[AgS[k][1][a][1]][1]:
                            VDict[AgS[k][1][a][1]][1].append(AgS[k][1][a][0])

        sVDict = {}
        for k in VDict.keys():
            sVDict[k] = len(VDict[k][0]) + len(VDict[k][1]) * weight
        sVDict = {k: v for k, v in sorted(sVDict.items(), key=lambda item: item[1], reverse=True)}
        candidateV = [item for item in sVDict.keys()]

        maxL = sVDict[list(sVDict.keys())[0]]
        pool = [item for item in sVDict.keys() if sVDict[item] == maxL and item in candidateV]
        if p:
            print("VDict(", len(VDict), "):", VDict)
            print("sVDict(", len(sVDict), "):", sVDict)
            print("pool(", len(pool), "):", pool)

        chosenV = random.choice(pool)
        if chosenV not in V: V.append(chosenV)
        if p: print("{} is chosen.".format(chosenV))

        ## Check Duplist
        ToRemove = []
        for i in range(len(DupList)):    ## each duplicate agree set
            for j in range(AgS[DupList[i]][0]): ## each vertexes pair
                if AgS[DupList[i]][1][j][0] in V and AgS[DupList[i]][1][j][1] in V:  ## both vertexes in V
                    ToRemove.append(DupList[i])
                    #AgS[DupList[i]] = [1, [(AgS[DupList[i]][1][j][0], AgS[DupList[i]][1][j][1])]]
                    if p: print("Duplicate of ", DupList[i], "has been removed.")
                    break

        DupList = [item for item in DupList if item not in ToRemove]

        if p:
            print("V(", len(V), ")", V)
            print("DupList(", len(DupList), ")", DupList)
            print("VDict(", len(VDict), "):", VDict)

    print("WEIGHTED VERTEX RANK: {} vertexes left: {}".format(len(V), sorted(V)))

    return sorted(V)

f = 'echocardiogram'
Mining = False
pa1 = "/Users/wye1/Documents/Armstrong/DataSets/naumann_small/"
pa2 = "/Users/wye1/Documents/Armstrong/DataSets/naumann_mined_agree_sets/"
path = "/users/wye1/Documents/Armstrong/Informative/WorkFolder/"
#pa = "D:/Wendy/Armstrong/DataSets/naumann_small/"
#path = "D:/Wendy/Armstrong/Informative/WorkFolder/"
ATFile = pa1 + f + '.csv'
ASFile = pa2 + f + '.txt'

# Main
if __name__ == "__main__":
    Start  = datetime.datetime.now()

    if Mining:
        MineResult = ATMining.ATMining(ATFile)
        AgSList = MineResult[1]
        R = MineResult[2]
        AgSDict = MineResult[3]
    else:
        Result = InitFromAgS.InitGraph(ATFile, ASFile)
        AgSList = Result[1]
        R = Result[2]
        AgSDict = Result[3]

    AgS = {}
    for i in range(len(AgSList)):
        AgS[FunctionSet.BitToString(R, AgSList[i])] = [0, []]

    V = []
    for k in AgSDict.keys():
        if AgSDict[k] in AgS.keys():
            AgS[AgSDict[k]][0] += 1
            AgS[AgSDict[k]][1].append(k)

            if k[0] not in V: V.append(k[0])
            if k[1] not in V: V.append(k[1])

    print("Agree sets occurence ({}): {}".format(len(AgS), AgS))
    V = sorted(V)
    print("Unisolated Vertexes({}): {}".format(len(V), V))

    Start1  = datetime.datetime.now()
    copyAgS = copy.deepcopy(AgS)
    V1 = EdgeNumber(copyAgS)
    End1 = datetime.datetime.now()
    print("Runs for: ", End1 - Start1)

    Start2  = datetime.datetime.now()
    copyAgS = copy.deepcopy(AgS)
    V2 = KeyVertex(copyAgS)
    End2 = datetime.datetime.now()
    print("Runs for: ", End2 - Start2)

    Start3  = datetime.datetime.now()
    copyAgS = copy.deepcopy(AgS)
    V3 = EdgeRank(copyAgS)
    End3 = datetime.datetime.now()
    print("Runs for: ", End3 - Start3)

    Start4  = datetime.datetime.now()
    copyAgS = copy.deepcopy(AgS)
    V4 = WeightedEdgeRank(copyAgS)
    End4 = datetime.datetime.now()
    print("Runs for: ", End4 - Start4)

    #Start5  = datetime.datetime.now()
    #copyAgS = copy.deepcopy(AgS)
    #V5 = VertexRank(copyAgS)
    #End5 = datetime.datetime.now()
    #print("Runs for: ", End5 - Start5)

    Start6  = datetime.datetime.now()
    copyAgS = copy.deepcopy(AgS)
    V6 = WeightedVertexRank(copyAgS)
    End6 = datetime.datetime.now()
    print("Runs for: ", End6 - Start6)

    End = datetime.datetime.now()

    print("Time of running: ", End - Start)
