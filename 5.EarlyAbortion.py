import datetime
import copy
import math
import logging

import ClassSet
import FunctionSet
import ATMining

#logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.WARNING)
logging.getLogger('FindArmstrong').setLevel(logging.DEBUG);

def FindArmstrong(E, AS, R, AgreeSets, boundary, depth=0):
    """
    :param E: Edge list
    :param AS: Agree set list with assignment status
    :param R: Attributes set (schema)
    :param AgreeSets: Entire agree sets
    :param boundary: Boundary of size for searching Armstrong table
    :return: 1. Armstrong Table exists - True or False
             2. Edge list
             3. Agree set list with assignment status
     """

    logger = logging.getLogger('FindArmstrong')

    for k in range(E.length()):
        if E.GetValue(k, "Assigned") == 0 and len(E.GetValue(k, "AttrSet")) == 0:
            ## Unassgined, no forced edge generated
            for i in range(len(AS)):
                if AS[i][1] == 0 and E.GetValue(k, "Assigned") == 0:
                    if ToDebug: print("Applying agree set", i, AS[i][0], "on Edge:", k, E.GetValue(k, "Nodes"))
                    E1 = copy.deepcopy(E)
                    AS1 = copy.deepcopy(AS)
                    #E1.SetValue(k, "AttrSet", AS1[i][0])
                    #result = FunctionSet.EdgeCheck(E1, R, AgreeSets)
                    result = FunctionSet.CliqueCheck(E1, R, AgreeSets, AS1[i][0], E.GetValue(k, "Nodes"))
                    Apply = result[1]
                    E1 = result[2]

                    if Apply:
                        if ToDebug: print("Applied agree set", i, AS1[i], "on Edge:", k, E1.GetValue(k, "Nodes"), "successfully : )")
                        E1.SetValue(k, "AttrSet", AS1[i][0])
                        E1.SetValue(k, "Assigned", 1)
                        AS1[i][1] = 1
                        #E1.print()

                        if sum(x.count(0) for x in AS1) > 0:
                            #print("Before: AS {}".format(AS))
                            #print("Before: AS1 {}".format(AS1))
                            #print("Before: Apply is {}, k: {}, Boundary: {}, Depth: {}".format(Apply, k, boundary, depth))
                            output = FindArmstrong(E1, AS1, R, AgreeSets, boundary, depth + 1)
                            Apply = output[1]
                            E1 = output[2]
                            AS1 = output[3]
                        #else:
                            #print("Bottom: AS {}".format(AS))
                            #print("Bottom: AS1 {}".format(AS1))
                            #print("Bottom: Apply is {}, k: {}, Boundary: {}, Depth: {}".format(Apply, k, boundary, depth))
                    #else:
                        #print("Applied agree set", i, AS1[i][0], "on Edge:", k, E1.GetValue(k, "Nodes"), "failed : (")

                    n = E1.ActualSize()
                    #print("After: AS {}".format(AS))
                    #print("After: AS1 {}".format(AS1))
                    #print("After: Apply is {}, k: {}, Boundary: {}, Actual size: {}, Depth: {}".format(Apply, k, boundary, n, depth))

                    if Apply:
                        if n < boundary and n >= math.ceil((1 + math.sqrt(1 + 8 * len(AgreeSets))) / 2):
                            return {1: Apply, 2: E1, 3: AS1}
                        elif sum(x.count(0) for x in AS1) == 0:
                            boundary = n - 1
                            E.resize(n - 1)
                            return {1: False, 2: E, 3: AS}
        elif E.GetValue(k, "Assigned") == 0 and len(E.GetValue(k, "AttrSet")) > 0:
            ## Unassgined, forced edge generated
            ms = 0
            msi = -1
            for i in range(len(AS)):
                if FunctionSet.MatchSize(E.GetValue(k, "AttrSet"), AS[i][0]) > ms and AS[i][1] == 0 and E.GetValue(k, "Assigned") == 0:
                    ms = FunctionSet.MatchSize(E.GetValue(k, "AttrSet"), AS[i][0])
                    msi = i
                    if ToDebug: print("Forced edge exists on edge", k, ", agree set", i, AS[i][0], "matchs", ms, "attributes")
                elif AS[i][1] == 0 and E.GetValue(k, "Assigned") == 0:  ## AS[i] is not superset of forced edge
                    Apply = False
                    if ToDebug: print("Forced edge exists on edge", k, ", agree set", i, AS[i][0], "is not superset")

            if msi > -1:
                if ToDebug: print("Applying agree set", msi, AS[msi][0], "on Edge:", k, E.GetValue(k, "Nodes"))
                E1 = copy.deepcopy(E)
                AS1 = copy.deepcopy(AS)
                #E1.SetValue(k, "AttrSet", AS1[i][0])
                #result = FunctionSet.EdgeCheck(E1, R, AgreeSets)
                result = FunctionSet.CliqueCheck(E1, R, AgreeSets, AS1[msi][0], E.GetValue(k, "Nodes"))
                Apply = result[1]
                E1 = result[2]

                if Apply:
                    if ToDebug: print("Applied agree set", msi, AS1[msi], "on Edge:", k, E1.GetValue(k, "Nodes"), "successfully : )")
                    E1.SetValue(k, "AttrSet", AS1[msi][0])
                    E1.SetValue(k, "Assigned", 1)
                    AS1[msi][1] = 1
                    #E1.print()

                    if sum(x.count(0) for x in AS1) > 0:
                        #print("Before: AS {}".format(AS))
                        #print("Before: AS1 {}".format(AS1))
                        #print("Before: Apply is {}, k: {}, Boundary: {}, Depth: {}".format(Apply, k, boundary, depth))
                        output = FindArmstrong(E1, AS1, R, AgreeSets, boundary, depth + 1)
                        Apply = output[1]
                        E1 = output[2]
                        AS1 = output[3]
                    #else:
                        #print("Bottom: AS {}".format(AS))
                        #print("Bottom: AS1 {}".format(AS1))
                        #print("Bottom: Apply is {}, k: {}, Boundary: {}, Depth: {}".format(Apply, k, boundary, depth))
                else:
                    if ToDebug: print("Applied agree set", msi, AS1[msi][0], "on Edge:", k, E1.GetValue(k, "Nodes"), "failed : (")

                n = E1.ActualSize()
                #print("After: AS {}".format(AS))
                #print("After: AS1 {}".format(AS1))
                #print("After: Apply is {}, k: {}, Boundary: {}, Actual size: {}, Depth: {}".format(Apply, k, boundary, n, depth))

                if Apply:
                    if n < boundary and n >= math.ceil((1 + math.sqrt(1 + 8 * len(AgreeSets))) / 2):
                        return {1: Apply, 2: E1, 3: AS1}
                    elif sum(x.count(0) for x in AS1) == 0:
                        boundary = n - 1
                        E.resize(n - 1)
                        return {1: False, 2: E, 3: AS}

    if not Apply:
        return {1: Apply, 2: E, 3: AS}

