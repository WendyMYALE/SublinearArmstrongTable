import datetime
import copy
import logging

import ClassSet
import FunctionSet
import ATMining

#logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.WARNING)
logging.getLogger('FindArmstrong').setLevel(logging.DEBUG);

def FindArmstrong(E, AS, R, AgreeSets, level, a, depth=0):
    """
    :param E: Edge list
    :param AS: Agree set list with assignment status
    :param R: Attributes set (schema)
    :param AgreeSets: Entire agree sets
    :param level: Current assignment level
    :return: 1. Armstrong Table exists - True or False
             2. Edge list
             3. Agree set list with assignment status
     """

    logger = logging.getLogger('FindArmstrong')

    Apply = False
    count = 0
    if level == 3:
        l1 = 0
    else:
        l1 = int((level  - 1) * (level - 2) / 2)
    l2 = int(level * (level - 1) / 2)
    for k in range(l2 - l1):
        ## Unassgined edge
        if E.GetValue(k + l1, "Assigned") == 0:
             for i in range(len(AS)):
                count += 1
                if ToDebug: print("Try No.", count)
                if FunctionSet.Subset(E.GetValue(k + l1, "AttrSet"), AS[i][0]) and AS[i][1] == 0 and E.GetValue(k + l1, "Assigned") == 0:
                ## No forced edge generated or AS[i] is superset of forced edge
                    if ToDebug: print("Applying agree set", i, AS[i][0], "on Edge:", k + l1, E.GetValue(k + l1, "Nodes"))
                    E1 = copy.deepcopy(E)
                    AS1 = copy.deepcopy(AS)
                    #E1.SetValue(k + l1, "AttrSet", AS1[i][0])
                    #result = FunctionSet.EdgeCheck(E1, R, AgreeSets)
                    result = FunctionSet.CliqueCheck(E1, R, AgreeSets, AS1[i][0], E.GetValue(k + l1, "Nodes"))
                    Apply = result[1]
                    E1 = result[2]

                    if Apply:
                        if ToDebug: print("Applied agree set", i, AS1[i], "on Edge:", k + l1, E1.GetValue(k + l1, "Nodes"), "successfully : )")
                        E1.SetValue(k + l1, "AttrSet", AS1[i][0])
                        E1.SetValue(k + l1, "Assigned", 1)
                        AS1[i][1] = 1
                        if l2 - l1 - E1.UnassignedNo(level)  > a:
                            Er = copy.deepcopy(E1)
                            ASr = copy.deepcopy(AS1)
                            a = l2 - l1 - E1.UnassignedNo(level)
                        if ToDebug: E1.print()

                        if sum(x.count(0) for x in AS1) > 0 and E1.UnassignedNo(level) > 0:
                            if ToDebug: print("Before: AS {}".format(AS))
                            if ToDebug: print("Before: AS1 {}".format(AS1))
                            if ToDebug: print("Before: Apply is {}, k + l1: {}, Depth: {}".format(Apply, k + l1, depth))
                            output = FindArmstrong(E1, AS1, R, AgreeSets, level, a, depth + 1)
                            Apply = output[1]
                            E1 = output[2]
                            AS1 = output[3]
                            a = output[4]
                        elif E1.UnassignedNo(level) == 0:
                            if ToDebug: print("Level {} finished: AS {}".format(level, AS))
                            if ToDebug: print("Level {} finished: AS1 {}".format(level, AS1))
                            if ToDebug: print("Level {} finished: Apply is {}, k + l1: {}, Depth: {}".format(level, Apply, k + l1, depth))
                            return {1: Apply, 2: E1, 3: AS1, 4: a}
                        else:   ##sum(x.count(0) for x in AS1) == 0
                            if ToDebug: print("Bottom: AS {}".format(AS))
                            if ToDebug: print("Bottom: AS1 {}".format(AS1))
                            if ToDebug: print("Bottom: Apply is {}, k: {}, Depth: {}".format(Apply, k, depth))
                            return {1: Apply, 2: E1, 3: AS1, 4: a}
                    else:
                        if ToDebug:
                            print("Applied agree set", i, AS1[i][0], "on Edge:", k + l1, E1.GetValue(k + l1, "Nodes"), "failed : (")
                            E1.print()

                    if sum(x.count(0) for x in AS1) == 0 or E1.UnassignedNo(level) == 0: # or count == (l2 - l1) * len(AS) - 1:
                        return {1: Apply, 2: E1, 3: AS1, 4: a}
                elif AS[i][1] == 0 and E.GetValue(k + l1, "Assigned") == 0:  ## AS[i] is not superset of forced edge
                    Apply = False
                    if ToDebug: print("Forced edge exists, applied agree set", i, AS[i][0], "on Edge:", k + l1, E.GetValue(k + l1, "Nodes"), "failed : (")

    if not Apply:
        if count < (l2 - l1) * len(AS):
            if ToDebug: print("Return E")
            return {1: Apply, 2: E, 3: AS, 4: a}
        else:
            if ToDebug: print("Return Er")
            return {1: Apply, 2: Er, 3: ASr, 4: a}

filename = 'Table_c10r15'
path_in = "/Users/wye1/Documents/Experiments/DataSets/naumann_small/"
path_m = "/Users/wye1/Documents/Experiments/DataSets/RandomTables/"
path_out = "/Users/wye1/Documents/Experiments/5-Sublinear/Output/"
DataFile = path_in + filename + '.csv'
ASFile = path_m + filename + '.txt'
OutFile = path_out + filename + '_StBT.txt'
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

    Start = datetime.datetime.now()

    m = len(AgreeSets)
    E = ClassSet.EdgeList(m)
    AS  = [['', 0] for x in range(m)]
    for i in range(m):
        AS[i][0] = AgreeSets[i]
    AS = sorted(AS)

    for i in range(m - 2):
        if sum(x.count(0) for x in AS) == 0:
            break
        else:
            print("Search for level {}...".format(i + 3))
            outcome = FindArmstrong(E, AS, R, AgreeSets, i + 3, 0)
            Apply = outcome[1]
            E = outcome[2]
            AS = outcome[3]

    if Apply:
        n = E.ActualSize()
        print('For dataset {}, {} agree sets: '.format(filename, len(AgreeSets)))
        print(n, 'tuples Armstrong Table can be built with Staged BT')
    else:
        print('No sublinear Armstrong DB exists!')

    End = datetime.datetime.now()
    print("Time of running {}:".format(End - Start))

    if Apply:
        with open(OutFile, "w") as text_file:
            print('For dataset {}, {} agree sets: '.format(filename, len(AgreeSets)), sep="\n", file=text_file)
            print('{} tuples Armstrong Table can be built with Staged BT'.format(n), sep="\n", file=text_file)
        E.export(OutFile)
        with open(OutFile, "a") as text_file:
            print("Time of running {}:".format(End - Start), sep="\n", file=text_file)
    else:
        with open(OutFile, "w") as text_file:
            print('No sublinear Armstrong DB exists!', sep="\n", file=text_file)
            print("Time of running {}:".format(End - Start), sep="\n", file=text_file)

