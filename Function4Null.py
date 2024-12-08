import copy

import ClassSet
import FunctionSet

def FindParameters(FileName):
    """
    :param FileName: File name of data set
    :return: 1. Attributes set (schema)
             2. Strong agree sets
             3. Weak agree sets
             4. Possible keys
             5. Certain keys
             6. Null set
    """

    ToDebug = 0   # Flag to print for debugging

    File1 = FileName + '_As.txt'
    File2 = FileName + '_Aw.txt'
    File3 = FileName + '_cKey.txt'
    File4 = FileName + '_pKey.txt'
    File5 = FileName + '_W.txt'

    file1 = open(File1, 'r')
    AsList = []
    for line in file1:
        AsList.append(line.rstrip())

    file2 = open(File2, 'r')
    AwList = []
    for line in file2:
        AwList.append(line.rstrip())

    file3 = open(File3, 'r')
    cKList = []
    for line in file3:
        cKList.append(line.rstrip())

    file4 = open(File4, 'r')
    pKList = []
    for line in file4:
        pKList.append(line.rstrip())

    file5 = open(File5, 'r')
    WList = []
    for line in file5:
        WList.append(line.rstrip())

    R = []
    for i in range(len(AsList[0])):
        R.append('C' + str(i + 1) + '~')

    StrongAS = []
    for i in range(len(AsList)):
        StrongAS.append(FunctionSet.BitToString(R, AsList[i]))
    WeakAS = []
    for i in range(len(AwList)):
        WeakAS.append(FunctionSet.BitToString(R, AwList[i]))
    cKey = []
    for i in range(len(cKList)):
        if len(cKList[i]) > 0: cKey.append(FunctionSet.BitToString(R, cKList[i]))
    pKey = []
    for i in range(len(pKList)):
        if len(pKList[i]) > 0: pKey.append(FunctionSet.BitToString(R, pKList[i]))
    w = []
    w[:0] = WList[0] ## Separated bits
    W = [int(i) for i in w] ## Convert to numbers

    print("Schema R:", R)
    print("Strong agree Sets:", StrongAS, "; Weak agree Sets:", WeakAS, "; Possible keys:", pKey, "; Certain keys:", cKey, "W:", W)

    return{1: R, 2: StrongAS, 3: WeakAS, 4: pKey, 5: cKey, 6: W}

def NullAttr(s, R, W):
    w = []
    ns = ''
    for i in range(len(R)):
        if R[i] in s and W[i] == 1:
            w.append(1)
        elif R[i] in s and W[i] == 0:
            ns += R[i]
            w.append(0)
        else:
            w.append(0)
    return {1: w, 2: ns}

def WeakAS(EdgeList, vMatrix, R, k):
    wAS = ''
    v1 = [i for i, j in enumerate(vMatrix[EdgeList.GetValue(k, "Nodes")[0]]) if j == 0]
    v2 = [i for i, j in enumerate(vMatrix[EdgeList.GetValue(k, "Nodes")[1]]) if j == 0]
    if len(v1) > 0:
        for i in v1:
            wAS = FunctionSet.MergeAttrSets(wAS, R[i])
    if len(v2) > 0:
        for i in v2:
            wAS = FunctionSet.MergeAttrSets(wAS, R[i])
    return wAS

def AssignStrongAS(EdgeList, vMatrix, As, R, pKey, e):
    """
    :param EdgeList: Edge list before assignment
    :param vMatrix: Vertex matrix before assignment
    :param As: Strong agree set to assign
    :param R: Attributes set (schema)
    :param pKey: Possible keys
    :param e: Node pair for new assignment
    :return: 1. Applying result - True or False
             2. Updated EdgeList
             3. Updated vMatrix
    """

    ToDebug = 0  # Flag to print for debugging

    result = FunctionSet.ForcedAttr(EdgeList, R, As, e)
    Apply = result[1]
    AList = result[2]
    if ToDebug: print("AList", AList)

    for k in AList.keys():
        f = FunctionSet.MergeAttrSets(EdgeList.GetValue(k, "AttrSet"), AList[k])
        if len(pKey) > 0:
            for pk in pKey:
                if not FunctionSet.Subset(pk, f) and EdgeList.GetValue(k, "Assigned") < 1:
                    EdgeList.SetValue(k, "AttrSet", f)
                    if ToDebug: print("Forced edge on", k, "is:", f)

                    for i in range(len(R)):
                        if R[i] in f:
                            vMatrix[EdgeList.GetValue(k, "Nodes")[0]][i] = 1
                            vMatrix[EdgeList.GetValue(k, "Nodes")[1]][i] = 1
                else:
                    Apply = False
                    if ToDebug: print("Forced edge", f, "is superset of possible key", pk, "or forced on assigned edge. Apply failed!")
                    break
        else:
            EdgeList.SetValue(k, "AttrSet", f)
            if ToDebug: print("Forced edge on", k, "is:", f)

            for i in range(len(R)):
                if R[i] in f:
                    vMatrix[EdgeList.GetValue(k, "Nodes")[0]][i] = 1
                    vMatrix[EdgeList.GetValue(k, "Nodes")[1]][i] = 1

        if not Apply: break

    return {1: Apply, 2: EdgeList, 3: vMatrix}

