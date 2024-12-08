## Sequence
import datetime
import math
import copy

import ClassSet
import Function4Null
import FunctionNoBT

filename = 'Hockey.Teams.main'
path_in = "/Users/wye1/Documents/Experiments/DataSets/Hocky_Parameters/"
path_out = "/Users/wye1/Documents/Experiments/8-Sublinear+Null/Output/"
OutFile = path_out + filename + '_seq.txt'
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

    ## Armstrong table for strong agree sets
    m = len(StrongAS)
    n = len(WeakAS)
    for k in range(math.ceil((1 + math.sqrt(1 + 8 * m)) / 2), m + 2):
        if math.ceil((1 + math.sqrt(1 + 8 * m)) / 2) < 3:
            k = 3
        if ToDebug: print("Strong agree sets - trying {} tuples table ....".format(k))
        E = ClassSet.EdgeList(k)
        V = [[-1 if i == 1 else 1 for i in W] for j in range(k)] ## initial with -1, 0 as Null, 1 as Not Null
        As = StrongAS.copy()

        ## First agree set assigned to first edge
        E.SetValue(0, "Assigned", 1)
        E.SetValue(0, "AttrSet", As[0])
        for i in range(len(R)):
            if R[i] in As[0]:
                V[0][i] = 1
                V[1][i] = 1
        if ToDebug: print("First Strong Agree Set 0", As[0], "applied on Edge 0:", E.GetValue(0, "Nodes"))
        del As[0]

        if len(As) == 0:
            Apply = True
        else:
            outcome = FunctionNoBT.Armstrong4As(E, V, As, R, pKey)
            Apply = outcome[1]
            E = outcome[2]
            V = outcome[3]

        if Apply: break

    s = k
    if Apply: print("{} tuples table for strong agree sets".format(s))
    if s < 10:
        E.print()
        print(V)

    Aw = WeakAS.copy()
    for k in range(s, m + 1 + 2 * n):
        if k > s:
            newE = ClassSet.EdgeList(k)
            for i in range(int(s * (s - 1) / 2)):
                newE.SetValue(i, "Assigned", E.GetValue(i, "Assigned"))
                newE.SetValue(i, "AttrSet", E.GetValue(i, "AttrSet"))

            V.append([-1 if i == 1 else 1 for i in W])
            E = copy.deepcopy(newE)

        if ToDebug: print("Weak agree sets - trying {} tuples table ....".format(k))

        outcome = FunctionNoBT.Armstrong4Aw(E, V, Aw, R, cKey, W)
        Apply = outcome[1]
        E = outcome[2]
        V = outcome[3]

        if Apply: break

    s = k
    if Apply: print("{} tuples table for weak agree sets".format(s))
    if s < 10:
        E.print()
        print(V)

    Wn = W
    Wm = []
    for i in range(len(V)):
        Wn = [a * b for a, b in zip(V[i], Wn)]
    for j in range(len(W)):
        Wm.append((j + 1) * Wn[j])
    if (Apply and sum(Wm) == 0):
        print("No extra tuple for mandatory NULL required.")
    elif Apply and 1 in Wn:
        W1 = [abs(a * b) for a, b in zip(W, Wn)]
        NewGraph = Function4Null.ExtraTuple(E, V, W1)
        E = NewGraph[1]
        V = NewGraph[2]
        s = s + 1
        print("Extra tuple required. {} tuples Armstrong table can be built as:".format(s))
    elif Apply and -1 in Wn:
        if ToDebug: print("Same size adding more NULL")
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

    if Apply:
        Ep = copy.deepcopy(E)
        for k in range(Ep.length()):
            Ep.SetValue(k, "AttrSet", Ep.GetValue(k, "AttrSet") + '+' + Function4Null.WeakAS(E, V, R, k))
        print("Final table size ", s)
        if s < 10:
            Ep.print()
            for i in range(len(V)): print(V[i])

    End = datetime.datetime.now()
    print("Total time of running: {}".format(End - Start))

    if Apply:
        with open(OutFile, "w") as text_file:
            print('For dataset {}: '.format(filename), sep="\n", file=text_file)
            print('{} tuples Armstrong Table can be built as'.format(s), sep="\n", file=text_file)
        Ep.export(OutFile)
        with open(OutFile, "a") as text_file:
            for i in range(len(V)): print(V[i], sep="\n", file=text_file)
            print("Time of running {}:".format(End - Start), sep="\n", file=text_file)
    else:
        with open(OutFile, "w") as text_file:
            print('No sublinear Armstrong Table exists!', sep="\n", file=text_file)
