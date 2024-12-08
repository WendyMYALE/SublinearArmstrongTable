## HopcroftKarp maximum matching
import datetime
import math
import copy
from hopcroftkarp import HopcroftKarp

import ClassSet
import FunctionSet
import Function4Null
import TableWithNull
import TableWithNull1

## Main
if __name__ == "__main__":
    p = 1  # Flag to print for debugging

    FileName = 'Hockey.TeamsPost_Pri'
    para = TableWithNull.FindParameters(FileName)
    R = para[1]
    StrongAS = para[2]
    WeakAS = para[3]
    pKey = para[4]
    cKey = para[5]
    W = para[6]

    Start = datetime.datetime.now()

    ## Find maximum matching strong and weak agree sets
    m = len(StrongAS)
    n = len(WeakAS)
    bg = {}
    A = []
    As = StrongAS.copy()
    Aw = WeakAS.copy()
    for i in range(m):
        for j in range(n):
            if FunctionSet.Subset(StrongAS[i], WeakAS[j]) and len(FunctionSet.Subtract(Function4Null.NullAttr(WeakAS[j], R, W)[2], StrongAS[i])) == 0:
                if StrongAS[i] not in bg.keys():
                    bg[StrongAS[i]] = {WeakAS[j]}
                else:
                    bg[StrongAS[i]].add(WeakAS[j])

    mm = HopcroftKarp(bg).maximum_matching()
    for k in mm.keys():
        if k in StrongAS:
            A.append((k, mm[k]))
            As.remove(k)
            Aw.remove(mm[k])

    print("Matched sets:", A, "; Rest strong sets:", As, "; Rest weak sets:", Aw)

    Result = TableWithNull1.PairAssign(A, As, Aw, pKey, cKey, R, W, m, n)
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