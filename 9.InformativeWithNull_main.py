## Update metrics for vertexes required
import datetime
import math
import copy
import random
import collections

import Function4Null
import InitFromAsAw_main

def ExtraCheck(V0, V, W):
    eCount = {}
    ASCount = {}
    for k in sAS.keys():
        ASCount[k] = [0, []]
        for a in range(sAS[k][0]):
            if sAS[k][1][a][0] in V and sAS[k][1][a][1] in V:
                ASCount[k][0] += 1
                ASCount[k][1].append(sAS[k][1][a])
                if sAS[k][1][a] not in eCount.keys():
                    eCount[sAS[k][1][a]] = [1, [k]]
                else:
                    eCount[sAS[k][1][a]][0] += 1
                    eCount[sAS[k][1][a]][1].append(k)

    for k in wAS.keys():
        ASCount[k] = [0, []]
        for a in range(wAS[k][0]):
            if wAS[k][1][a][0] in V and wAS[k][1][a][1] in V:
                ASCount[k][0] += 1
                ASCount[k][1].append(wAS[k][1][a])
                if wAS[k][1][a] not in eCount.keys():
                    eCount[wAS[k][1][a]] = [1, [k]]
                else:
                    eCount[wAS[k][1][a]][0] += 1
                    eCount[wAS[k][1][a]][1].append(k)

    newE = [i[1] for i in ASCount.values() if i[0] == 1]
    newV = list(set(sum([item for Tups in newE for item in Tups], ())))
    for a in ASCount.keys():
        if ASCount[a][0] > 0:
            ePair = ASCount[a][1][0]
            for i in range(len(ASCount[a][1])):
                if ASCount[a][1][i][0] in newV and ASCount[a][1][i][1] in newV:
                    ePair = ()
                    break
                elif ASCount[a][1][i][0] in newV or ASCount[a][1][i][1] in newV:
                    ePair = ASCount[a][1][i]

            for j in range(len(ePair)):
                if ePair[j] not in newV: newV.append(ePair[j])

    if len(V) - len(newV) > 0:
       if ToDebug:
           print("{} vertexes removed with duplicates, {} vertexes left: {}".format(len(V) - len(newV), len(newV), sorted(newV)))

    w = [a * b for a, b in zip(V0[newV[0]], W)]
    for i in range(len(newV) - 1):
        w1 = [a * b for a, b in zip(V0[newV[i + 1]], W)]
        w = [1 if c + d > 0 else 0 for c, d in zip(w, w1)]
    if w != W:
        w0 = [1 if e - f > 0 else 0 for e, f in zip(W, w)]
        for v in V0.keys():
            if [g * h for g, h in zip(V0[v], w0)] == w0:
                newV.append(v)
                break
        if ToDebug: print("Extra vertex added: {} vertexes left: {}".format(len(newV), sorted(newV)))
    return (newV)

def vGroup(VDict):
    vList = [item for item in VDict.keys()]
    vRank = [[vList[0]]]
    for i in range(len(vList)):
        NewGroup = True
        for j in range(len(vRank)):
            if vList[i] in vRank[j] or len([item for item in VDict[vList[i]][1] if item in vRank[j]]) > 0:
                vRank[j] = list(set(vRank[j] + [vList[i]] + VDict[vList[i]][1]))
                NewGroup = False
        if NewGroup:
            vRank.append(list(set([vList[i]] + VDict[vList[i]][1])))

    vRankFlat = [item for sublist in vRank for item in sublist]
    DupV = [item for item, count in collections.Counter(vRankFlat).items() if count > 1]
    if len(DupV) > 0:
        ToMerge = []
        for i in range(len(vRank)):
            if len([item for item in vRank[i] if item in DupV]) > 0:
                ToMerge.append(vRank[i])
        for j in range(len(ToMerge)):
            vRank.remove(ToMerge[j])
        vRank.append(list(set([item for sublist in ToMerge for item in sublist])))
    if ToDebug: print("vList:", len(vList), "vs vRank:", len([item for sublist in vRank for item in sublist]))

    return vRank

def GetMetrics(m, v, mFactor, vRank, dBonus, weight):
    for l in range(len(vRank)):
        if v in vRank[l]:
            gIndex = len(vRank[l])

    if m == 0:  ## Occurence + double assignment bonus
        if v in dBonus.keys():
            dBonusV = dBonus[v]
        else:
            dBonusV = 0
        metric = [mFactor[0][0], sum([1 / item for item in mFactor[0][1]]) * 2 * weight ** 2 + sum([1 / item for item in mFactor[0][3]]) * weight ** 2
                                + sum([1 / item for item in mFactor[1][1]]) * 2 * weight + sum([1 / item for item in mFactor[1][3]]) * weight + gIndex + dBonusV * math.sqrt(weight)]
    elif m == 1:  ## Occurence
        metric = [mFactor[0][0], sum([1 / item for item in mFactor[0][1]]) * 2 * weight ** 2 + sum([1 / item for item in mFactor[0][3]]) * weight ** 2
                                + sum([1 / item for item in mFactor[1][1]]) * 2 * weight + sum([1 / item for item in mFactor[1][3]]) * weight + gIndex]
    elif m == 2:  ## O ** 2
        metric = [mFactor[0][0], sum([1 / item ** 2 for item in mFactor[0][1]]) * 2 * weight ** 2 + sum([1 / item ** 2 for item in mFactor[0][3]]) * weight ** 2
                                + sum([1 / item for item in mFactor[1][1]]) * 2 * weight + sum([1 / item for item in mFactor[1][3]]) * weight + gIndex]
    elif m == 3:  ## sqrt(O)
        metric = [mFactor[0][0], sum([1 / math.sqrt(item) for item in mFactor[0][1]]) * 2 * weight ** 2 + sum([1 / math.sqrt(item) for item in mFactor[0][3]]) * weight ** 2
                                + sum([1 / math.sqrt(item) for item in mFactor[1][1]]) * 2 * weight + sum([1 / math.sqrt(item) for item in mFactor[1][3]]) * weight + gIndex]

    return metric