def AssignWeakAS(EdgeList, vMatrix, Aw, R, cKey, k):
    """
    :param EdgeList: Edge list before assignment0
    :param vMatrix: Vertex matrix before assignment
    :param Aw: Week agree set to assign
    :param R: Attributes set (schema)
    :param cKey: Certain keys
    :param k: Edge for new assignment
    :return: 1. Applying result - True or False
             2. Updated EdgeList
             3. Updated vMatrix
    """

    ToDebug = 0  # Flag to print for debugging

    wAw = WeakAS(EdgeList, vMatrix, R, k)
    sAw = FunctionSet.Subtract(Aw, wAw)
    if ToDebug: print("Weak agree set", Aw, "splitted into:", sAw, wAw)
    result = FunctionSet.ForcedAttr(EdgeList, R, sAw, EdgeList.GetValue(k, "Nodes"))
    Apply = result[1]
    AList = result[2]

    if Apply:
        for i in range(EdgeList.length()):
            e = EdgeList.GetValue(i, "Nodes")
            if (0 in vMatrix[e[0]] or 0 in vMatrix[e[1]]) and i not in AList.keys():
                AList[i] = ''
        if ToDebug: print("AList", AList)

        for i in AList.keys():
            Fs = FunctionSet.MergeAttrSets(EdgeList.GetValue(i, "AttrSet"), AList[i])
            Fw = WeakAS(EdgeList, vMatrix, R, i)
            if len(AList[i]) > 0 and FunctionSet.Subset(EdgeList.GetValue(i, "AttrSet"), Fs) and EdgeList.GetValue(i, "Assigned") > 0:
                Apply = False
                if ToDebug: print("Forced edge", Fs + '+' + Fw, "is superset of assigned agree set", EdgeList.GetValue(i, "AttrSet"), ". Apply failed!")
                break
            elif len(cKey) > 0:
                for ck in cKey:
                    if FunctionSet.Subtract(ck, Fs) != '' and FunctionSet.Subset(FunctionSet.Subtract(ck, Fs), Fw):
                        Apply= False
                        if ToDebug: print("Forced edge", Fs + '+' + Fw, "is superset of certain key", ck, ". Apply failed!")
                        break
                    else:
                        Apply = True
                        EdgeList.SetValue(i, "AttrSet", Fs)
                        if ToDebug: print("Forced edge on", EdgeList.GetValue(i, "Nodes"), "is:", Fs + '+' + Fw)
            else:
                Apply = True
                EdgeList.SetValue(i, "AttrSet", Fs)
                if ToDebug: print("Forced edge on", EdgeList.GetValue(i, "Nodes"), "is:", Fs + '+' + Fw)

            if not Apply: break

    return {1: Apply, 2: EdgeList, 3: vMatrix}

def AwCheck(EdgeList, vMatrix, R, cKey, vList):
    """
    :param EdgeList: Edge list before assignment0
    :param vMatrix: Vertex matrix before assignment
    :param R: Attributes set (schema)
    :param cKey: Certain keys
    :param vList: Vertexes that adding NULL
    :return: Checking result - True or False
    """

    ToDebug = 0  # Flag to print for debugging

    Apply = False
    for i in range(len(vList)):
        for j in range(EdgeList.length()):
            if vList[i] in EdgeList.GetValue(j, "Nodes"):
                Fs = EdgeList.GetValue(j, "AttrSet")
                Fw = WeakAS(EdgeList, vMatrix, R, j)
                if ToDebug: print("Forced weak agree set on edge", j, "is:", Fs, "+", Fw)

                for ck in cKey:
                    if FunctionSet.Subtract(ck, Fs) != '' and FunctionSet.Subset(FunctionSet.Subtract(ck, Fs), Fw):
                        Apply= False
                        if ToDebug: print("Forced edge", Fs + '+' + Fw, "is superset of certain key", ck, ". Apply failed!")
                        break
                    else:
                        Apply = True

        if not Apply: break

    return Apply

