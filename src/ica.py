import numpy as np
import random as rn
import math

from country import *
import parameters as param
from parameters import *
from util_functions import *
from empire import *



# Create k random countries with length n (number of tasks) and elements in range(0..(r-1))
def createCountries(config):
    k = config['number_of_countries']
    r = config['number_of_processors']
    n = config['number_of_tasks']
    countries = []
    i = 0
    while i < k:
        candidate = Country(generator(r,n))
        if (True for elem in countries if np.array_equal(elem.getRepresentation(), candidate.getRepresentation())):
            countries.append(candidate)
            i +=1

    return np.array(countries)

def createEmpires(countries,config):

    costs = np.array([np.sum(countries[i].cost) for i in range(len(countries))])

    indices = np.argsort(costs)

    new_countries = np.array([countries[i] for i in indices])

    candidate_empires=new_countries[:config['number_of_empires']]

    candidate_colonies=new_countries[config['number_of_empires']:]

    empires=[]
    for ctr in candidate_empires:
        empires.append(Empire(ctr))

    empires_costs = np.array([np.sum(empires[i].getCost()) for i in range(len(empires))])
    #imp_cost = imp_cost.flatten()
    P = np.exp(-np.multiply(config['alpha_rate'], empires_costs) / np.max(empires_costs))
    P = P / np.sum(P)

    for ctry in candidate_colonies:
        k=randomSelection(P)
        empires[k].addColony(ctry)
    return empires

def assimilate(empires, config):
    number_of_empires = len(empires)
    for k in range(number_of_empires):
        empire_representation = empires[k].getEmperor().getRepresentation()  #vector of the empire
        for i in range(empires[k].getNumberOfColonies()):
            colony_representation = empires[k].getColony(i).getRepresentation()

            number_of_tasks = int(colony_representation.shape[0]*config['assimilation_rate'])
            candidates = rn.sample(range(colony_representation.shape[0]),number_of_tasks)
            colony_representation[candidates] = empire_representation[candidates]
            empires[k].getColony(i).setRepresentation(colony_representation)

            # emp[k]['Col'][i]['Position'] = emp[k]['Col'][i]['Position']+ beta * np.array([random.random() for j in range(nVar)])* (emp[k]['Imp']['Position'] - emp[k]['Col'][i]['Position'])
            # emp[k]['Col'][i]['Position'] = np.maximum(emp[k]['Col'][i]['Position'],np.full(nVar,VarMin))
            # emp[k]['Col'][i]['Position'] = np.minimum(emp[k]['Col'][i]['Position'], np.full(nVar, VarMax))
            # emp[k]['Col'][i]['Cost'] = costFunction.sphere(emp[k]['Col'][i]['Position'])

    return empires

def revolution(empires, config):
    number_of_empires = len(empires)
    for k in range(number_of_empires):
        for i in range(empires[k].getNumberOfColonies()):
            if rn.random() <= config['revolution_probability']:
                colony_representation = empires[k].getColony(i).getRepresentation()
                oldCost = empires[k].getColony(i).cost
                number_of_tasks = int(math.ceil(config['revolution_rate']*colony_representation.shape[0]))
                candidates = rn.sample(range(colony_representation.shape[0]), number_of_tasks)
                exchange = list(range(colony_representation.shape[0]))
                for index in sorted(candidates, reverse=True):
                    del exchange[index]
                #del exchange[candidates]
                exchange_candidates = rn.sample(exchange,number_of_tasks)
                new_colony_representation = colony_representation
                for (x,y) in zip(candidates,exchange_candidates):
                    new_colony_representation[x] = colony_representation[y]
                    new_colony_representation[y] = colony_representation[x]
                #empires[k].getColony(i).setRepresentation(new_colony_representation)
                new_colony=Country(new_colony_representation)
                if (new_colony.cost < oldCost):
                    empires[k].replaceColony(i,new_colony)

    return empires