def Sequence(sAS, wAS):
    """
    :param sAS: Strong agree sets occurence
    :param wAS: Weak agree sets occurence
    :return: Vertexes list
    """
    V = []
    for k in sAS.keys():
        i = sAS[k][1][0][0]
        j = sAS[k][1][0][1]
        n = math.ceil(j * (j - 1) / 2) + i
        if sAS[k][0] > 1:
            for a in range(sAS[k][0] - 1):
                i1 = sAS[k][1][a][0]
                j1 = sAS[k][1][a][1]
                if math.ceil(j1 * (j1 - 1) / 2) + i1 < n:
                    i = i1
                    j = j1

        if i not in V: V.append(i)
        if j not in V: V.append(j)

    for k in wAS.keys():
        i = wAS[k][1][0][0]
        j = wAS[k][1][0][1]
        n = math.ceil(j * (j - 1) / 2) + i
        if wAS[k][0] > 1:
            for a in range(wAS[k][0] - 1):
                i1 = wAS[k][1][a][0]
                j1 = wAS[k][1][a][1]
                if math.ceil(j1 * (j1 - 1) / 2) + i1 < n:
                    i = i1
                    j = j1

        if i not in V: V.append(i)
        if j not in V: V.append(j)

    if ToDebug: print("SEQUENCE: {} vertexes left: {}".format(len(V), sorted(V)))

    return sorted(V)

def AgreeSetOccurence(sAS, wAS):
    """
    :param sAS: Strong agree sets occurence
    :param wAS: Weak agree sets occurence
    :return: Vertexes list
    """

    V = []
    ASList = []
    AWList = []
    ## For agree sets only appear once
    for k in sAS.keys():
        if sAS[k][0] == 1:
            i = sAS[k][1][0][0]
            j = sAS[k][1][0][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)
            ASList.append(k)

    for k in wAS.keys():
        if wAS[k][0] == 1:
            i = wAS[k][1][0][0]
            j = wAS[k][1][0][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)
            AWList.append(k)

    ## Double assigned edges are preferable
    frequency = {}
    for k in AgSDict.keys():
        if AgSDict[k][0] in ASList and len(AgSDict[k][1]) > 0: ## if the AS is in the graph, add the AW on same edge
            if AgSDict[k][1] not in AWList: AWList.append(AgSDict[k][1])
        elif AgSDict[k][1] in AWList and len(AgSDict[k][0]) > 0: ## if the AW is in the graph, add the AS on same edge
            if AgSDict[k][0] not in ASList: ASList.append(AgSDict[k][0])
        ## Start from less frequent agree sets
        elif len(AgSDict[k][0]) > 0 and len(AgSDict[k][1]) > 0 and AgSDict[k][0] not in ASList and AgSDict[k][1] not in AWList:
            if tuple(AgSDict[k]) in frequency.keys():
                if sAS[AgSDict[k][0]][0] + wAS[AgSDict[k][1]][0] < frequency[tuple(AgSDict[k])][0]:
                    frequency[tuple(AgSDict[k])][0] = sAS[AgSDict[k][0]][0] + wAS[AgSDict[k][1]][0]
                    frequency[tuple(AgSDict[k])][1] = k
            else:
                frequency[tuple(AgSDict[k])] = [sAS[AgSDict[k][0]][0] + wAS[AgSDict[k][1]][0], k]

    for dAssign in frequency.keys():
        if dAssign[0] not in ASList and dAssign[1] not in AWList:
            if frequency[dAssign][1][0] not in V: V.append(frequency[dAssign][1][0])
            if frequency[dAssign][1][1] not in V: V.append(frequency[dAssign][1][1])

            ASList.append(dAssign[0])
            AWList.append(dAssign[1])

    ## For the rest: less frequent agree sets are preferable still
    sAS = dict(sorted(sAS.items(), key=lambda x:x[1]))
    for k in sAS.keys():
        if k not in ASList:
            n = -1
            for a in range(sAS[k][0]):
                ## Both vertexes already in graph
                if sAS[k][1][a][0] in V and sAS[k][1][a][1] in V:
                    i = sAS[k][1][a][0]
                    j = sAS[k][1][a][1]
                    n = math.ceil(j * (j - 1) / 2) + i
                    break
                ## Only one vertex in graph
                elif sAS[k][1][a][0] in V or sAS[k][1][a][1] in V:
                    i = sAS[k][1][a][0]
                    j = sAS[k][1][a][1]
                    n = math.ceil(j * (j - 1) / 2) + i

            ## None of vertexes in graph, randomly pick one
            if n == -1:
                r = random.randrange(sAS[k][0])
                i = sAS[k][1][0][0]
                j = sAS[k][1][0][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)

    wAS = dict(sorted(wAS.items(), key=lambda x:x[1]))
    for k in wAS.keys():
        if k not in AWList:
            n = -1
            for a in range(wAS[k][0]):
                ## Both vertexes already in graph
                if wAS[k][1][a][0] in V and wAS[k][1][a][1] in V:
                    i = wAS[k][1][a][0]
                    j = wAS[k][1][a][1]
                    n = math.ceil(j * (j - 1) / 2) + i
                    break
                ## Only one vertex in graph
                elif wAS[k][1][a][0] in V or wAS[k][1][a][1] in V:
                    i = wAS[k][1][a][0]
                    j = wAS[k][1][a][1]
                    n = math.ceil(j * (j - 1) / 2) + i

            ## None of vertexes in graph, randomly pick one
            if n == -1:
                r = random.randrange(wAS[k][0])
                i = wAS[k][1][r][0]
                j = wAS[k][1][r][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)

    if ToDebug: print("Agree Set Occurence: {} vertexes left: {}".format(len(V), sorted(V)))

    return sorted(V)

