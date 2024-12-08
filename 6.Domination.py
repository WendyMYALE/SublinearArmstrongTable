## Domination check through vertexes + Weighted Vertex Rank
import datetime
import copy
import random
import itertools

import FunctionSet
import ATMining
import InitFromKey

def KeyVCheck(AgSi):
    ## Key vertexes for given agree set
    c = [AgSi[1][0][0], AgSi[1][0][1]]
    for i in range(AgSi[0] - 1):
        c = [value for value in c if value in AgSi[1][i + 1]]

    return c

def DomCheck(Vx, Vy, OpVDict, V):
    """
    :param Vx: Vertex to check
    :param Vy: Vertex to check against
    :param OpVDict: Vertexes dictionary
    :param V: Forced list
    :return: Vertex pair (Dominating V, Dominated V) or empty tuple (dominated each other)
    """
    p = 0   # Flag to print for debugging

    if OpVDict[Vx]["len"] > OpVDict[Vy]["len"]:
        Vx, Vy = Vy, Vx

    if FunctionSet.Subeq(OpVDict[Vx]["edges"], OpVDict[Vy]["edges"]):
        if p: print("{}: {} is subset of {}: {}".format(Vx, OpVDict[Vx], Vy, OpVDict[Vy]))
        if Vy in OpVDict[Vx]["conn"]:
            if p: print("{} and {} are connected".format(Vx, Vy))
            DomPair = ()
        else:
            Px = {}
            Py = {}
            Cx = {}
            Cy = {}
            for a in range(OpVDict[Vx]["len"]):
                if OpVDict[Vx]["conn"][a] in V:
                    Cx[OpVDict[Vx]["conn"][a]] = OpVDict[Vx]["edges"][a]
                Px[OpVDict[Vx]["conn"][a]] = OpVDict[Vx]["edges"][a]
            for b in range(OpVDict[Vy]["len"]):
                if OpVDict[Vy]["conn"][b] in V:
                    Cy[OpVDict[Vy]["conn"][b]] = OpVDict[Vy]["edges"][b]
                Py[OpVDict[Vy]["conn"][b]] = OpVDict[Vy]["edges"][b]

            ## Case A - Y dominates X
            if FunctionSet.Subeq(list(Px.values()), list(Cy.values())) and len(Px) > 0 and len(Cy) > 0 and Vx not in V:
                if p:
                    print("{} is dominated by {}.".format(Vx, Vy))
                    print("{} - Certain ({}): {}, Possible ({}): {}".format(Vx, len(Cx), Cx, len(Px), Px))
                    print("{} - Certain ({}): {}; Possible ({}): {}".format(Vy, len(Cy), Cy, len(Py), Py))
                DomPair = (Vy, Vx)
            ## Case A - X dominates Y
            elif FunctionSet.Subeq(list(Py.values()), list(Cx.values())) and len(Py) > 0 and len(Cx) > 0 and Vy not in V:
                if p:
                    print("{} dominates {}.".format(Vx, Vy))
                    print("{} - Certain ({}): {}, Possible ({}): {}".format(Vx, len(Cx), Cx, len(Px), Px))
                    print("{} - Certain ({}): {}; Possible ({}): {}".format(Vy, len(Cy), Cy, len(Py), Py))
                DomPair = (Vx, Vy)
            ## Case B
            elif len(set(Px.keys()) & set(Py.keys())) > 0:
                d = list(set(Px.keys()) & set(Py.keys()))
                if p: print("Common neighbor(s): {}".format(d))
                for m in range(len(d)):
                    if Px[d[m]] == Py[d[m]]:
                        del Px[d[m]]
                        del Py[d[m]]
                if FunctionSet.Subeq(list(Px.values()), list(Cy.values())) and len(Px) > 0 and len(Cy) > 0 and Vx not in V:
                    if p:
                        print("{} is dominated by {}.".format(Vx, Vy))
                        print("{} - Certain updated ({}): {}, Possible updated ({}): {}".format(Vx, len(Cx), Cx, len(Px), Px))
                        print("{} - Certain updated ({}): {}, Possible updated ({}): {}".format(Vy, len(Cy), Cy, len(Py), Py))
                    DomPair = (Vy, Vx)
                elif FunctionSet.Subeq(list(Py.values()), list(Cx.values())) and len(Py) > 0 and len(Cx) > 0 and Vx not in V:
                    if p:
                        print("{} dominates {}.".format(Vx, Vy))
                        print("{} - Certain updated ({}): {}, Possible updated ({}): {}".format(Vx, len(Cx), Cx, len(Px), Px))
                        print("{} - Certain updated ({}): {}, Possible updated ({}): {}".format(Vy, len(Cy), Cy, len(Py), Py))
                    DomPair = (Vx, Vy)
                else:
                    if p: print("{} and {} dominate each other.".format(Vx, Vy))
                    DomPair = ()
            else:
                if p:
                    print("{} and {} dominate each other.".format(Vx, Vy))
                    print("{} - Certain updated ({}): {}, Possible updated ({}): {}".format(Vx, len(Cx), Cx, len(Px), Px))
                    print("{} - Certain updated ({}): {}, Possible updated ({}): {}".format(Vy, len(Cy), Cy, len(Py), Py))
                DomPair = ()
    else:
        if p: print("{} and {} dominate each other.".format(Vx, Vy))
        DomPair = ()

    return DomPair

