import csv
import math
import copy
import random
import itertools

def AttributeSet(E, R):
    """
    :param E: Edge list
    :param R: Attributes set (schema)
    :return: Attribute clique clusters (disjoint set of attributes)
    """

    ToDebug = 0  # Flag to print for debugging

    n = int(1 + math.sqrt(1 + 8 * E.length()) / 2)
    Attr = [['', [-1 for y in range(n)]] for x in range(len(R))]
    for i in range(len(R)):
        Attr[i][0] = R[i]
        for j in range(E.length()):
            if R[i] in E.GetValue(j, "AttrSet"):
                v = E.GetValue(j, "Nodes")  # Node pair (v0, v1)
                if Attr[i][1][v[0]] == -1 and Attr[i][1][v[1]] == -1:
                    Attr[i][1][v[0]] = v[0]
                    Attr[i][1][v[1]] = v[0]
                elif Attr[i][1][v[0]] == -1 and Attr[i][1][v[1]] != -1:
                    Attr[i][1][v[0]] = Attr[i][1][v[1]]
                elif Attr[i][1][v[0]] != -1 and Attr[i][1][v[1]] == -1:
                    Attr[i][1][v[1]] = Attr[i][1][v[0]]
                else:
                    vl = max(Attr[i][1][v[0]], Attr[i][1][v[1]])
                    vs = min(Attr[i][1][v[0]], Attr[i][1][v[1]])
                    Attr[i][1] = [x if x != vl else vs for x in Attr[i][1]]  # replace vl with vs

            if ToDebug: print("AttributeSet", Attr)

    return (Attr)

def BitToString(R, Bit):
    Str = ''
    for i in range(len(Bit)):
        if Bit[i] == '1':
            Str += R[i]

    return Str