def AdjacentEdge(sAS, wAS):
    """
    :param sAS: Strong agree sets occurence
    :param wAS: Weak agree sets occurence
    :return: Vertexes list
    """
    ToDebug = 0   # Flag to print for debugging

    VDict = {}
    for k in sAS.keys():
        for a in range(sAS[k][0]):
            if sAS[k][1][a][0] not in VDict.keys():
                VDict[sAS[k][1][a][0]] = [[k], []]
            elif k not in VDict[sAS[k][1][a][0]][0]:
                VDict[sAS[k][1][a][0]][0].append(k)

            if sAS[k][1][a][1] not in VDict.keys():
                VDict[sAS[k][1][a][1]] = [[k], []]
            elif k not in VDict[sAS[k][1][a][1]][0]:
                VDict[sAS[k][1][a][1]][0].append(k)

    for k in wAS.keys():
        for a in range(wAS[k][0]):
            if wAS[k][1][a][0] not in VDict.keys():
                VDict[wAS[k][1][a][0]] = [[], [k]]
            elif k not in VDict[wAS[k][1][a][0]][1]:
                VDict[wAS[k][1][a][0]][1].append(k)

            if wAS[k][1][a][1] not in VDict.keys():
                VDict[wAS[k][1][a][1]] = [[], [k]]
            elif k not in VDict[wAS[k][1][a][1]][1]:
                VDict[wAS[k][1][a][1]][1].append(k)
    if ToDebug: print("VDict:", VDict)

    V = []
    ASList = []
    AWList = []
    ## For agree sets only appear once
    for k in sAS.keys():
        if sAS[k][0] == 1:
            i = sAS[k][1][0][0]
            j = sAS[k][1][0][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)
            ASList.append(k)

    for k in wAS.keys():
        if wAS[k][0] == 1:
            i = wAS[k][1][0][0]
            j = wAS[k][1][0][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)
            AWList.append(k)

    ## Check for double assgined edges
    for k in AgSDict.keys():
        if AgSDict[k][0] in ASList and len(AgSDict[k][1]) > 0: ## if the AS is in the graph, add the AW on same edge
            AWList.append(AgSDict[k][1])
        elif AgSDict[k][1] in AWList and len(AgSDict[k][0]) > 0: ## if the AW is in the graph, add the AS on same edge
            ASList.append(AgSDict[k][0])

    ## For agree sets appear more than once
    for k in sAS.keys():
        if k not in ASList:
            r = -1
            for a in range(sAS[k][0]):
                ## Both vertexes already in graph
                if sAS[k][1][a][0] in V and sAS[k][1][a][1] in V:
                    i1 = sAS[k][1][a][0]
                    j1 = sAS[k][1][a][1]
                    if max(len(VDict[i1][0]), len(VDict[j1][0])) > r:
                        i = i1
                        j = j1
                        r = max(len(VDict[i][0]), len(VDict[j][0]))
                ## Only one vertex in graph
                elif sAS[k][1][a][0] in V or sAS[k][1][a][1] in V:
                    i1 = sAS[k][1][a][0]
                    j1 = sAS[k][1][a][1]
                    if max(len(VDict[i1][0]), len(VDict[j1][0])) > r:
                        i = i1
                        j = j1
                        r = max(len(VDict[i][0]), len(VDict[j][0]))

            ## None of vertexes in graph, randomly pick one
            if r == -1:
                n = random.randrange(sAS[k][0])
                i = sAS[k][1][n][0]
                j = sAS[k][1][n][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)
            ASList.append(k)

    for k in wAS.keys():
        if k not in AWList:
            r = -1
            for a in range(wAS[k][0]):
                ## Both vertexes already in graph
                if wAS[k][1][a][0] in V and wAS[k][1][a][1] in V:
                    i1 = wAS[k][1][a][0]
                    j1 = wAS[k][1][a][1]
                    if max(len(VDict[i1][1]), len(VDict[j1][1])) > r:
                        i = i1
                        j = j1
                        r = max(len(VDict[i][1]), len(VDict[j][1]))
                ## Only one vertex in graph
                elif wAS[k][1][a][0] in V or wAS[k][1][a][1] in V:
                    i1 = wAS[k][1][a][0]
                    j1 = wAS[k][1][a][1]
                    if max(len(VDict[i1][1]), len(VDict[j1][1])) > r:
                        i = i1
                        j = j1
                        r = max(len(VDict[i][1]), len(VDict[j][1]))

                ## None of vertexes in graph, randomly pick one
            if r == -1:
                n = random.randrange(wAS[k][0])
                i = wAS[k][1][n][0]
                j = wAS[k][1][n][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)
            AWList.append(k)

    if ToDebug: print("Adjacent edge: {} vertexes left: {}".format(len(V), sorted(V)))

    return sorted(V)