def HaurPick(candidateV, V, OpVDict):
    """
    :param candidateV: Candidates of vertex to pick
    :param V: Forced list
    :param OpVDict: Vertexes dictionary
    :return: Chosen vertex
    """
    p = 0   # Flag to print for debugging

    weight = len(OpVDict) * 1000
    sVDict = {}
    for i in range(len(candidateV)):
        Vi = candidateV[i]
        sVDict[Vi] = OpVDict[Vi]['len'] + len([item for item in OpVDict[Vi]['conn'] if item in V]) * weight
    sVDict = {k: v for k, v in sorted(sVDict.items(), key=lambda item: item[1], reverse=True)}
    maxL = sVDict[list(sVDict.keys())[0]]
    pool = [item for item in sVDict.keys() if sVDict[item] == maxL]
    if p: print("Candidate vertexes pool for hauristic pick: ", pool)

    return random.choice(pool)

def RemoveEdge(keep, A, e, Z, AgS, OpVDict):
    """
    :param keep: Boolean of keep the edge and remove other or remove this edge
    :param A: Agree set on the edge
    :param e: The edge to keep or remove
    :param Z: The vertex to remove
    :param AgS: Agree set occurence
    :param OpVDict: Vertexes dictionary
    :return: 1: Updated AgS, 2: Updated OpVDict
    """
    p = 0   # Flag to print for debugging

    copyAgSi = copy.deepcopy(AgS[A])
    if keep:
        if p: print("Keep edge {} and duplicates of {} to remove.".format(e, A))
        XList = []
        for i in range(copyAgSi[0]):
            if copyAgSi[1][i] != e:
                XList.append(copyAgSi[1][i])

        AgS[A][0] = 1
        AgS[A][1].clear()
        AgS[A][1].append(e)

        for j in range(len(XList)):
            if XList[j][0] in OpVDict.keys() and XList[j][1] in OpVDict[XList[j][0]]['conn']:
                OpVDict[XList[j][0]]['len'] -= 1
                if A in OpVDict[XList[j][0]]['edges']: OpVDict[XList[j][0]]['edges'].remove(A)
                OpVDict[XList[j][0]]['conn'].remove(XList[j][1])
            if XList[j][1] in OpVDict.keys() and XList[j][0] in OpVDict[XList[j][1]]['conn']:
                OpVDict[XList[j][1]]['len'] -= 1
                if A in OpVDict[XList[j][1]]['edges']: OpVDict[XList[j][1]]['edges'].remove(A)
                OpVDict[XList[j][1]]['conn'].remove(XList[j][0])
    else:   ## Remove edge e
        XList = []
        for i in range(copyAgSi[0]):
            if copyAgSi[1][i] == e:
                if copyAgSi[1][i][0] == Z:
                    XList.append((copyAgSi[1][i][1], A))
                else:
                    XList.append((copyAgSi[1][i][0], A))

                AgS[A][0] -= 1
                AgS[A][1].remove(e)

        copyAgS = copy.deepcopy(AgS)
        for k in copyAgS.keys():
            for j in range(copyAgS[k][0]):
                if copyAgS[k][1][j][0] == Z:
                    XList.append((copyAgS[k][1][j][1], k))
                    AgS[k][0] -= 1
                    AgS[k][1].remove(copyAgS[k][1][j])
                elif copyAgS[k][1][j][1] == Z:
                    XList.append((copyAgS[k][1][j][0], k))
                    AgS[k][0] -= 1
                    AgS[k][1].remove(copyAgS[k][1][j])

        for n in range(len(XList)):
            if XList[n][0] in OpVDict.keys() and Z in OpVDict[XList[n][0]]['conn']:
                OpVDict[XList[n][0]]['len'] -= 1
                if XList[n][1] in OpVDict[XList[n][0]]['edges']: OpVDict[XList[n][0]]['edges'].remove(XList[n][1])
                OpVDict[XList[n][0]]['conn'].remove(Z)

        if Z in OpVDict.keys():
            del OpVDict[Z]
            if p: print("{} has been removed from OpVDict".format(Z))

    return {1: AgS, 2: OpVDict}