def ExtraTuple(EdgeList, vMatrix, W):
    """
    :param EdgeList: Edge list before adding new tuple
    :param vMatrix: Vertex matrix before adding new tuple
    :param W: Null set
    :return: 1. New EdgeList
             2. New vMatrix
    """

    s = EdgeList.ActualSize()
    newE = ClassSet.EdgeList(s + 1)
    for i in range(int(s * (s - 1) / 2)):
        newE.SetValue(i, "Assigned", EdgeList.GetValue(i, "Assigned"))
        newE.SetValue(i, "AttrSet", EdgeList.GetValue(i, "AttrSet"))

    vMatrix.append([0 if i == 1 else -1 for i in W])

    return{1: newE, 2: vMatrix}

def Armstrong4As(E, V, As, R, pKey, depth=0):
    """
    :param E: Edge list
    :param V: Vertex matrix for Null value
    :param As: Remained strong agree sets
    :param R: Attributes set (schema)
    :param pKey: Possible keys
    :return: 1. Armstrong Table exists - True or False
             2. Edge list
             3. Vertex matrix
    """

    ToDebug = 0   # Flag to print for debugging
    for k in range(E.length()):
        ## Unassigned edge
        if E.GetValue(k, "Assigned") == 0:
            if ToDebug: print("Applying agree set", As[0], "on Edge:", k, E.GetValue(k, "Nodes"))
            if FunctionSet.Subset(E.GetValue(k, "AttrSet"), As[0]):
                ## No forced edge generated or As[0] is superset of forced edge
                E1 = copy.deepcopy(E)
                V1 = copy.deepcopy(V)
                As1 = As.copy()
                result = AssignStrongAS(E1, V1, As1[0], R, pKey, E.GetValue(k, "Nodes"))
                Apply = result[1]
                E1 = result[2]
                V1 = result[3]

                if Apply:
                    if ToDebug: print("Applied agree set", As1[0], "on Edge:", k, E1.GetValue(k, "Nodes"), "successfully : )")
                    E1.SetValue(k, "AttrSet", As1[0])
                    E1.SetValue(k, "Assigned", 1)

                    for i in range(len(R)):
                        if R[i] in As1[0]:
                            V1[E1.GetValue(k, "Nodes")[0]][i] = 1
                            V1[E1.GetValue(k, "Nodes")[1]][i] = 1

                    del As1[0]
                    if ToDebug: E1.print()

                    if len(As1) > 0:
                        if ToDebug: print("Before: As {}".format(As))
                        if ToDebug: print("Before: As1 {}".format(As1))
                        if ToDebug: print("Before: Apply is {}, k: {}, Depth: {}".format(Apply, k, depth))
                        output = Armstrong4As(E1, V1, As1, R, pKey, depth + 1)
                        Apply = output[1]
                        E1 = output[2]
                        V1 = output[3]
                        if ToDebug: E1.print()

                    n = E1.ActualSize()
                    if ToDebug: print("After: As {}".format(As))
                    if ToDebug: print("After: As1 {}".format(As1))
                    if ToDebug: print("After: Apply is {}, k: {}, Actual size: {}, Depth: {}".format(Apply, k, n, depth))

                    if Apply: return {1: Apply, 2: E1, 3: V1}
                else:
                    if ToDebug: print("Applied agree set", As1[0], "on Edge:", k, E1.GetValue(k, "Nodes"), "failed : (")
            else:  ## AS[0] is not superset of forced edge
                Apply = False
                #if ToDebug: print("Forced edge exists (", E[k]["AttrSet"], "), applied agree set", AS[0], "on Edge:", k, E.GetValue(k, "Nodes"), "failed : (")
                #if ToDebug: print("Forced edge exists, applied agree set", AS[0], "on Edge:", k, E.GetValue(k, "Nodes"), "failed : (")

    if not Apply: return {1: Apply, 2: E, 3: V}