def EdgeRank(sAS, wAS):
    """
    :param sAS: Strong agree sets occurence
    :param wAS: Weak agree sets occurence
    :return: Vertexes list
    """
    ToDebug = 0   # Flag to print for debugging

    VDict = {}
    for k in sAS.keys():
        for a in range(sAS[k][0]):
            if sAS[k][1][a][0] not in VDict.keys():
                VDict[sAS[k][1][a][0]] = [[k], []]
            elif k not in VDict[sAS[k][1][a][0]][0]:
                VDict[sAS[k][1][a][0]][0].append(k)

            if sAS[k][1][a][1] not in VDict.keys():
                VDict[sAS[k][1][a][1]] = [[k], []]
            elif k not in VDict[sAS[k][1][a][1]][0]:
                VDict[sAS[k][1][a][1]][0].append(k)

    for k in wAS.keys():
        for a in range(wAS[k][0]):
            if wAS[k][1][a][0] not in VDict.keys():
                VDict[wAS[k][1][a][0]] = [[], [k]]
            elif k not in VDict[wAS[k][1][a][0]][1]:
                VDict[wAS[k][1][a][0]][1].append(k)

            if wAS[k][1][a][1] not in VDict.keys():
                VDict[wAS[k][1][a][1]] = [[], [k]]
            elif k not in VDict[wAS[k][1][a][1]][1]:
                VDict[wAS[k][1][a][1]][1].append(k)
    if ToDebug: print("VDict:", VDict)

    V = []
    ASList = []
    AWList = []
    ## For agree sets only appear once
    for k in sAS.keys():
        if sAS[k][0] == 1:
            i = sAS[k][1][0][0]
            j = sAS[k][1][0][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)
            ASList.append(k)

    for k in wAS.keys():
        if wAS[k][0] == 1:
            i = wAS[k][1][0][0]
            j = wAS[k][1][0][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)
            AWList.append(k)

    ## Check for double assgined edges
    for k in AgSDict.keys():
        if AgSDict[k][0] in ASList and len(AgSDict[k][1]) > 0: ## if the AS is in the graph, add the AW on same edge
            AWList.append(AgSDict[k][1])
        elif AgSDict[k][1] in AWList and len(AgSDict[k][0]) > 0: ## if the AW is in the graph, add the AS on same edge
            ASList.append(AgSDict[k][0])

    ## For agree sets appear more than once
    weight = (len(VDict) + sum(sAS[item][0] for item in sAS) + sum(wAS[item][0] for item in wAS)) * 10
    for k in sAS.keys():
        if k not in ASList:
            r = -1
            for a in range(sAS[k][0]):
                ## Both vertexes already in graph
                if sAS[k][1][a][0] in V and sAS[k][1][a][1] in V:
                    i1 = sAS[k][1][a][0]
                    j1 = sAS[k][1][a][1]
                    if max(len(VDict[i1][0]), len(VDict[j1][0])) + weight * 2  > r:
                        i = i1
                        j = j1
                        r = max(len(VDict[i][0]), len(VDict[j][0])) + weight * 2
                ## Only one vertex in graph
                elif sAS[k][1][a][0] in V or sAS[k][1][a][1] in V:
                    i1 = sAS[k][1][a][0]
                    j1 = sAS[k][1][a][1]
                    if max(len(VDict[i1][0]), len(VDict[j1][0])) + weight > r:
                        i = i1
                        j = j1
                        r = max(len(VDict[i][0]), len(VDict[j][0])) + weight
                ## None of vertexes in graph
                else:
                    i1 = sAS[k][1][a][0]
                    j1 = sAS[k][1][a][1]
                    if max(len(VDict[i1][0]), len(VDict[j1][0])) > r:
                        i = i1
                        j = j1
                        r = max(len(VDict[i][0]), len(VDict[j][0]))

            if i not in V: V.append(i)
            if j not in V: V.append(j)
            ASList.append(k)

    for k in wAS.keys():
        if k not in AWList:
            r = -1
            for a in range(wAS[k][0]):
                ## Both vertexes already in graph
                if wAS[k][1][a][0] in V and wAS[k][1][a][1] in V:
                    i1 = wAS[k][1][a][0]
                    j1 = wAS[k][1][a][1]
                    if max(len(VDict[i1][1]), len(VDict[j1][1])) + weight * 2  > r:
                        i = i1
                        j = j1
                        r = max(len(VDict[i][1]), len(VDict[j][1])) + weight * 2
                ## Only one vertex in graph
                elif wAS[k][1][a][0] in V or wAS[k][1][a][1] in V:
                    i1 = wAS[k][1][a][0]
                    j1 = wAS[k][1][a][1]
                    if max(len(VDict[i1][1]), len(VDict[j1][1])) + weight > r:
                        i = i1
                        j = j1
                        r = max(len(VDict[i][1]), len(VDict[j][1])) + weight
                ## None of vertexes in graph
                else:
                    i1 = wAS[k][1][a][0]
                    j1 = wAS[k][1][a][1]
                    if max(len(VDict[i1][1]), len(VDict[j1][1])) > r:
                        i = i1
                        j = j1
                        r = max(len(VDict[i][1]), len(VDict[j][1]))

            if i not in V: V.append(i)
            if j not in V: V.append(j)
            AWList.append(k)

    if ToDebug: print("Edge rank: {} vertexes left: {}".format(len(V), sorted(V)))

    return sorted(V)