def Domination(AgS):
    """
    :param AgS: Agree set occurence
    :return: Vertexes list
    """

    p = 0   # Flag to print for debugging

    counter = 0
    dCounter = 0
    V = []
    AList = []
    OpVDict = {}
    for k in AgS.keys():
        ## Key vertexes for agree sets only appear once
        if AgS[k][0] == 1:
            i = AgS[k][1][0][0]
            j = AgS[k][1][0][1]

            if p: print("{} and {} are key vetexes of unique agree set {}.".format(i, j, k))
            if i not in V: V.append(i)
            if j not in V: V.append(j)
        else:
            AList.append(k)
            c = KeyVCheck(AgS[k])
            if len(c) > 0:
                if p: print("{} is key vetex of agree set {}.".format(c[0], k))
                if c[0] not in V: V.append(c[0])

        for j in range(AgS[k][0]):
            ## Candidate vertexes for dominance check
            if AgS[k][1][j][0] not in OpVDict.keys():
                OpVDict[AgS[k][1][j][0]] = {}
                OpVDict[AgS[k][1][j][0]]["len"] = 1
                OpVDict[AgS[k][1][j][0]]["edges"] = [k]
                OpVDict[AgS[k][1][j][0]]["conn"] = [AgS[k][1][j][1]]
            else:
                OpVDict[AgS[k][1][j][0]]["len"] += 1
                OpVDict[AgS[k][1][j][0]]["edges"].append(k)
                OpVDict[AgS[k][1][j][0]]["conn"].append(AgS[k][1][j][1])

            if AgS[k][1][j][1] not in OpVDict.keys():
                OpVDict[AgS[k][1][j][1]] = {}
                OpVDict[AgS[k][1][j][1]]["len"] = 1
                OpVDict[AgS[k][1][j][1]]["edges"] = [k]
                OpVDict[AgS[k][1][j][1]]["conn"] = [AgS[k][1][j][0]]
            else:
                OpVDict[AgS[k][1][j][1]]["len"] += 1
                OpVDict[AgS[k][1][j][1]]["edges"].append(k)
                OpVDict[AgS[k][1][j][1]]["conn"].append(AgS[k][1][j][0])

    if p:
        print("Key vertexes ({}): {}".format(len(V), sorted(V)))
        print("Vertexes for dominance check({}): {}".format(len(OpVDict), OpVDict))
        print("Duplicated agree sets({}): {}".format(len(AList), AList))

    v_dominating = []
    v_dominated = [item for item in list(OpVDict.keys()) if item not in V]
    if p:
        print("v_dominating ({}): {}".format(len(v_dominating), v_dominating))
        print("v_dominated ({}): {}".format(len(v_dominated), v_dominated))

    while len(AList) > 0:
        if len(v_dominated) > 0:
            v0 = v_dominated[0]
            v_check = []
            for i in range(OpVDict[v0]['len']):
                v_check = v_check + list(set(itertools.chain.from_iterable(AgS[OpVDict[v0]['edges'][i]][1])) - set(v_check))
            v_check = [item for item in v_check if item != v0]
            if p: print("Domination check for {} with ({}): {}".format(v0, len(v_check), sorted(v_check)))

            rList = []
            for j in range(len(v_check)):
                counter += 1
                DomPair = DomCheck(v0, v_check[j], OpVDict, V)
                if len(DomPair) > 0:
                    rList.append(DomPair[1])
                    dCounter += 1
                    if DomPair[1] == v0:
                        break

            if len(rList) > 0:
                copyAList = copy.deepcopy(AList)
                for i in range(len(copyAList)):
                    A = copyAList[i]
                    tempAgS = copy.deepcopy(AgS[A])
                    for j in range(tempAgS[0]):
                        zList = [value for value in tempAgS[1][j] if value in rList]
                        if len(zList) > 0:
                            update = RemoveEdge(0, A, tempAgS[1][j], zList[0], AgS, OpVDict)
                            AgS = update[1]
                            OpVDict = update[2]
                            if p: print("{} {} has been removed from graph.".format(A, tempAgS[1][j]))

                    if AgS[A][0] == 1:
                        if AgS[A][1][0][0] not in V: V.append(AgS[A][1][0][0])
                        if AgS[A][1][0][1] not in V: V.append(AgS[A][1][0][1])
                        if AgS[A][1][0][0] in v_dominated: v_dominated.remove(AgS[A][1][0][0])
                        if AgS[A][1][0][1] in v_dominated: v_dominated.remove(AgS[A][1][0][1])
                        AList.remove(A)
                        if p: print("Duplicates of {} has been removed from graph.".format(A))
                    else:
                        c = KeyVCheck(AgS[A])
                        if len(c) > 0:
                            if p: print("{} is key vetex of agree set {} now.".format(c[0], A))
                            if c[0] not in V: V.append(c[0])
                            if c[0] in v_dominated: v_dominated.remove(c[0])

                if p: print("Vertexes to remove from the graph: {}".format(rList))
                v_dominated =  [item for item in v_dominated if item not in rList]
            if v0 not in rList and v0 not in V: v_dominating.append(v0)
            if v0 in v_dominated: v_dominated.remove(v0)

            if p:
                print("v_dominating ({}): {}".format(len(v_dominating), v_dominating))
                print("v_dominated ({}): {}".format(len(v_dominated), v_dominated))
                print("Key vertexes update({}): {}".format(len(V), sorted(V)))
                print("Duplicated agree sets update ({}): {}".format(len(AList), AList))
                print("Agree set occurrence updated ({}): {}".format(len(AgS), AgS))
        elif len(v_dominating) > 0:
            ## Hauristic pick vertex among highest rank
            ChosenV = HaurPick(v_dominating, V, OpVDict)

            if ChosenV not in V: V.append(ChosenV)
            if ChosenV in v_dominating: v_dominating.remove(ChosenV)
            if p: print("{} has been forced into graph.".format(ChosenV))

            v_dominated = copy.deepcopy(v_dominating)
            v_dominating.clear()

        if p:
            print("v_dominating ({}): {}".format(len(v_dominating), v_dominating))
            print("v_dominated ({}): {}".format(len(v_dominated), v_dominated))
            print("Key vertexes ({}): {}".format(len(V), sorted(V)))
            print("Duplicated agree sets({}): {}".format(len(AList), AList))
            print("Agree set occurrence ({}): {}".format(len(AgS), AgS))

    V1 = []
    for k in AgS.keys():
        V1 = sorted(V1 + list(set(AgS[k][1][0]) - set(V1)))

    print("DOMINATION: {} vertexes left (V1): {}".format(len(V1), sorted(V1)))
    print("Vertexs removed by domination: ", dCounter)

    ## Result check
    for k in AgS.keys():
        for i in range(len(AgS[k][1])):
            if AgS[k][1][i][0] not in V1 or AgS[k][1][i][1] not in V1:
                AgS[k][0] -=1
    for k in AgS.keys():
        if AgS[k][0] < 1:
            print(k, AgS[k])
    for k in AgS.keys():
        if AgS[k][0] > 1:
            print(k, AgS[k])

    return {1: V1, 2: dCounter, 3: counter}