filename = 'Table_c20r15'
path_in = "/Users/wye1/Documents/Experiments/DataSets/naumann_small/"
path_m = "/Users/wye1/Documents/Experiments/DataSets/RandomTables/"
path_out = "/Users/wye1/Documents/Experiments/5-Sublinear/Output/"
DataFile = path_in + filename + '.csv'
ASFile = path_m + filename + '.txt'
OutFile = path_out + filename + '_Abort.txt'
Mining = False
ToDebug = False

## Main
if __name__ == "__main__":
    if Mining:
        ATM = ATMining.ATMining(DataFile)
        AgSList = ATM[1]
        R = ATM[2]
    else:
        file = open(ASFile, 'r')
        AgSList = []
        for line in file:
            AgSList.append(line.rstrip())

        R = []
        for i in range(len(AgSList[0])):
            R.append('C' + str(i + 1) + '~')

    AgreeSets = []
    for i in range(len(AgSList)):
        AgreeSets.append(FunctionSet.BitToString(R, AgSList[i]))
    print("Schema R:", R)
    print("Agree Sets (", len(AgreeSets), "):")
    if len(AgreeSets) < 11: print(AgreeSets)

    m = len(AgreeSets)
    E = ClassSet.EdgeList(m)
    AS  = [['', 0] for x in range(m)]
    for i in range(m):
        AS[i][0] = AgreeSets[i]
    #AS = sorted(AS)
    #AS = FunctionSet.RandomList(AS)

    Start = datetime.datetime.now()

    ## First agree set assigned to first edge
    E.SetValue(0, "Assigned", 1)
    E.SetValue(0, "AttrSet", AS[0][0])
    if ToDebug: print("First Agree Set 0", AS[0][0], "applies on Edge 0:", E.GetValue(0, "Nodes"))
    AS[0][1] = 1

    outcome = FindArmstrong(E, AS, R, AgreeSets, m)
    Apply = outcome[1]
    E = outcome[2]

    if Apply:
        n = E.ActualSize()
        print('For dataset {}, {} agree sets: '.format(filename, len(AgreeSets)))
        print(n, 'tuples Armstrong Table can be built with CWMostMatch')
    else:
        print('No sublinear Armstrong DB exists!')

    End = datetime.datetime.now()
    print("Time of running {}:".format(End - Start))

    if Apply:
        with open(OutFile, "w") as text_file:
            print('For dataset {}, {} agree sets: '.format(filename, len(AgreeSets)), sep="\n", file=text_file)
            print('{} tuples Armstrong Table can be built with Early Abortion'.format(n), sep="\n", file=text_file)
        E.export(OutFile)
        with open(OutFile, "a") as text_file:
            print("Time of running {}:".format(End - Start), sep="\n", file=text_file)
    else:
        with open(OutFile, "w") as text_file:
            print('No sublinear Armstrong DB exists!')