def ExpandVertexWise(sAS, wAS, m):
    """
    :param sAS: Strong agree sets occurence
    :param wAS: Weak agree sets occurence
    :param m: Metric number
    :return: Vertexes list
    """
    ToDebug = 0   # Flag to print for debugging

    if ToDebug:
        print("sAS(", len(sAS), "):", sAS)
        print("wAS(", len(wAS), "):", wAS)
    VDict = {} ## {V: [sAS and wAS], [sV and wV]}
    for k in sAS.keys():
        for a in range(sAS[k][0]):
            if sAS[k][1][a][0] not in VDict.keys():
                VDict[sAS[k][1][a][0]] = [[k], [sAS[k][1][a][1]]]
            elif k not in VDict[sAS[k][1][a][0]][0]:
                VDict[sAS[k][1][a][0]][0].append(k)
                VDict[sAS[k][1][a][0]][1].append(sAS[k][1][a][1])

            if sAS[k][1][a][1] not in VDict.keys():
                VDict[sAS[k][1][a][1]] = [[k], [sAS[k][1][a][0]]]
            elif k not in VDict[sAS[k][1][a][1]][0]:
                VDict[sAS[k][1][a][1]][0].append(k)
                VDict[sAS[k][1][a][1]][1].append(sAS[k][1][a][0])

    for k in wAS.keys():
        for a in range(wAS[k][0]):
            if wAS[k][1][a][0] not in VDict.keys():
                VDict[wAS[k][1][a][0]] = [[k], [wAS[k][1][a][1]]]
            elif k not in VDict[wAS[k][1][a][0]][0]:
                VDict[wAS[k][1][a][0]][0].append(k)
                VDict[wAS[k][1][a][0]][1].append(wAS[k][1][a][1])

            if wAS[k][1][a][1] not in VDict.keys():
                VDict[wAS[k][1][a][1]] = [[k], [wAS[k][1][a][0]]]
            elif k not in VDict[wAS[k][1][a][1]][0]:
                VDict[wAS[k][1][a][1]][0].append(k)
                VDict[wAS[k][1][a][1]][1].append(wAS[k][1][a][0])
    if ToDebug: print("VDict(", len(VDict), "):", VDict)

    V = []
    AgSList = []
    ## For agree sets only appear once
    for k in sAS.keys():
        if sAS[k][0] == 1:
            i = sAS[k][1][0][0]
            j = sAS[k][1][0][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)
            if k not in AgSList: AgSList.append(k)

    for k in wAS.keys():
        if wAS[k][0] == 1:
            i = wAS[k][1][0][0]
            j = wAS[k][1][0][1]

            if i not in V: V.append(i)
            if j not in V: V.append(j)
            if k not in AgSList: AgSList.append(k)

    ## Check for double assgined edges
    dBonus = {}
    for k in AgSDict.keys():
        if AgSDict[k][0] in AgSList and len(AgSDict[k][1]) > 0: ## if the AS is in the graph, add the AW on same edge
            if AgSDict[k][1] not in AgSList: AgSList.append(AgSDict[k][1])
        elif AgSDict[k][1] in AgSList and len(AgSDict[k][0]) > 0: ## if the AW is in the graph, add the AS on same edge
            if AgSDict[k][0] not in AgSList: AgSList.append(AgSDict[k][0])

        if len(AgSDict[k][0]) > 0 and len(AgSDict[k][1]) > 0:
            if k[0] not in dBonus.keys():
                dBonus[k[0]] = 1
            else:
                dBonus[k[0]] += 1
            if k[1] not in dBonus.keys():
                dBonus[k[1]] = 1
            else:
                dBonus[k[1]] += 1

    weight = (len(VDict) + sum(sAS[item][0] for item in sAS) + sum(wAS[item][0] for item in wAS)) * 10
    DupList = [item for item in list(sAS.keys()) + list(wAS.keys())]
    vRank = vGroup(VDict)
    if ToDebug: print("DupList:", len(DupList), "AgSList:", len(AgSList), AgSList)

    candidate = [item for item in list(VDict.keys()) if item not in V]
    if ToDebug: print("candidate(", len(candidate), "):", candidate)

    metric = {}
    mFactors = {}
    for i in range(len(candidate)):
        fCover = [[], [], [], []] ##[[Distincdt AS], [Occurence], [Duplicate AS], [Occurence]]
        hCover = [[], [], [], []]
        for j in range(len(VDict[candidate[i]][0])):
            if VDict[candidate[i]][0][j] not in AgSList: ## Uncovered agree sets only
                if VDict[candidate[i]][1][j] in V:
                    if VDict[candidate[i]][0][j] not in fCover[0]:
                        fCover[0].append(VDict[candidate[i]][0][j])
                        if VDict[candidate[i]][0][j] in sAS.keys():
                            fCover[1].append(sAS[VDict[candidate[i]][0][j]][0]) ## Occurence of strong AS
                        else:
                            fCover[1].append(wAS[VDict[candidate[i]][0][j]][0])  ## Occurence of weak AS
                    else: ## Duplicate AS
                        fCover[2].append(VDict[candidate[i]][0][j])
                        if VDict[candidate[i]][0][j] in sAS.keys():
                            fCover[3].append(sAS[VDict[candidate[i]][0][j]][0]) ## Occurence of strong AS
                        else:
                            fCover[3].append(wAS[VDict[candidate[i]][0][j]][0])  ## Occurence of weak AS
                else:
                    if VDict[candidate[i]][0][j] not in hCover[0]:
                        hCover[0].append(VDict[candidate[i]][0][j])
                        if VDict[candidate[i]][0][j] in sAS.keys():
                            hCover[1].append(sAS[VDict[candidate[i]][0][j]][0]) ## Occurence of strong AS
                        else:
                            hCover[1].append(wAS[VDict[candidate[i]][0][j]][0])  ## Occurence of weak AS
                    else: ## Duplicate AS
                        hCover[2].append(VDict[candidate[i]][0][j])
                        if VDict[candidate[i]][0][j] in sAS.keys():
                            hCover[3].append(sAS[VDict[candidate[i]][0][j]][0]) ## Occurence of strong AS
                        else:
                            hCover[3].append(wAS[VDict[candidate[i]][0][j]][0])  ## Occurence of weak AS

        mFactors[candidate[i]] = [fCover, hCover]
        metric[candidate[i]] = GetMetrics(m, candidate[i], mFactors[candidate[i]], vRank, dBonus, weight)

    while len([item for item in DupList if item not in AgSList]) > 0:
        if ToDebug: print("AS left (", len(DupList) - len(AgSList), "):", [item for item in DupList if item not in AgSList])

        candidate = [item for item in list(VDict.keys()) if item not in V and item in list(metric.keys())]
        if ToDebug: print("candidate(", len(candidate), "):", candidate)
        if ToDebug: print("metric(", len(metric), "):", metric)
        if len(metric) > 0:
            s_metric = {k: v for k, v in sorted(metric.items(), key=lambda item: item[1][1], reverse=True)}
            maxL = s_metric[list(s_metric.keys())[0]][1]
            pool = [item for item in s_metric.keys() if s_metric[item][1] == maxL]
            chosenV = random.choice(pool)
            if ToDebug: print("Max L:", maxL, "max metric pool:", pool, "chosenV: ", chosenV, "AS to add:", metric[chosenV][0])
            if chosenV not in V: V.append(chosenV)
            for i in range(len(metric[chosenV][0])):
                if metric[chosenV][0][i] not in AgSList:
                    AgSList.append(metric[chosenV][0][i])

            ## Half covered to fully covered AS
            vToRemove = {}
            for f in range(len(mFactors[chosenV][0][0])):
                vToRemove[mFactors[chosenV][0][0][f]] = []
                if mFactors[chosenV][0][0][f] in sAS.keys():
                    vToRemove[mFactors[chosenV][0][0][f]] += list(set(sum(sAS[mFactors[chosenV][0][0][f]][1], ())))
                elif mFactors[chosenV][0][0][f] in wAS.keys():
                    vToRemove[mFactors[chosenV][0][0][f]] += list(set(sum(wAS[mFactors[chosenV][0][0][f]][1], ())))
                vToRemove[mFactors[chosenV][0][0][f]] = [item for item in vToRemove[mFactors[chosenV][0][0][f]] if item not in V]
            if ToDebug: print("Half covered to fully covered: vertexes to remove", vToRemove)

            for dAS in vToRemove.keys():
                for g in range(len(vToRemove[dAS])):
                    if vToRemove[dAS][g] in VDict.keys() and vToRemove[dAS][g] in mFactors.keys():
                        if dAS in mFactors[vToRemove[dAS][g]][0][0]:
                            idx1 = mFactors[vToRemove[dAS][g]][0][0].index(dAS)
                            del mFactors[vToRemove[dAS][g]][0][0][idx1]
                            del mFactors[vToRemove[dAS][g]][0][1][idx1]
                        elif dAS in mFactors[vToRemove[dAS][g]][0][2]:
                            idx2 = mFactors[vToRemove[dAS][g]][0][2].index(dAS)
                            del mFactors[vToRemove[dAS][g]][0][2][idx2]
                            del mFactors[vToRemove[dAS][g]][0][3][idx2]
                        elif dAS in mFactors[vToRemove[dAS][g]][1][0]:
                            idx3 = mFactors[vToRemove[dAS][g]][1][0].index(dAS)
                            del mFactors[vToRemove[dAS][g]][1][0][idx3]
                            del mFactors[vToRemove[dAS][g]][1][1][idx3]
                        elif dAS in mFactors[vToRemove[dAS][g]][1][2]:
                            idx4 = mFactors[vToRemove[dAS][g]][1][2].index(dAS)
                            del mFactors[vToRemove[dAS][g]][1][2][idx4]
                            del mFactors[vToRemove[dAS][g]][1][3][idx4]
                    vToDel = {key:value for (key, value) in mFactors.items() if len(sum(value[0], []) + sum(value[1], [])) == 0}

            ## Uncovered to half covered AS
            vToMove = {}
            for h in range(len(mFactors[chosenV][1][0])):
                vToMove[mFactors[chosenV][1][0][h]] = []
                idxL = [idx for idx, value in enumerate(VDict[chosenV][0]) if value == mFactors[chosenV][1][0][h]]
                for otherV in range(len(idxL)):
                    vToMove[mFactors[chosenV][1][0][h]].append(VDict[chosenV][1][idxL[otherV]])
            if ToDebug: print("Uncovered to half covered: vertexes to move", vToMove)

            for mAS in vToMove.keys():
                for vi in range(len(vToMove[mAS])):
                    if mAS in mFactors[vToMove[mAS][vi]][1][0]:
                        idx5 = mFactors[vToMove[mAS][vi]][1][0].index(mAS)
                        fOccur = mFactors[vToMove[mAS][vi]][1][1][idx5]

                        mFactors[vToMove[mAS][vi]][0][0].append(mAS)
                        mFactors[vToMove[mAS][vi]][0][1].append(fOccur)
                        del mFactors[vToMove[mAS][vi]][1][0][idx5]
                        del mFactors[vToMove[mAS][vi]][1][1][idx5]

                        if mAS in mFactors[vToMove[mAS][vi]][1][2]:
                            dupCount = mFactors[vToMove[mAS][vi]][1][2].count(mAS)
                            idx6 = [idx for idx, value in enumerate(mFactors[vToMove[mAS][vi]][1][2]) if value == mAS]
                            for c in range(len(dupCount)):
                                mFactors[vToMove[mAS][vi]][0][2].append(mAS)
                                mFactors[vToMove[mAS][vi]][0][3].append(fOccur)
                                del mFactors[vToMove[mAS][vi]][1][2][idx6[c]]
                                del mFactors[vToMove[mAS][vi]][1][3][idx6[c]]

            del mFactors[chosenV]
            del metric[chosenV]
            for v2d in vToDel.keys():
                if v2d in mFactors.keys(): del mFactors[v2d]
                if v2d in metric.keys():del metric[v2d]

                for l in range(len(vRank)):
                    if v2d in vRank[l]:
                        vRank[l].remove(v2d)

            ToUpdate = sum(vToRemove.values(), []) + sum(vToMove.values(), [])
            for ul in range(len(ToUpdate)):
                if ToUpdate[ul] in metric.keys():
                    metric[ToUpdate[ul]] = GetMetrics(m, ToUpdate[ul], mFactors[ToUpdate[ul]], vRank, dBonus, weight)
        else:
            reList = [item for item in DupList if item not in AgSList]
            for iAS in range(len(reList)):
                if reList[iAS] in sAS.keys():
                    r = random.randint(0, sAS[reList[iAS]][0] - 1)
                    if sAS[reList[iAS]][1][r][0] not in V: V.append(sAS[reList[iAS]][1][r][0])
                    if sAS[reList[iAS]][1][r][1] not in V: V.append(sAS[reList[iAS]][1][r][1])
                elif reList[iAS] in wAS.keys():
                    r = random.randint(0, wAS[reList[iAS]][0] - 1)
                    if wAS[reList[iAS]][1][r][0] not in V: V.append(wAS[reList[iAS]][1][r][0])
                    if wAS[reList[iAS]][1][r][1] not in V: V.append(wAS[reList[iAS]][1][r][1])
            break
    if ToDebug: print("Expand Vertex Wise: {} vertexes left: {}".format(len(V), sorted(V)))

    return sorted(V)


