import numpy as np
import parameters as param

class Country:

    def __init__(self, representation):
        self.colonies = []
        self.representation = representation  #np.array length
        self.makespan = self._calculateCost()


    #CALCULATORS
    def _calculateCost(self):
        ETC = param.ETC
        return np.sum(np.multiply(ETC.T,self.representation))

    #GETTERS

    def isColony(self):
        return False

    def isImperialist(self):
        return not self.isColony(self)

    def getRepresentation(self):
        return self.representation

    def getCost(self):
        return self.makespan

    def getTimeFitness(self):
        return None

    #SETTERS

    def setRepresentation(self,representation):
        self.representation = representation
        self._calculateCost()