def Armstrong4Aw(E, V, Aw, R, cKey, W, depth=0):
    """
    :param E: Edge list
    :param V: Vertex matrix for Null value
    :param Aw: Remained weak agree sets
    :param R: Attributes set (schema)
    :param cKey: Certain keys
    :param W: Null set
    :return: 1. Armstrong Table exists - True or False
             2. Edge list
             3. Vertex matrix
    """

    ToDebug = 0   # Flag to print for debugging

    for k in range(E.length()):
        ## Edge assignable
        if E.GetValue(k, "Assigned") < 2 and FunctionSet.Subset(E.GetValue(k, "AttrSet") + WeakAS(E, V, R, k), Aw[0]):
            w = NullAttr(FunctionSet.Subtract(Aw[0], E.GetValue(k, "AttrSet")), R, W)[1]
            if sum(w) != 0:
                if ToDebug: print("Applying weak agree set", Aw[0], "on Edge:", k, E.GetValue(k, "Nodes"))
                e = E.GetValue(k, "Nodes")

                if [- c * d for c, d in zip(V[e[0]], w)] == w or [- c * d for c, d in zip(V[e[1]], w)] == w:
                    ## e[0] or e[1] allow Nulls required
                    E1 = copy.deepcopy(E)
                    V1 = copy.deepcopy(V)
                    Aw1 = Aw.copy()

                    if [- c * d for c, d in zip(V[e[0]], w)] == w:
                        ## Set Nulls for e[0]
                        for i in range(len(w)):
                            if w[i] == 1 and V1[e[0]][i] == -1:
                                V1[e[0]][i] = 0
                        if ToDebug: print("Null on vertex", e[0], V1[e[0]])
                    else:
                        ## Set Nulls for e[1]
                        for i in range(len(w)):
                            if w[i] == 1 and V1[e[1]][i] == -1:
                                V1[e[1]][i] = 0
                        if ToDebug: print("Null on", e[1], V1[e[1]])

                    result = AssignWeakAS(E1, V1, Aw1[0], R, cKey, k)
                    Apply = result[1]
                    E1 = result[2]
                    V1 = result[3]

                    if Apply:
                        if ToDebug: print("Applied weak agree set", Aw1[0], "on Edge:", k, E1.GetValue(k, "Nodes"), "successfully : )")
                        E1.SetValue(k, "AttrSet", FunctionSet.Subtract(Aw1[0], WeakAS(E1, V1, R, k)))
                        E1.SetValue(k, "Assigned", E1.GetValue(k, "Assigned") + 1)

                        del Aw1[0]
                        if ToDebug: E1.print()
                        if ToDebug: print(V1)

                        if len(Aw1) > 0:
                            if ToDebug: print("Before: Aw {}".format(Aw))
                            if ToDebug: print("Before: Aw1 {}".format(Aw1))
                            if ToDebug: print("Before: Apply is {}, k: {}, Depth: {}".format(Apply, k, depth))
                            output = Armstrong4Aw(E1, V1, Aw1, R, cKey, W, depth + 1)
                            Apply = output[1]
                            E1 = output[2]
                            V1 = output[3]
                            if ToDebug: E1.print()
                            if ToDebug: print(V1)

                        n = E1.ActualSize()
                        if ToDebug: print("After: Aw {}".format(Aw))
                        if ToDebug: print("After: Aw1 {}".format(Aw1))
                        if ToDebug: print("After: Apply is {}, k: {}, Actual size: {}, Depth: {}".format(Apply, k, n, depth))

                        if Apply: return {1: Apply, 2: E1, 3: V1}
                    else:
                        if ToDebug: print("Applied weak agree set", Aw1[0], "on Edge:", k, E1.GetValue(k, "Nodes"), "failed : (")
                else:  ## Not enough attributes allow Nulls
                    Apply = False
                    if ToDebug: print("Not enough attributes allow Nulls on Edge:", k)
            else:
                Apply = False
                if ToDebug: print("No Null allows on Edge:", k, E.GetValue(k, "Nodes"), "for weak agree set", Aw[0])
        else:  ## Aw[0] failed applying on k
            Apply = False

    if not Apply: return {1: Apply, 2: E, 3: V}

