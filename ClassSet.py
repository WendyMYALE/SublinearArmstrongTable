import math

class EdgeList:
    def __init__(self, n):
        self.edge_list = list()

        for i in range(3 - 1):
           for j in range(3 - (i + 1)):
                self.edge_list.append({"Nodes": (i, i + j + 1), "Assigned": 0, "AttrSet": ''})

        for i in range(n - 3):
            for j in range(i + 3):
                self.edge_list.append({"Nodes": (j, i + 3), "Assigned": 0, "AttrSet": ''})

    def __str__(self):
        return str(self.edge_list)

    def print(self):
        for i in range(len(self.edge_list)):
            print(self.edge_list[i])

    def export(self, OutFile):
        with open(OutFile, "a") as text_file:
            for i in range(len(self.edge_list)):
                print(self.edge_list[i], sep="\n", file=text_file)

    def length(self):
        return len(self.edge_list)

    def SetValue(self, i, key, value):
        self.edge_list[i][key] = value

    def GetValue(self, i, key):
        return self.edge_list[i][key]

    def ActualSize(self):
        l = len(self.edge_list)
        n = math.ceil((1 + math.sqrt(1 + 8 * l)) / 2)
        for k in range(l):
            if self.edge_list[l - 1 - k]["Assigned"] == 1 and self.edge_list[l - 1 - k]["AttrSet"] != '':
                n = math.ceil((1 + math.sqrt(1 + 8 * (l - k))) / 2)
                break
        return n

    def DelItem(self, i):
        del self.edge_list[i]

    def UnassignedNo(self, level):
        if level == 3:
            l1 = 0
        else:
            l1 = int((level - 1) * (level - 2) / 2)
        l2 = int(level * (level - 1) /2)
        s = 0
        for i in range (l2 -l1):
            if self.edge_list[i + l1]["Assigned"] == 0:
                s += 1
        return s

    def alter(self, n):
        l1 = len(self.edge_list)
        l2 = int(n * (n - 1) / 2)
        for k in range(l1 - l2):
            self.edge_list[l1 - 1 - k]["Assigned"] = 1
            self.edge_list[l1 - 1 - k]["AttrSet"] = ''

    def resize(self, n):
        l1 = len(self.edge_list)
        l2 = int(n * (n - 1) / 2)
        for k in range(l1 - l2):
            del self.edge_list[l1 - 1 - k]

        #return self.edge_list
