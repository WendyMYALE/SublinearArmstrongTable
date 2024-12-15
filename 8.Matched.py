## Matched Pair
import datetime
import math
import copy

import ClassSet
import FunctionSet
import Function4Null
import Sequence

def PairAssign(A, As, Aw, pKey, cKey, R, W, m, n):
    """
    :param A: Paired agree sets
    :param As: Rest strong agree sets
    :param Aw: Rest weak agree sets
    :param pKey: Possible keys
    :param cKey: Certain keys
    :param R: Attributes set (schema)
    :param W: Null set
    :param m: Number of all strong agree sets
    :param n: Number of all weak agree sets
    :return: 1. Armstrong Table exists - True or False
             2. Edge list
             3. Vertex matrix
    """

    p = 0   # Flag to print for debugging

    s = max(math.ceil((1 + math.sqrt(1 + 8 * m)) / 2), 3)
    E = ClassSet.EdgeList(s)
    V = [[-1 if i == 1 else 1 for i in W] for j in range(s)]  ## initial with -1, 0 as Null, 1 as Not Null

    if len(A) > 0:
        ## Assign first set pair
        E.SetValue(0, "Assigned", 2)
        E.SetValue(0, "AttrSet", A[0][0])
        for i in range(len(R)):
            if R[i] in A[0][0]:
                V[0][i] = 1
                V[1][i] = 1
            elif R[i] in A[0][1] and W[i] == 1:
                V[0][i] = 0
        w = Function4Null.NullAttr(FunctionSet.Subtract(FunctionSet.Subtract(A[0][1], A[0][0]), E.GetValue(0, "AttrSet")),
                               R, W)[1]
        Wn = [e - f for e, f in zip(W, w)]
        if p: print("First set pair", A[0], "applied on Edge 0:", E.GetValue(0, "Nodes"))
        del A[0]
        Apply = True
        if p:
            E.print()
            print(V)
    else:
        k = s

    if len(A) > 0:
        ## Armstrong table for matched set pairs
        for k in range(s, m + 2):
            if k > s:
                newE = ClassSet.EdgeList(k)
                for i in range(int(s * (s - 1) / 2)):
                    newE.SetValue(i, "Assigned", E.GetValue(i, "Assigned"))
                    newE.SetValue(i, "AttrSet", E.GetValue(i, "AttrSet"))

                V.append([-1 if i == 1 else 1 for i in W])
                E = copy.deepcopy(newE)

            if p: print("Matched set pairs - trying {} tuples table ....".format(k))
            outcome = Function4Null.Armstrong4A(E, V, A, R, pKey, cKey, W)
            Apply = outcome[1]
            E = outcome[2]
            V = outcome[3]

            if Apply: break
    else:
        k = s

    s = k
    print("{} tuples table for matched set pairs".format(s))
    E.print()
    print(V)

    if len(As) > 0:
        ## Armstrong table for strong agree sets
        for k in range(s, m + 2):
            if k > s:
                newE = ClassSet.EdgeList(k)
                for i in range(int(s * (s - 1) / 2)):
                    newE.SetValue(i, "Assigned", E.GetValue(i, "Assigned"))
                    newE.SetValue(i, "AttrSet", E.GetValue(i, "AttrSet"))

                V.append([-1 if i == 1 else 1 for i in W])
                E = copy.deepcopy(newE)

            if p: print("Strong agree sets - trying {} tuples table ....".format(k))
            outcome = Function4Null.Armstrong4As(E, V, As, R, pKey)
            Apply = outcome[1]
            E = outcome[2]
            V = outcome[3]

            if Apply: break

    s = k
    print("{} tuples table for strong agree sets".format(s))
    E.print()
    print(V)

    if len(Aw) > 0:
        ## Armstrong table for weak agree sets
        for k in range(s, m + 1 + 2 * n):
            if k > s:
                newE = ClassSet.EdgeList(k)
                for i in range(int(s * (s - 1) / 2)):
                    newE.SetValue(i, "Assigned", E.GetValue(i, "Assigned"))
                    newE.SetValue(i, "AttrSet", E.GetValue(i, "AttrSet"))

                V.append([-1 if i == 1 else 1 for i in W])
                E = copy.deepcopy(newE)

            if p: print("Weak agree sets - trying {} tuples table ....".format(k))
            outcome = Function4Null.Armstrong4Aw(E, V, Aw, R, cKey, W)
            Apply = outcome[1]
            E = outcome[2]
            V = outcome[3]

            if Apply: break

    s = k
    print("{} tuples table for weak agree sets".format(s))
    E.print()
    print(V)

    Wn = W
    Wm = []
    for i in range(len(V)):
        Wn = [a * b for a, b in zip(V[i], Wn)]
    for j in range(len(W)):
        Wm.append((j + 1) * Wn[j])
    if Apply and sum(Wm) == 0:
        print("{} tuples Armstrong table can be built as:".format(s))
    elif Apply and 1 in Wn:
        W1 = [abs(a * b) for a, b in zip(W, Wn)]
        NewGraph = Function4Null.ExtraTuple(E, V, W1)
        E = NewGraph[1]
        V = NewGraph[2]
        print("Extra tuple required. {} tuples Armstrong table can be built as:".format(s + 1))
    elif Apply and -1 in Wn:
        if p: print("Same size adding more NULL")
        V1 = copy.deepcopy(V)
        vList = []
        for i in range(len(Wn)):
            if Wn[i] == -1:
                for j in range(len(V1)):
                    if V1[j][i] == -1:
                        V1[j][i] = 0
                        vList.append(j)
                        break
        if len(cKey) == 0:
            V = copy.deepcopy(V1)
        elif Function4Null.AwCheck(E, V1, R, cKey, vList):
            V = copy.deepcopy(V1)
        else:
            W1 = [abs(a * b) for a, b in zip(W, Wn)]
            NewGraph = Function4Null.ExtraTuple(E, V, W1)
            E = NewGraph[1]
            V = NewGraph[2]
            print("Extra tuple required. {} tuples Armstrong table can be built as:".format(s + 1))
    else:
        print('No sublinear Armstrong table exists!')

    return{1: Apply, 2: E, 3: V}

