import numpy as np

class Empire:
    """Best initial countries."""
    
    def __init__(self, emperor):
        self.emperor = emperor
        self.colonies = []
        self.cost = emperor.getCost()

    def _calculateCost(self):
        self.cost = self.emperor.getCost() + sum([x.getCost() for x in self.colonies])

    def replaceColony(self,index,colony):
        self.colonies[index] = colony
        self._calculateCost()

    def replaceEmperor(self,colony):
        self.emperor = colony
        self._calculateCost()

    def deleteColony(self, index):
        del self.colonies[index]
        self._calculateCost()

    def getCost(self):
        return self.cost

    def addColony(self,ctr,index = 0):
        if index == 0:
            self.colonies.insert(len(self.colonies), ctr)
        else:
            self.colonies.insert(index, ctr)
        self._calculateCost()

    def removeColony(self,index):
        del self.colonies[index]
        self._calculateCost()

    def getNumberOfColonies(self):
        return len(self.colonies)

    def getColony(self, index):
        return self.colonies[index]

    def getEmperor(self):
        return self.emperor