f = 'iris'
Mining = False
pa1 = "/Users/wye1/Documents/Armstrong/DataSets/naumann_small/"
pa2 = "/Users/wye1/Documents/Armstrong/DataSets/naumann_mined/"
path = "/users/wye1/Documents/Armstrong/Informative/WorkFolder/"
#pa = "D:/Wendy/Armstrong/DataSets/naumann_small/"
#path = "D:/Wendy/Armstrong/Informative/WorkFolder/"
ATFile = pa1 + f + '.csv'
KeyFile = pa2 + f + '.txt'

# Main
if __name__ == "__main__":
    Start  = datetime.datetime.now()

    if Mining:
        MineResult = ATMining.ATMining(ATFile)
        AgSList = MineResult[1]
        R = MineResult[2]
        AgSDict = MineResult[3]
    else:
        Result = InitFromKey.InitGraph(ATFile, KeyFile)
        AgSList = Result[1]
        R = Result[2]
        AgSDict = Result[3]

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
    print("Agree set occurrence ({}): {}".format(len(AgS), AgS))
    V = sorted(V)
    print("Unisolated Vertexes({}): {}".format(len(V), V))

    outcome = Domination(AgS)
    FinalV = outcome[1]
    print("Domination check:", outcome[3])
    print("Domination occur:", outcome[2])

    End = datetime.datetime.now()

    print("Time of running: ", End - Start)