filename = 'Hockey.Goalies.main'
path_in = "/Users/wye1/Documents/Experiments/DataSets/Hocky_Parameters/"
path_out = "/Users/wye1/Documents/Experiments/8-Sublinear+Null/Output/"
OutFile = path_out + filename + '_Mat.txt'
ToDebug = False

## Main
if __name__ == "__main__":
    para = Function4Null.FindParameters(path_in + filename)
    R = para[1]
    StrongAS = para[2]
    WeakAS = para[3]
    pKey = para[4]
    cKey = para[5]
    W = para[6]

    Start = datetime.datetime.now()

    w = [str(i) for i in W] ## Convert to strings
    WList = "".join(w) ## Single string

    ## Match strong and weak agree sets
    m = len(StrongAS)
    n = len(WeakAS)
    A = []
    As = StrongAS.copy()
    Aw = WeakAS.copy()
    for i in range(n):
        for j in range(m):
            #mask = FunctionSet.StringToBit(R, FunctionSet.Subtract(WeakAS[i], StrongAS[j]))
            if FunctionSet.Subset(StrongAS[j], WeakAS[i]) and StrongAS[j] in As and WeakAS[i] in Aw \
                    and len(FunctionSet.Subtract(Function4Null.NullAttr(WeakAS[i], R, W)[2], StrongAS[j])) == 0 \
                    and WeakAS[i] != StrongAS[j]:
                #and int(mask, 2) & int(WList, 2) > 0:
                A.append((StrongAS[j],WeakAS[i]))
                As.remove(StrongAS[j])
                Aw.remove(WeakAS[i])

    print("Matched sets:", A, "; Rest strong sets:", As, "; Rest weak sets:", Aw)

    Result = PairAssign(A, As, Aw, pKey, cKey, R, W, m, n)
    Apply = Result[1]
    E = Result[2]
    V = Result[3]

    if Apply:
        Ep = copy.deepcopy(E)
        for k in range(Ep.length()):
            Ep.SetValue(k, "AttrSet", Ep.GetValue(k, "AttrSet") + '+' + Function4Null.WeakAS(E, V, R, k))
        Ep.print()
        for i in range(len(V)): print(V[i])

    End = datetime.datetime.now()
    print("Total time of running: {}".format(End - Start))

    if Apply:
        with open(OutFile, "w") as text_file:
            print('For dataset {}: '.format(filename), sep="\n", file=text_file)
            print('{} tuples Armstrong Table can be built as'.format(Ep.ActualSize()), sep="\n", file=text_file)
        Ep.export(OutFile)
        with open(OutFile, "a") as text_file:
            for i in range(len(V)): print(V[i], sep="\n", file=text_file)
            print("Time of running {}:".format(End - Start), sep="\n", file=text_file)
    else:
        with open(OutFile, "w") as text_file:
            print('No sublinear Armstrong Table exists!', sep="\n", file=text_file)