def interEmpireWar(empires, config):
    #alpha = ICASettings['alpha']

    if len(empires) == 1:
        return empires

    TotalCost = np.array([empires[i].cost for i in range(len(empires))])
    # TotalCost=emp['TotalCost']

    weakest_empire_index = np.argmax(TotalCost)
    weakest_empire = empires[weakest_empire_index]
    P = np.exp(-np.multiply(config['alpha_rate'], TotalCost) / np.max(TotalCost))
    P[weakest_empire_index] = 0
    P = P / np.sum(P)
    if np.any(np.isnan(P)):
        P[np.isnan(P)] = 0;
        if all(P == 0):
            P[:] = 1;
        P = P / sum(P);

    if weakest_empire.getNumberOfColonies() > 0:
        weakest_empire_colonies_cost = np.array([weakest_empire.getColony(i).cost for i in range(weakest_empire.getNumberOfColonies())])
        weakest_colony_index= np.argmax(weakest_empire_colonies_cost)
        weakest_colony = weakest_empire.getColony(weakest_colony_index)

        winning_empire_index = randomSelection(P)
        winning_empire = empires[winning_empire_index]

        # WinnerEmp['Col'].append(WeakestCol)
        winning_empire.addColony(weakest_colony)
        #WinnerEmp['Col'] = np.append(WinnerEmp['Col'], WeakestCol)
        #WinnerEmp['nCol'] = WinnerEmp['nCol'] + 1

        weakest_empire.deleteColony(weakest_colony_index)
        #WeakestEmp['Col'] = np.delete(WeakestEmp['Col'], WeakestColIndex)

        #WeakestEmp['nCol'] = WeakestEmp['nCol'] - 1

    if weakest_empire.getNumberOfColonies() == 0:
    #if WeakestEmp['nCol'] == 0:
        winning_empire_index = randomSelection(P)
        #WinnerEmpIndex2 = RouletteWheelSelection(P)
        winning_empire = empires[winning_empire_index]
        #WinnerEmp2 = emp[WinnerEmpIndex2]

        winning_empire.addColony(weakest_empire.getEmperor())
        #WinnerEmp2['Col'] = np.append(WinnerEmp2['Col'], WeakestEmp['Imp'])
        #WinnerEmp2['nCol'] = WinnerEmp2['nCol'] + 1
        del empires[empires.index(weakest_empire)]
        #emp = np.delete(emp, WeakestEmpIndex)

    return empires

def intraEmpireWar(empires, config):
    number_of_empires = len(empires)
    for k in range(number_of_empires):
        for i in range(empires[k].getNumberOfColonies()):
            if empires[k].getColony(i).cost < empires[k].getEmperor().cost:
                old_emperor = empires[k].getEmperor()
                old_colony = empires[k].getColony(i)
                empires[k].replaceColony(i,old_emperor)
                empires[k].replaceEmperor(old_colony)

    #total cost remains unchanged for the empire
    return empires




config = param.read_parameters('config.txt')


countries = createCountries(config)

empires = createEmpires(countries, config)

# List to hold best cost values
BestCost = [0]*config['number_of_iterations']

## MAIN LOOP

for it in range(config['number_of_iterations']):

    # Assimilation
    empires = assimilate(empires, config)

    # Revolution
    empires = revolution(empires, config)

    # Intra - empire competition
    empires = intraEmpireWar(empires,config)

    # Inter - empire competition
    empires = interEmpireWar(empires, config)

    # Update best solution ever found

    costs = np.array([empires[i].getEmperor().cost for i in range(len(empires))])
    #imp = np.array([empires[i]['Imp'] for i in range(len(empires))])
    #costs = np.array([imp[i]['Cost'] for i in range(len(imp))])

    best_empire_index = np.argmin(costs)
    #BestImpIndex = np.argmin(costs)
    best_solution = empires[best_empire_index]
    #BestSol = imp[BestImpIndex]

    # Update best cost
    BestCost[it] = best_solution.getCost()

    # Display iteration information
    print(['Iteration ' + str(it)+': Best Cost = ' + str(BestCost[it])])

print(best_solution.getEmperor().getRepresentation())