m = 0 ## metric number: 1 - O; 2 - O ** 2; 3 - sqrt(O)
source = 'Hockey.Goalies'
path1 = "/Users/wye1/Documents/Armstrong/DataSets/Hockey/"
path2 = "/Users/wye1/Documents/Armstrong/DataSets/Hocky_Parameters/"
path_out = "/Users/wye1/Documents/Experiments/9-Informative+Null/Output/"
#pa1 = "D:/Wendy/Armstrong/DataSets/naumann_small/"
ATFile = path1 + source + '.csv'

rCounter = 1
if rCounter > 1:
    OutFile = path_out + source + ".txt"
else:
    OutFile = path_out + source + "_result.txt"

# Main
if __name__ == "__main__":
    ToDebug = 1   # Flag to print for debugging

    Start = datetime.datetime.now()

    FileName = path2 + source # + '.main'
    para = Function4Null.FindParameters(FileName)
    R = para[1]
    StrongAS = para[2]
    WeakAS = para[3]
    W = para[6]

    result = InitFromAsAw_main.InitGraph(ATFile, StrongAS, WeakAS, W)
    AgSDict = result[4]
    V = result[5]

    WeakAS = [item for item in WeakAS if item not in StrongAS]
    if ToDebug:
        print('R', R)
        print('StrongAS', StrongAS)
        print('WeakAS', WeakAS)
        print('W', W)
        print('AgSDict (', len(AgSDict), '):')#, AgSDict)

    sAS = {}
    for i in range(len(StrongAS)):
        sAS[StrongAS[i]] = [0, []]
    wAS = {}
    for j in range(len(WeakAS)):
        wAS[WeakAS[j]] = [0, []]

    for k in AgSDict.keys():
        if AgSDict[k][0] in sAS.keys():
            sAS[AgSDict[k][0]][0] += 1
            sAS[AgSDict[k][0]][1].append(k)

        if AgSDict[k][1] in wAS.keys():
            wAS[AgSDict[k][1]][0] += 1
            wAS[AgSDict[k][1]][1].append(k)

    if ToDebug:
        print("sAS (", len(sAS), ")") #, sAS)
        print("wAS (", len(wAS), ")") #, wAS)

    initV = sorted(V.keys())
    print("Initial Graph has", len(initV), "vertexes")#, ":", initV)

    Start1  = datetime.datetime.now()
    copy_sAS = copy.deepcopy(sAS)
    copy_wAS = copy.deepcopy(wAS)
    copy_V = copy.deepcopy(V)
    V1 = Sequence(copy_sAS, copy_wAS)
    fV1 = ExtraCheck(V, V1, W)
    print("Size for Sequence: ", len(fV1))
    End1 = datetime.datetime.now()
    print("Runs for: ", End1 - Start1)

    Start2  = datetime.datetime.now()
    aV2 = 0
    for i in range(rCounter):
        copy_sAS = copy.deepcopy(sAS)
        copy_wAS = copy.deepcopy(wAS)
        V2 = AgreeSetOccurence(copy_sAS, copy_wAS)
        fV2 = ExtraCheck(V, V2, W)
        aV2 += len(fV2)
    print("Average size for AS Occurence:", aV2 / rCounter)
    End2 = datetime.datetime.now()
    print("Runs for: ", End2 - Start2)

    Start3  = datetime.datetime.now()
    aV3 = 0
    for i in range(rCounter):
        copy_sAS = copy.deepcopy(sAS)
        copy_wAS = copy.deepcopy(wAS)
        V3 = AdjacentEdge(copy_sAS, copy_wAS)
        fV3 = ExtraCheck(V, V3, W)
        aV3 += len(fV3)
    print("Average size for Adjacent Edge:", aV3 / rCounter)
    End3 = datetime.datetime.now()
    print("Runs for: ", End3 - Start3)

    Start5  = datetime.datetime.now()
    copy_sAS = copy.deepcopy(sAS)
    copy_wAS = copy.deepcopy(wAS)
    V5 = EdgeRank(copy_sAS, copy_wAS)
    fV5 = ExtraCheck(V, V5, W)
    print("Size for Edge Rank: ", len(fV5))
    End5 = datetime.datetime.now()
    print("Runs for: ", End5 - Start5)

    Start4  = datetime.datetime.now()
    aV4 = 0
    for i in range(rCounter):
        copy_sAS = copy.deepcopy(sAS)
        copy_wAS = copy.deepcopy(wAS)
        V4 = ExpandVertexWise(copy_sAS, copy_wAS, 0)
        fV4 = ExtraCheck(V, V4, W)
        aV4 += len(fV4)
    print("Average size for Expand Vertex Wise (metric 0):", aV4 / rCounter)
    End4 = datetime.datetime.now()
    print("Runs for: ", End4 - Start4)

    Start6  = datetime.datetime.now()
    aV6 = 0
    for i in range(rCounter):
        copy_sAS = copy.deepcopy(sAS)
        copy_wAS = copy.deepcopy(wAS)
        V6 = ExpandVertexWise(copy_sAS, copy_wAS, 1)
        fV6 = ExtraCheck(V, V6, W)
        aV6 += len(fV6)
    print("Average size for Expand Vertex Wise (metric 1):", aV6 / rCounter)
    End6 = datetime.datetime.now()
    print("Runs for: ", End6 - Start6)

    Start7  = datetime.datetime.now()
    aV7 = 0
    for i in range(rCounter):
        copy_sAS = copy.deepcopy(sAS)
        copy_wAS = copy.deepcopy(wAS)
        V7 = ExpandVertexWise(copy_sAS, copy_wAS, 2)
        fV7 = ExtraCheck(V, V7, W)
        aV7 += len(fV7)
    print("Average size for Expand Vertex Wise (metric 2):", aV7 / rCounter)
    End7 = datetime.datetime.now()
    print("Runs for: ", End7 - Start7)

    Start8  = datetime.datetime.now()
    aV8 = 0
    for i in range(rCounter):
        copy_sAS = copy.deepcopy(sAS)
        copy_wAS = copy.deepcopy(wAS)
        V8 = ExpandVertexWise(copy_sAS, copy_wAS, 3)
        fV8 = ExtraCheck(V, V8, W)
        aV8 += len(fV8)
    print("Average size for Expand Vertex Wise (metric 3):", aV8 / rCounter)
    End8 = datetime.datetime.now()
    print("Runs for: ", End8 - Start8)

    End = datetime.datetime.now()
    print("Total time of running: {}".format(End - Start))

