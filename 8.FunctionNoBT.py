import copy

import FunctionSet
import Function4Null

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
                result = Function4Null.AssignStrongAS(E, V, As[0], R, pKey, E.GetValue(k, "Nodes"))
                Apply = result[1]
                E = result[2]
                V = result[3]

                if Apply:
                    if ToDebug: print("Applied agree set", As[0], "on Edge:", k, E.GetValue(k, "Nodes"), "successfully : )")
                    E.SetValue(k, "AttrSet", As[0])
                    E.SetValue(k, "Assigned", 1)

                    for i in range(len(R)):
                        if R[i] in As[0]:
                            V[E.GetValue(k, "Nodes")[0]][i] = 1
                            V[E.GetValue(k, "Nodes")[1]][i] = 1

                    del As[0]
                    if ToDebug: E.print()

                    if len(As) > 0:
                        if ToDebug: print("Before: As {}".format(As))
                        if ToDebug: print("Before: Apply is {}, k: {}, Depth: {}".format(Apply, k, depth))
                        output = Armstrong4As(E, V, As, R, pKey, depth + 1)
                        Apply = output[1]
                        E = output[2]
                        V = output[3]
                        if ToDebug: E.print()

                    n = E.ActualSize()
                    if ToDebug: print("After: As {}".format(As))
                    if ToDebug: print("After: Apply is {}, k: {}, Actual size: {}, Depth: {}".format(Apply, k, n, depth))

                    if Apply: return {1: Apply, 2: E, 3: V}
                else:
                    if ToDebug: print("Applied agree set", As[0], "on Edge:", k, E.GetValue(k, "Nodes"), "failed : (")
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
    ToDebug = 0

    for k in range(E.length()):
        AttrSet = E.GetValue(k, "AttrSet") + Function4Null.WeakAS(E, V, R, k)
        ## Aw[0] forced on k
        if FunctionSet.Subtract(AttrSet, Aw[0]) == "" and FunctionSet.Subtract(Aw[0], AttrSet) == "" and E.GetValue(k, "Assigned") < 2:
            Apply = True
            E.SetValue(k, "Assigned", E.GetValue(k, "Assigned") + 1)
            if ToDebug: print("Weak agree set", Aw[0], "is already on Edge:", k, E.GetValue(k, "Nodes"), ": )")
        ## Edge assignable
        elif E.GetValue(k, "Assigned") < 2 and FunctionSet.Subset(E.GetValue(k, "AttrSet") + Function4Null.WeakAS(E, V, R, k), Aw[0]):
            w = Function4Null.NullAttr(FunctionSet.Subtract(Aw[0], E.GetValue(k, "AttrSet")), R, W)[1]
            if sum(w) != 0:
                if ToDebug: print("Applying weak agree set", Aw[0], "on Edge:", k, E.GetValue(k, "Nodes"))
                e = E.GetValue(k, "Nodes")
                Vx = copy.deepcopy(V)

                if [- c * d for c, d in zip(Vx[e[0]], w)] == w or [- c * d for c, d in zip(Vx[e[1]], w)] == w:
                    ## e[0] or e[1] allow Nulls required
                    if [- c * d for c, d in zip(Vx[e[0]], w)] == w:
                        ## Set Nulls for e[0]
                        for i in range(len(w)):
                            if w[i] == 1 and Vx[e[0]][i] == -1:
                                Vx[e[0]][i] = 0
                        if ToDebug: print("Null on vertex", e[0], Vx[e[0]])
                    else:
                        ## Set Nulls for e[1]
                        for i in range(len(w)):
                            if w[i] == 1 and Vx[e[1]][i] == -1:
                                Vx[e[1]][i] = 0
                        if ToDebug: print("Null on", e[1], Vx[e[1]])

                    result = Function4Null.AssignWeakAS(E, Vx, Aw[0], R, cKey, k)
                    Apply = result[1]
                    E = result[2]
                    Vx = result[3]

                    if Apply:
                        if ToDebug: print("Applied weak agree set", Aw[0], "on Edge:", k, E.GetValue(k, "Nodes"), "successfully : )")
                        V = copy.deepcopy(Vx)
                        E.SetValue(k, "AttrSet", FunctionSet.Subtract(Aw[0], Function4Null.WeakAS(E, V, R, k)))
                        E.SetValue(k, "Assigned", E.GetValue(k, "Assigned") + 1)
                    else:
                        if ToDebug: print("Applied weak agree set", Aw[0], "on Edge:", k, E.GetValue(k, "Nodes"), "failed : (")
                else:  ## Not enough attributes allow Nulls
                    Apply = False
                    if ToDebug:
                        print("Not enough attributes allow Nulls on Edge:", k)
                        if k == 244: print(V)
            else:
                Apply = False
                if ToDebug: print("No Null allows on Edge:", k, E.GetValue(k, "Nodes"), "for weak agree set", Aw[0])
        else:  ## Aw[0] failed applying on k
            Apply = False

        if Apply:
            del Aw[0]
            n = E.ActualSize()
            if ToDebug and n < 10: E.print()
            if ToDebug and n < 10: print(V)

            if len(Aw) > 0:
                if ToDebug: print("Before: Aw {}".format(Aw))
                if ToDebug: print("Before: Apply is {}, k: {}, Depth: {}".format(Apply, k, depth))
                output = Armstrong4Aw(E, V, Aw, R, cKey, W, depth + 1)
                Apply = output[1]
                E = output[2]
                V = output[3]
                if ToDebug: E.print()
                if ToDebug: print(V)

            if ToDebug and n < 10: print("After: Aw {}".format(Aw))
            if ToDebug and n < 10: print("After: Apply is {}, k: {}, Actual size: {}, Depth: {}".format(Apply, k, n, depth))

            if Apply:
                return {1: Apply, 2: E, 3: V}

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
                and FunctionSet.Subset(E.GetValue(k, "AttrSet") + Function4Null.WeakAS(E, V, R, k), A[0][1]):
            ## Edge assignable
            e = E.GetValue(k, "Nodes")
            w0 = Function4Null.NullAttr(FunctionSet.Subtract(A[0][1], A[0][0]), R, W)[1]
            w = Function4Null.NullAttr(FunctionSet.Subtract(FunctionSet.Subtract(A[0][1], A[0][0]), E.GetValue(k, "AttrSet")), R, W)[1]
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
                if ToDebug: print("Applied agree set pair", A[0], "on Edge:", k, E.GetValue(k, "Nodes"))

                ## Check strong agree set
                AsB = []
                AsBit = FunctionSet.StringToBit(R, A[0][0])
                AsB[:0] = AsBit  ## Separated bits
                AsBI = [int(i) for i in AsB]  ## Convert to numbers

                if AsBI != [abs(a) * b for a, b in zip(V[e[0]], AsBI)] or AsBI != [abs(a) * b for a, b in zip(V[e[1]], AsBI)]:
                    ## Null value on attribute of strong agree set
                    Apply = False
                else:
                    result = Function4Null.AssignStrongAS(E, V, A[0][0], R, pKey, E.GetValue(k, "Nodes"))
                    Apply = result[1]
                    E = result[2]
                    V = result[3]

                if Apply:
                    if Nil == 1:
                        if ToDebug: print("Utilize existing Null")
                    elif [- c * d for c, d in zip(V[e[0]], w)] == w:
                        ## Set Nulls for e[0]
                        for i in range(len(w)):
                            if w[i] == 1 and V[e[0]][i] == -1:
                                V[e[0]][i] = 0
                        if ToDebug: print("Null on vertex", e[0], V[e[0]])
                    else:
                        ## Set Nulls for e[1]
                        for i in range(len(w)):
                            if w[i] == 1 and V[e[1]][i] == -1:
                                V[e[1]][i] = 0
                        if ToDebug: print("Null on", e[1], V[e[1]])

                    result = Function4Null.AssignWeakAS(E, V, A[0][1], R, cKey, k)
                    Apply = result[1]
                    E = result[2]
                    V = result[3]

                    if Apply:
                        if ToDebug: print("Applied agree set pair", A[0], "on Edge:", k, E.GetValue(k, "Nodes"), "successfully : )")
                        E.SetValue(k, "AttrSet", FunctionSet.Subtract(A[0][1], Function4Null.WeakAS(E, V, R, k)))
                        E.SetValue(k, "Assigned", E.GetValue(k, "Assigned") + 2)

                        del A[0]
                        if ToDebug: E.print()
                        if ToDebug: print("V:", V)

                        if len(A) > 0:
                            if ToDebug: print("Before: A {}".format(A))
                            if ToDebug: print("Before: Apply is {}, k: {}, Depth: {}".format(Apply, k, depth))
                            output = Armstrong4A(E, V, A, R, pKey, cKey, W, depth + 1)
                            Apply = output[1]
                            E = output[2]
                            V = output[3]

                            if ToDebug: E.print()
                            if ToDebug: print(V)

                        n = E.ActualSize()
                        if ToDebug: print("After: A {}".format(A))
                        if ToDebug: print("After: Apply is {}, k: {}, Actual size: {}, Depth: {}".format(Apply, k, n, depth))

                        if Apply: return {1: Apply, 2: E, 3: V}
                    else:
                        if ToDebug: print("Applied weak agree set", A[0][1], "on Edge:", k, E.GetValue(k, "Nodes"), "failed : (")
                else: ## Strong agree set failed to assign
                    Apply = False
                    if ToDebug: print("Applied strong agree set", A[0][0], "on Edge:", k, E.GetValue(k, "Nodes"), "failed : (")
            else:
                Apply = False
                if ToDebug: print("Not enough attributes allow Nulls on Edge:", k)
        else:
            Apply = False
            if ToDebug: print("Edge", k, "is unassignable")

    if not Apply: return {1: Apply, 2: E, 3: V}
