import datetime
import copy
import csv
import logging

import ClassSet
import FunctionSet
import ATMining

#logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.WARNING)
logging.getLogger('FindArmstrong').setLevel(logging.DEBUG);

def FindArmstrong(E, AS, R, AgreeSets, depth=0):
    """
    :param E: Edge list
    :param AS: Remained agree sets
    :param R: Attributes set (schema)
    :param AgreeSets: Entire agree sets
    :return: 1. Armstrong Table exists - True or False
             2. Edge list
     """

    logger = logging.getLogger('FindArmstrong')

    for k in range(E.length()):
        ## Unassgined edge
        if E.GetValue(k, "Assigned") == 0:
            if ToDebug: print("Applying agree set", AS[0], "on Edge:", k, E.GetValue(k, "Nodes"))
            if FunctionSet.Subset(E.GetValue(k, "AttrSet"), AS[0]):
            ## No forced edge generated or AS[0] is superset of forced edge
                E1 = copy.deepcopy(E)
                AS1 = AS.copy()
                result = FunctionSet.CliqueCheck(E1, R, AgreeSets, AS1[0], E.GetValue(k, "Nodes"))
                Apply = result[1]
                E1 = result[2]

                if Apply:
                    if ToDebug: print("Applied agree set", AS1[0], "on Edge:", k, E1.GetValue(k, "Nodes"), "successfully : )")
                    E1.SetValue(k, "AttrSet", AS1[0])
                    E1.SetValue(k, "Assigned", 1)
                    del AS1[0]

                    if len(AS1) > 0:
                        #print("Before: AS {}".format(AS))
                        #print("Before: AS1 {}".format(AS1))
                        if ToDebug: print("Before: Apply is {}, k: {}, Depth: {}".format(Apply, k, depth))
                        output = FindArmstrong(E1, AS1, R, AgreeSets, depth + 1)
                        Apply = output[1]
                        E1 = output[2]
                        if ToDebug: E1.print()

                    n = E1.ActualSize()
                    #print("After: AS {}".format(AS))
                    #print("After: AS1 {}".format(AS1))
                    if ToDebug: print("After: Apply is {}, k: {}, Actual size: {}, Depth: {}".format(Apply, k, n, depth))

                    return {1: Apply, 2: E1}
                else:
                    if ToDebug: print("Applied agree set", AS1[0], "on Edge:", k, E1.GetValue(k, "Nodes"), "failed : (")
            else:  ## AS[0] is not superset of forced edge
                Apply = False
                if ToDebug: print("Forced edge exists, applied agree set", AS[0], "on Edge:", k, E.GetValue(k, "Nodes"), "failed : (")

    if not Apply: return {1: Apply, 2: E}

filename = 'Table_c20r15'
path_in = "/Users/wye1/Documents/Experiments/DataSets/naumann_small/"
path_m = "/Users/wye1/Documents/Experiments/DataSets/RandomTables/"
path_out = "/Users/wye1/Documents/Experiments/5-Sublinear/Output/"
DataFile = path_in + filename + '.csv'
ASFile = path_m + filename + '.txt'
OutFile = path_out + filename + '_Ran.txt'
Mining = False
ToDebug = False
rep = 10

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

    Start = datetime.datetime.now()

    m = len(AgreeSets)
    AS0 = AgreeSets.copy()
    Es = ClassSet.EdgeList(m)

    for t in range(rep):
        AS = FunctionSet.RandomList(AS0)
        E = ClassSet.EdgeList(m)
        if ToDebug: print("Random list {}: {}".format(t, AS))

        ## First agree set assigned to first edge
        E.SetValue(0, "Assigned", 1)
        E.SetValue(0, "AttrSet", AS[0])
        if ToDebug: print("First Agree Set 0", AS[0], "applies on Edge 0:") #, E[0]["Nodes"])
        del AS[0]

        outcome = FindArmstrong(E, AS, R, AgreeSets)
        Apply = outcome[1]
        E = outcome[2]

        if (t == 0 or E.ActualSize() < Es.ActualSize()) and Apply:
            Es = copy.deepcopy(E)

        t += 1

    if Es.length() > 0:
        Apply = True

    if Apply:
        n = Es.ActualSize()
        print('For dataset {}, {} agree sets: '.format(filename, len(AgreeSets)))
        print(n, 'tuples Armstrong Table can be built with Randomization')
    else:
        print('No sublinear Armstrong DB exists!')

    End = datetime.datetime.now()
    print("Time of running {}:".format(End - Start))

    if Apply:
        with open(OutFile, "w") as text_file:
            print('For dataset {}, {} agree sets: '.format(filename, len(AgreeSets)), sep="\n", file=text_file)
            print('{} tuples Armstrong Table can be built with Randomization'.format(n), sep="\n", file=text_file)
        Es.export(OutFile)
        with open(OutFile, "a") as text_file:
            print("Time of running {}:".format(End - Start), sep="\n", file=text_file)
    else:
        with open(OutFile, "w") as text_file:
            print('No sublinear Armstrong DB exists!')

