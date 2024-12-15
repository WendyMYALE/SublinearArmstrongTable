## Most Matched
import datetime
import math
import copy

import ClassSet
import FunctionSet
import Function4Null
import Sequence
import Matched

## Main
if __name__ == "__main__":
    p = 1  # Flag to print for debugging

    FileName = 'Hockey.Goalies.main'
    para = TableWithNull.FindParameters(FileName)
    R = para[1]
    StrongAS = para[2]
    WeakAS = para[3]
    pKey = para[4]
    cKey = para[5]
    W = para[6]

    Start = datetime.datetime.now()

    ## Find most matched strong and weak agree sets
    m = len(StrongAS)
    n = len(WeakAS)
    A = []
    A1 = []
    As = StrongAS.copy()
    Aw = WeakAS.copy()
    As2Del = []
    Aw2Del = []
    for i in range(n):
        for j in range(m):
            if j not in As2Del and i not in Aw2Del and FunctionSet.Subset(StrongAS[j], WeakAS[i]) \
                    and len(FunctionSet.Subtract(Function4Null.NullAttr(WeakAS[i], R, W)[2], StrongAS[j])) == 0 \
                    and WeakAS[i] != StrongAS[j]:
                A.append((StrongAS[j],WeakAS[i]))
                As2Del.append(j)
                Aw2Del.append(i)
                l1 = [item for item in A1 if StrongAS[j] in item]
                l2 = [item for item in A1 if WeakAS[i] in item]
                for g in range(len(l1)): A1.remove(l1[g])
                for h in range(len(l2)): A1.remove(l2[h])
            elif j not in As2Del and i not in Aw2Del and FunctionSet.Subset(StrongAS[j], Function4Null.NullAttr(WeakAS[i], R, W)[2]):
                ma = FunctionSet.Match(Function4Null.NullAttr(WeakAS[i], R, W)[2], StrongAS[j], R)
                if ma > 1:
                    l1 = [item for item in A1 if StrongAS[j] in item]
                    l2 = [item for item in A1 if WeakAS[i] in item]
                    if len(l1) > 0 and ma > l1[0][2]:
                        A1.remove(l1[0])
                        A1.append((StrongAS[j], WeakAS[i], ma))
                    elif len(l2) > 0 and ma > l2[0][2]:
                        A1.remove(l2[0])
                        A1.append((StrongAS[j], WeakAS[i], ma))
                    else:
                        A1.append((StrongAS[j], WeakAS[i], ma))

    for i in range(len(A1)):
        A.append((A1[i][0], A1[i][1]))
        if A1[i][0] in As: As.remove(A1[i][0])
        if A1[i][1] in Aw: Aw.remove(A1[i][1])

    for j in range(len(A)):
        if A[j][0] in As: As.remove(A[j][0])
        if A[j][1] in Aw: Aw.remove(A[j][1])

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