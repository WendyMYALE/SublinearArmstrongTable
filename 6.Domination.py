## Domination check through vertexes + Weighted Vertex Rank
import datetime
import copy
import random
import itertools

import FunctionSet
import ATMining
import InitFromAgS

def KeyVCheck(AgSi):
    ## Key vertexes for AgSi - adjacent to all edges labelled AgSi
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

def RemoveDominated(AgS, rList):
    """
    :param AgS: Agree set occurence
    :param rList: Dominated vertexes to remove
    :return: Updated AgS
    """

    ToRemove = {}
    for k in AgS.keys():
        if AgS[k][0] > 1:
            for j in range(AgS[k][0]):
                if AgS[k][1][j][0] in rList or AgS[k][1][j][1] in rList:
                    if k not in ToRemove:
                        ToRemove[k] = [AgS[k][1][j]]
                    else:
                        ToRemove[k].append(AgS[k][1][j])

    for k in ToRemove.keys():
        AgS[k][0] -= len(ToRemove[k])
        for i in range(len(ToRemove[k])):
            AgS[k][1].remove(ToRemove[k][i])
            #print("RemoveDominated: ", k, ToRemove[k][i], "has been removed from the graph")

    return AgS

def UpdateGraph(AgS, ForcedV):
    """
    :param AgS: Agree set occurence
    :param ForcedV: Forced vertexes list
    :return: 1: V; 2: AList; 3: OpVDict
    """

    V = []
    AList = []
    for k in AgS.keys():
        ## Key vertexes for agree sets only appear once
        if AgS[k][0] == 1:
            i = AgS[k][1][0][0]
            j = AgS[k][1][0][1]

            #print("UpdateGraph: {} and {} are key vetexes of unique agree set {}.".format(i, j, k))
            if i not in V: V.append(i)
            if j not in V: V.append(j)
        else:   ## Key vertexes for certain agree sets
            AList.append(k)
            c = KeyVCheck(AgS[k])
            if len(c) > 0:
                #print("UpdateGraph: {} is key vetex of agree set {}.".format(c[0], k))
                if c[0] not in V: V.append(c[0])

    OpVDict = {}
    for k in AgS.keys():
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

    for i in range(len(V)):
        if V[i] in OpVDict.keys():
            del OpVDict[V[i]]

    for j in range(len(ForcedV)):
        if ForcedV[j] in OpVDict.keys():
            del OpVDict[ForcedV[j]]

    return {1: V, 2:AList, 3: OpVDict}

def Domination(AgS):
    """
    :param AgS: Agree set occurence
    :return: Vertexes list
    """

    p = 0   # Flag to print for debugging

    counter = 0
    dCounter = 0
    ForcedV = []
    output = UpdateGraph(AgS, ForcedV)
    V = output[1]
    AList = output[2]
    OpVDict = output[3]
    v_dominating = []
    v_dominated = [item for item in list(OpVDict.keys()) if item not in V]

    if p:
        print("Validated vertexes ({}): {}".format(len(V + ForcedV), sorted(V)))
        print("Vertex dictionary ({}): {}".format(len(OpVDict), OpVDict))
        print("Duplicated agree sets({}): {}".format(len(AList), AList))
        print("v_dominating ({}): {}".format(len(v_dominating), v_dominating))
        print("v_dominated ({}): {}".format(len(v_dominated), v_dominated))

    #for x in range(40):
    while len(AList) > 0:
        while len(v_dominated) > 1:
            v0 = v_dominated.pop(0)
            if p: print("Domination check for {} with other {} vertexes: {}".format(v0, len(v_dominated), v_dominated))

            rList = []
            for j in range(len(v_dominated)):
                counter += 1
                DomPair = DomCheck(v0, v_dominated[j], OpVDict, V)
                if len(DomPair) > 0:
                    rList.append(DomPair[1])
                    if p: print(DomPair[1], "is dominated by", DomPair[0])
                    dCounter += 1
                    if DomPair[1] == v0:
                        break

            if len(rList) > 0:  ## domination(s) occurred
                AgS = RemoveDominated(AgS, rList)
                break
            else:
                v_dominating.append(v0)
                if p: print("No domination occurred for", v0, "and others")

        if len(rList) > 0:
            output = UpdateGraph(AgS, ForcedV)
            V = output[1]
            AList = output[2]
            OpVDict = output[3]
            v_dominating = []
            v_dominated = [item for item in list(OpVDict.keys()) if item not in V]

            if p:
                print("Validated vertexes ({}): {}".format(len(V + ForcedV), sorted(V)))
                print("Vertex dictionary ({}): {}".format(len(OpVDict), OpVDict))
                print("Duplicated agree sets({}): {}".format(len(AList), AList))
                print("v_dominating ({}): {}".format(len(v_dominating), v_dominating))
                print("v_dominated ({}): {}".format(len(v_dominated), v_dominated))

        if len(v_dominating) > 0:
            ## Hauristic pick vertex among highest rank
            ChosenV = HaurPick(v_dominated + [v0], V + ForcedV, OpVDict)

            if ChosenV not in ForcedV: ForcedV.append(ChosenV)
            if ChosenV in v_dominated: v_dominated.remove(ChosenV)
            if p: print("Hauristic pick: {} has been forced into graph.".format(ChosenV))

            UniqueAgS = {}
            TotalV = V + ForcedV
            for k in AgS.keys():
                if AgS[k][0] > 1:
                    for i in range(AgS[k][0]):
                        if AgS[k][1][i][0] in TotalV and AgS[k][1][i][1] in TotalV:   ## AgS[k] becomes unique
                            UniqueAgS[k] = (AgS[k][1][i][0], AgS[k][1][i][1])
                            break

            for k in UniqueAgS.keys():
                AgS[k] = [1, [UniqueAgS[k]]]

            output = UpdateGraph(AgS, ForcedV)
            V = output[1]
            AList = output[2]
            OpVDict = output[3]
            v_dominating = []
            v_dominated = [item for item in list(OpVDict.keys()) if item not in V]

        if p: print("Agree set occurrence ({}): {}".format(len(AgS), AgS))

    print("Agree set occurrence ({}): {}".format(len(AgS), AgS))
    V1 = []
    for k in AgS.keys():
        V1 = sorted(V1 + list(set(AgS[k][1][0]) - set(V1)))

    print("DOMINATION: {} vertexes left (V1): {}".format(len(V1), sorted(V1)))
    print("Vertexs removed by domination: ", dCounter)

    return {1: V1, 2: dCounter, 3: counter}

f = 'chess'
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