def Armstrong4A(E, V, A, R, pKey, cKey, W, depth=0):
    """
    :param E: Edge list
    :param V: Vertex matrix for Null value
    :param A: Matched agree set pairs
    :param R: Attributes set (schema)
    :param pKey: Possible keys
    :param cKey: Certain keys
    :param W: Null set
    :return: 1. Armstrong Table exists - True or False
             2. Edge list
             3. Vertex matrix
    """

    ToDebug = 0   # Flag to print for debugging

    for k in range(E.length()):
        if E.GetValue(k, "Assigned") < 1 and FunctionSet.Subset(E.GetValue(k, "AttrSet"), A[0][0]) \
                and FunctionSet.Subset(E.GetValue(k, "AttrSet") + WeakAS(E, V, R, k), A[0][1]):
            ## Edge assignable
            e = E.GetValue(k, "Nodes")
            w0 = NullAttr(FunctionSet.Subtract(A[0][1], A[0][0]), R, W)[1]
            w = NullAttr(FunctionSet.Subtract(FunctionSet.Subtract(A[0][1], A[0][0]), E.GetValue(k, "AttrSet")), R, W)[1]
            if sum([a * b for a, b in zip(V[e[0]], w0)]) == 0 or sum([a * b for a, b in zip(V[e[1]], w0)]) == 0:
                ## Existing Null can be utilized.
                Nil = 1
            elif sum(w) != 0:
                if [- c * d for c, d in zip(V[e[0]], w)] == w or [- c * d for c, d in zip(V[e[1]], w)] == w \
                        or sum([- c * d for c, d in zip(V[e[0]], w)]) == 0 or sum([- c * d for c, d in zip(V[e[1]], w)]) == 0:
                    ## e[0] or e[1] allow Nulls required
                    Nil = 2
                else: ## Not enough attributes allow Nulls
                    Nil = 0
            else: ## No Null allows on Edge k
                Nil = 0

            if Nil > 0:
                E1 = copy.deepcopy(E)
                V1 = copy.deepcopy(V)
                A1 = A.copy()
                if ToDebug: print("Applied agree set pair", A1[0], "on Edge:", k, E.GetValue(k, "Nodes"))

                ## Check Strong agree set
                result = AssignStrongAS(E1, V1, A1[0][0], R, pKey, E.GetValue(k, "Nodes"))
                Apply = result[1]
                E1 = result[2]
                V1 = result[3]

                if Apply:
                    if Nil == 1:
                        if ToDebug: print("Utilize existing Null")
                    elif [- c * d for c, d in zip(V[e[0]], w)] == w:
                        ## Set Nulls for e[0]
                        for i in range(len(w)):
                            if w[i] == 1 and V1[e[0]][i] == -1:
                                V1[e[0]][i] = 0
                        if ToDebug: print("Null on vertex", e[0], V1[e[0]])
                    else:
                        ## Set Nulls for e[1]
                        for i in range(len(w)):
                            if w[i] == 1 and V1[e[1]][i] == -1:
                                V1[e[1]][i] = 0
                        if ToDebug: print("Null on", e[1], V1[e[1]])

                    result = AssignWeakAS(E1, V1, A1[0][1], R, cKey, k)
                    Apply = result[1]
                    E1 = result[2]
                    V1 = result[3]

                    if Apply:
                        if ToDebug: print("Applied agree set pair", A1[0], "on Edge:", k, E1.GetValue(k, "Nodes"), "successfully : )")
                        E1.SetValue(k, "AttrSet", FunctionSet.Subtract(A1[0][1], WeakAS(E1, V1, R, k)))
                        E1.SetValue(k, "Assigned", E1.GetValue(k, "Assigned") + 2)

                        del A1[0]
                        if ToDebug: E1.print()
                        if ToDebug: print("V:", V1)

                        if len(A1) > 0:
                            if ToDebug: print("Before: A {}".format(A))
                            if ToDebug: print("Before: A1 {}".format(A1))
                            if ToDebug: print("Before: Apply is {}, k: {}, Depth: {}".format(Apply, k, depth))
                            output = Armstrong4A(E1, V1, A1, R, pKey, cKey, W, depth + 1)
                            Apply = output[1]
                            E1 = output[2]
                            V1 = output[3]

                            if ToDebug: E1.print()
                            if ToDebug: print(V1)

                        n = E1.ActualSize()
                        if ToDebug: print("After: A {}".format(A))
                        if ToDebug: print("After: A1 {}".format(A1))
                        if ToDebug: print("After: Apply is {}, k: {}, Actual size: {}, Depth: {}".format(Apply, k, n, depth))

                        if Apply: return {1: Apply, 2: E1, 3: V1}
                    else:
                        if ToDebug: print("Applied weak agree set", A1[0][1], "on Edge:", k, E1.GetValue(k, "Nodes"), "failed : (")
                else: ## Strong agree set failed to assign
                    Apply = False
                    if ToDebug: print("Applied strong agree set", A1[0][0], "on Edge:", k, E1.GetValue(k, "Nodes"), "failed : (")
            else:
                Apply = False
                if ToDebug: print("Not enough attributes allow Nulls on Edge:", k)
        else:
            Apply = False
            if ToDebug: print("Edge", k, "is unassignable")

    if not Apply: return {1: Apply, 2: E, 3: V}