def BuildAT(EdgeList, R):
    """
    :param EdgeList: Edge list
    :param R: Attributes set (schema)
    :return: Armstrong table
    """

    AppliedEdge = dict()
    for k in range(EdgeList.length()):
        if EdgeList.GetValue(k, "Assigned") == 1:
            AppliedEdge[EdgeList.GetValue(k, "Nodes")] = EdgeList.GetValue(k, "AttrSet")

    n = int(1 + math.sqrt(1 + 8 * EdgeList.length()) / 2)
    AT = [[0] * len(R) for x in range(n)]
    AList = dict()
    for A in R:
        AList[A] = []

    number = 1
    for k in AppliedEdge.keys():
        for i in range(len(R)):
            if R[i] in AppliedEdge[k]:
                if k[0] in AList[R[i]]:
                    AT[k[1] - 1][i] = AT[k[0] - 1][i]
                    AList[R[i]].append(k[1])
                elif k[1] in AList[R[i]]:
                    AT[k[0] - 1][i] = AT[k[1] - 1][i]
                    AList[R[i]].append(k[0])
                else:
                    AT[k[0] - 1][i] = number
                    AT[k[1] - 1][i] = number
                    AList[R[i]] = [k[0], k[1]]
                    number += 1

    for i in range(n):
        for j in range(len(R)):
            if AT[i][j] == 0:
                AT[i][j] = number
                number += 1

    print(n, 'tuples Armstrong Table built as:')
    print(R)
    ATFile = 'AT.csv'
    with open(ATFile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in range(n):
            print(AT[i])
            writer.writerow(AT[i])

    return ATFile

def CliqueCheck(EdgeList, R, AgreeSets, AS, e):
    """
    :param EdgeList: Edge list before assignment
    :param R: Attributes set (schema)
    :param AgreeSets: Entire list of agree sets
    :param AS: Agree set to assign
    :param e: Node pair for new assignment
    :return: 1. Applying result - True or False
             2. Updated EdgeList
    """

    ToDebug = 0  # Flag to print for debugging

    result = ForcedAttr(EdgeList, R, AS, e)
    Apply = result[1]
    AList = result[2]

    for k in AList.keys():
        ClosedSet = Closure(R, AgreeSets, EdgeList.GetValue(k, "AttrSet") + AList[k])
        if ToDebug: print("Closed set for", EdgeList.GetValue(k, "AttrSet") + AList[k], "is", ClosedSet)

        if StringToBit(R, R) != StringToBit(R, ClosedSet):
            EdgeList.SetValue(k, "AttrSet", ClosedSet)
            if ToDebug: print("Forced edge on", k, "is:", ClosedSet)
        else:
            Apply = False
            if ToDebug: print("Closed set for", EdgeList.GetValue(k, "AttrSet") + AList[k], "is", ClosedSet,
                        "All attribute included. Apply failed.")
            break

    return {1: Apply, 2: EdgeList}

def Closure(R, AgS, Set):
    IntSec = StringToBit(R, R)
    for i in range(len(AgS)):
        if int(StringToBit(R, Set), 2) & int(StringToBit(R, AgS[i]), 2) == int(StringToBit(R, Set), 2):
            IntSec = format(int(IntSec, 2) & int(StringToBit(R, AgS[i]), 2), '0' + str(len(R)) + 'b')

    return BitToString(R, IntSec)

def EdgeScan(EdgeList, l1, l2):
    ToDebug = 0  # Flag to print for debugging
    list = []
    if ToDebug: print("Clique cluster 1:", l1, "Clique cluster 2:", l2)
    for i in range(len(l1)):
        for j in range(len(l2)):
            v1 = min(l1[i], l2[j])
            v2 = max(l1[i], l2[j])
            k = int((v2 * (v2 + 1) / 2 - 1) - (v2 - v1 - 1))  # Compute edge number between l1[i] and l2[j]
            if EdgeList.GetValue(k, "Assigned") == 1:
                Apply = False
                if ToDebug: print("Edge", k, "(", l1[i], ",", l2[j], ") labeled with", EdgeList.GetValue(k, "AttrSet"))
            else:
                Apply = True
                list.append(k)
                if ToDebug: print("Edge", k, "(", l1[i], ",", l2[j], ") is added to append list:", list)
            if not Apply: break
        if not Apply: break

    return {1: Apply, 2: list}

def FindGenSet(AgSDict, R):
    """
    :param AgSDict: Agree sets dictionary
    :param R: Attributes set (schema)
    :return: Generator sets
    """

    ToDebug = 0  # Flag to print for debugging

    AgList = []
    for key in AgSDict.keys():
        if AgSDict[key] not in AgList:
            AgList.append(AgSDict[key])
    if ToDebug: print("Distinct Agree sets List ({}): {}".format(len(AgList), AgList))

    AgSList = []
    for i in range(len(AgList)):
        AgSList.append(StringToBit(R, AgList[i]))
    if ToDebug: print("Agree sets List in bits({}): {}".format(len(AgSList), AgSList))

    # Bitwise AND to find common attributes, hence generated agree sets
    c1 = 0
    c2 = 0
    c3 = 0
    c4 = 0
    GenSets = {}
    for A in AgSList:
        ## Supersets searching for each Agree Set
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

    print("Generated sets ({}): {}".format(len(GenSets), GenSets))
    print("Generator sets ({}): {}".format(len(AgSList), AgSList))
    print("{} Agree sets don't have supersets; {} have only one. {} don't equal intersection of their supersets. Rest {} are generated sets.".format(c5-c1,c2,c3,c4))

    return AgSList

def FindKey(AgSList, R):
    ToDebug = 0   # Flag to print for debugging

    if ToDebug: print("Agree sets: ", AgSList)
    CompList = [[] for a in range(len(AgSList))]
    s = []
    for i in range(len(AgSList)):
        s[:0] = AgSList[i]
        for j in range(len(s)):
            if s[j] == '0':
                CompList[i].append(R[j])
        s = []
    if ToDebug: print("Compliments of agree sets: ", CompList)

    ## Optimized approach to speed up
    mCompList = []
    Keys = []
    exList = []
    for i in range(len(CompList)):
        exList = []
        if len(mCompList) > 0:
            for a in range(len(mCompList[0])):
                for b in range(len(CompList[i])):
                    if Subset(CompList[i][b], mCompList[0][a]) and mCompList[0][a] not in exList:
                        exList.append(mCompList[0][a])
            mCompList[0] = [item for item in mCompList[0] if item not in exList]
        mCompList.append(CompList[i])
        products = itertools.product(*mCompList)
        Keu = []
        for t in list(products):
            s = sorted(list(set(t)))
            item = RemoveDupAttr(''.join([str(e) for e in s]))
            if item not in Keys: Keys.append(item)
        mCompList = [RemoveSuperSet(Keys + exList)]
    Keys = RemoveSuperSet(Keys + exList)
    if ToDebug: print("Keys: ", Keys)
    #products = itertools.product(*CompList)

    # Keys = []
    # for t in list(products):
    #     s = sorted(list(set(t)))
    #     Keys.append(''.join([str(e) for e in s]))
    # Keys = list(set(Keys))
    # if ToDebug: print("Keys: ", Keys)
    #
    # ## Remove super sets
    # a2del = []
    # for A in Keys:
    #     for B in [item for item in Keys if item not in A]:
    #         if Subset(A, B) and B not in a2del:
    #             a2del.append(B)
    # Keys = list(set(Keys) - set(a2del))

    KeysBit = []
    for k in Keys:
        KeysBit.append(StringToBit(R, k))

    return KeysBit

def FindAgS(Keys, R):
    ToDebug = 0   # Flag to print for debugging

    if ToDebug: print("Keys: ", Keys)
    KeyList = [[] for a in range(len(Keys))]
    s = []
    for i in range(len(Keys)):
        s[:0] = Keys[i]
        for j in range(len(s)):
            if s[j] == '1':
                KeyList[i].append(R[j])
        s = []
    if ToDebug: print("Key list: ", KeyList)

    ## Optimized approach to speed up
    mKeyList = []
    AgSCom = []
    exList = []
    for i in range(len(KeyList)):
        exList = []
        if len(mKeyList) > 0:
            for a in range(len(mKeyList[0])):
                for b in range(len(KeyList[i])):
                    if Subset(KeyList[i][b], mKeyList[0][a]) and mKeyList[0][a] not in exList:
                        exList.append(mKeyList[0][a])
            mKeyList[0] = [item for item in mKeyList[0] if item not in exList]
        mKeyList.append(KeyList[i])
        products = itertools.product(*mKeyList)
        AgSCom = []
        for t in list(products):
            s = sorted(list(set(t)))
            item = RemoveDupAttr(''.join([str(e) for e in s]))
            if item not in AgSCom: AgSCom.append(item)
        mKeyList = [RemoveSuperSet(AgSCom + exList)]
    AgSCom = RemoveSuperSet(AgSCom + exList)
    if ToDebug: print("Compliments of agree sets: ", AgSCom)

    AgS = []
    for i in range(len(AgSCom)):
        st = ''
        for j in range(len(R)):
            if R[j] not in AgSCom[i]:
                st += R[j]
        AgS.append(st)
    if ToDebug: print("Agree sets: ", AgS)

    AgSBit = []
    for k in AgS:
        AgSBit.append(StringToBit(R, k))

    return RemoveSuperSetInBit(AgSBit)

def ForcedAttr(EdgeList, R, AS, e):
    """
    :param EdgeList: Edge list before assignment
    :param R: Attributes set (schema)
    :param AS: Agree set to assign
    :param e: Node pair for new assignment
    :return: 1. Applying result - True or False
             2. Newly forced attribute sets
    """

    ToDebug = 0

    Attr = AttributeSet(EdgeList, R)
    for j in range(len(Attr)):
        if ToDebug: print(Attr[j])

    AList = {}
    for i in range(len(Attr)):  # For each attribute
        if ToDebug: print("Attribute", Attr[i][0], "is subset of ", AS, Attr[i][0] in AS, "; For edge (", e[0], ",", e[1],
                    "), cluster for vertex", e[0], ":", Attr[i][1][e[0]], ", cluster for vertex", e[1], ":",
                    Attr[i][1][e[1]])
        if Attr[i][0] in AS:
            if Attr[i][1][e[0]] == -1 and Attr[i][1][e[1]] == -1:  # Attribute i doesn't appear on both vertices of e
                Apply = True
                Attr[i][1][e[0]] = e[0]
                Attr[i][1][e[1]] = e[0]
            elif Attr[i][1][e[0]] == -1 and Attr[i][1][e[1]] != -1:  # Attribute i not on e[0] but on e[1]
                l1 = [e[0]]
                l2 = [s for s, x in enumerate(Attr[i][1]) if
                      x == Attr[i][1][e[1]]]  # Vertices in same clique cluster with e[1]
                l2.remove(e[1])
                check = EdgeScan(EdgeList, l1, l2)
                Apply = check[1]
                if Apply:
                    Attr[i][1][e[0]] = Attr[i][1][e[1]]
                    list = check[2]
                    if ToDebug: print("Attribute", Attr[i][0], "is forced on", list)
                    for j in range(len(list)):
                        if list[j] in AList:
                            AList[list[j]] += Attr[i][0]
                        else:
                            AList[list[j]] = Attr[i][0]
                    if ToDebug: print("Forced attributes to add:", AList)
            elif Attr[i][1][e[0]] != -1 and Attr[i][1][e[1]] == -1:  # Attribute i on e[0] but not on e[1]
                l1 = [e[1]]
                l2 = [s for s, x in enumerate(Attr[i][1]) if
                      x == Attr[i][1][e[0]]]  # Vertices in same clique cluster with e[0]
                l2.remove(e[0])
                check = EdgeScan(EdgeList, l1, l2)
                Apply = check[1]
                if Apply:
                    Attr[i][1][e[1]] = Attr[i][1][e[0]]
                    list = check[2]
                    if ToDebug: print("Attribute", Attr[i][0], "is forced on", list)
                    for j in range(len(list)):
                        if list[j] in AList:
                            AList[list[j]] += Attr[i][0]
                        else:
                            AList[list[j]] = Attr[i][0]
                    if ToDebug: print("Forced attributes to add:", AList)
            else:  # Attribute i appears on both vertexes of e
                if Attr[i][1][e[0]] == Attr[i][1][e[1]]:
                    if ToDebug: print("Vertex", e[0], "and vertex", e[1], "in same cluster", Attr[i][1][e[0]])
                    Apply = True
                else:
                    l1 = [s for s, x in enumerate(Attr[i][1]) if
                          x == Attr[i][1][e[0]]]  # Vertices in same clique cluster with e[0]
                    l2 = [s for s, x in enumerate(Attr[i][1]) if
                          x == Attr[i][1][e[1]]]  # Vertices in same clique cluster with e[1]
                    check = EdgeScan(EdgeList, l1, l2)
                    Apply = check[1]
                    if Apply:
                        vl = max(Attr[i][1][e[1]], Attr[i][1][e[0]])
                        vs = min(Attr[i][1][e[1]], Attr[i][1][e[0]])
                        Attr[i][1] = [x if x != vl else vs for x in Attr[i][1]]
                        list = check[2]
                        if ToDebug: print("Attribute", Attr[i][0], "is forced on", list)
                        for j in range(len(list)):
                            if list[j] in AList:
                                AList[list[j]] += Attr[i][0]
                            else:
                                AList[list[j]] = Attr[i][0]
                        if ToDebug: print("Forced attributes to add:", AList)
        else:  # Attribute i is not in As
            Apply = True

        if ToDebug: print(Attr[i][0], "apply on (", e[0], ",", e[1], ") is", Apply)

        if not Apply:
            break

    return {1: Apply, 2: AList}

def Match(s1, s2, R):
    m = 0
    for i in range(len(R)):
        if R[i] in s1 and R[i] in s2:
            m += 1

    return m

def MatchSize(a, b):
    r = -1

    for i in a.split('~'):
        if i in b:
            r += 1
        else:
            r = 0
            break

    return r

def MergeAttrSets(s1, s2):
    if len(s1) > 0 and len(s2) > 0:
        l = sorted(list(set(s1[0:-1].split('~') + s2[0:-1].split('~'))))
        return '~'.join([str(s) for s in l]) + '~'
    elif len(s1) > 0:
        return s1
    else:
        return s2

def RandomList(list):
    list0 = copy.deepcopy(list)
    list1 = []
    for i in range(len(list0)):
        e = random.choice(list0)
        list1.append(e)
        list0.remove(e)

    return list1

def RemoveDupAttr(st):
    l = sorted(list(set(st[0:-1].split('~'))))

    return '~'.join([str(s) for s in l]) + '~'

def RemoveSuperSet(l):
    ToDel = []
    for i in range(len(l)):
        for j in range(len(l) - i - 1):
            if Subset(l[i], l[j + i + 1]):
                ToDel.append(l[j + i + 1])
            elif Subset(l[j + i + 1], l[i]):
                ToDel.append(l[i])

    return [item for item in l if item not in ToDel]

def RemoveSuperSetInBit(l):
    ToDel = []
    for i in range(len(l)):
        for j in range(len(l) - i - 1):
            if int(l[i], 2) & int(l[j + i + 1], 2) == int(l[i], 2):
                ToDel.append(l[i])
            elif int(l[i], 2) & int(l[j + i + 1], 2) == int(l[j + i + 1], 2):
                ToDel.append(l[j + i + 1])

    return [item for item in l if item not in ToDel]

def StringToBit(R, String):
    l = ''
    for C in R:
        if C in String:
            l += '1'
        else:
            l += '0'

    return l

def Subeq(a, b):
    r = True

    for i in range(len(a)):
        if a[i] not in b:
            r = False

    return r

def Subset(a, b):
    # a is subset of b?
    r = False

    for i in a[:-1].split('~'):
        if i +'~' in b:
            r = True
        else:
            r = False
            break

    return r

def Subtract(a, b):
    # return a - b
    c = ''
    for i in a[:-1].split('~'):
        if i + '~' not in b:
            c += i + '~'

    return c

def transversal(l1, l2):
    """
    :param l1: Original list
    :param l2: Transversal list
    """

    l = l1.copy()
    newl = []
    if len(l2) == 0:
        newl = [[x] for x in l[0]]
        l.remove(l[0])
    else:
        for i in range(len(l2)):
            if l[0][0] in l2[i]:
                newl.append(l2[i])
            else:
                newl.append(l2[i] + [l[0][0]])
            for j in range(len(l[0]) - 1):
                if l[0][j + 1] in l2[i]:
                    newl.append(l2[i])
                else:
                    newl.append(l2[i] + [l[0][j + 1]])

        l.remove(l[0])

    if len(l) == 0:
        newsl = []
        for s in newl:
            newsl.append(''.join([str(elem) for elem in sorted(s)]))
        return list(dict.fromkeys(newsl))
    else:
        l3 = transversal(l, newl)
        return l3

"""
import ClassSet
E = ClassSet.EdgeList(5)

E.SetValue(0, "Assigned", 1)
E.SetValue(0, "AttrSet", 'C1~C2~C4~')
E.SetValue(1, "Assigned", 1)
E.SetValue(1, "AttrSet", 'C1~C2~C5~')
E.SetValue(2, "AttrSet", 'C1~C2~')
E.SetValue(3, "Assigned", 1)
E.SetValue(3, "AttrSet", 'C1~C4~C5~')
E.SetValue(4, "AttrSet", 'C1~C4~')
E.SetValue(5, "AttrSet", 'C1~C5~')
E.SetValue(6, "AttrSet", 'C2~')
E.SetValue(7, "AttrSet", 'C2~')
E.SetValue(8, "Assigned", 1)
E.SetValue(8, "AttrSet", 'C2~C3~C4~')

#i = E.GetValue(4, "Nodes")[0]
#j = E.GetValue(4, "Nodes")[1]
#print("i: {}, j: {}, ceil(j*(j-1)/2) + i: {}".format(i, j, math.ceil(j*(j-1)/2) + i))

E.print()
R = ['C1~', 'C2~', 'C3~', 'C4~', 'C5~']
AgreeSets = ['C1~C2~C4~', 'C1~C2~C5~', 'C1~C4~C5~', 'C2~C3~C4~', 'C2~C3~C5~', 'C3~C4~C5~']
output = CliqueCheck(E, R, AgreeSets, 'C2~C3~C5~', (1,4))
print("Applied:", output[1])
output[2].print()
"""
