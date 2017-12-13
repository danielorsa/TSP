import math
import random
from itertools import permutations

# This module employs a Genetic Algorithm for attempting to find an optimal solution to TSP


def distanceChart(someData):
    allDistances = []
    for i in range(len(someData)):
        row = []
        for j in range(len(data)):
            xDiffSqr = (someData[i][0] - someData[j][0])**2
            yDiffSqr = (someData[i][1] - someData[j][1])**2
            distance = xDiffSqr + yDiffSqr
            distance = math.sqrt(distance)
            row.append(distance)
        allDistances.append(row)
    return allDistances


def distanceUpperBound(someData):
    upperBound = 0
    for i in someData:
        rowMax = max(i)
        if rowMax > upperBound:
            upperBound = rowMax
    return upperBound


def distanceLowerBound(someData):
    allRowMins = []
    for i in someData:
        rowMin = max(i)
        for j in i:
            if j > 0 and j < rowMin:
                rowMin = j
        allRowMins.append(rowMin)
    lowerBound = min(allRowMins)
    return lowerBound


def calcRouteDistance(route):
    dist = allDistances[route[0]][route[-1]]
    for j in range(1, len(route)):
        dist += allDistances[route[j-1]][route[j]]
    return dist


def getHistBins():
    histogramBins = []
    for i in range(100):
        histogramBins.append(0)
    return histogramBins

data = [[0.835291712, 0.917509743],
        [0.354055828, 0.428775989],
        [0.847944906, 0.422120483],
        [0.237885545, 0.208667108],
        [0.371568857, 0.130918266],
        [0.95200017, 0.963952421],
        [0.858567273, 0.691107499],
        [0.898640884, 0.227944792],
        [0.045393758, 0.505043543],
        [0.138167321, 0.522844999],
        [0.18830582, 0.352084188],
        [0.474768453, 0.967067497],
        [0.009079769, 0.408477785],
        [0.524189828, 0.94452817]]

labelLookUp = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]

allDistances = distanceChart(data)


def getInitPop(n):
    randIndex = random.randint(0, 1000000)
    randomPerms = []
    i = 0
    for perm in permutations(range(n)):
        if i == randIndex:
            permOne = []
            for i in perm:
                permOne.append(i)
            randomPerms.append(permOne)
            break
        else:
            i += 1
    sumOfDistances = 0
    while len(randomPerms) < 1000:
        newPerm = random.sample(randomPerms[0], len(randomPerms[0]))
        if newPerm not in randomPerms:
            randomPerms.append(newPerm)
            sumOfDistances += calcRouteDistance(newPerm)
    avg = sumOfDistances/1000
    print("Randoms:",len(randomPerms))

    belowAvg = []
    for perm in randomPerms:
        if calcRouteDistance(perm) < avg:
            belowAvg.append(perm)
    print("Better Than Average:",len(belowAvg))
    initPop = random.sample(belowAvg, 50)
    print("Initial Population Size:",len(initPop))

    return initPop


def getFitness(aTrip, stdDev, avg):
    thisTripDist = calcRouteDistance(aTrip)
    fitness = (avg - thisTripDist)/stdDev
    fitness = fitness//.1
    return fitness


def sortByFitness(aPop):
    for i in range(50):
        j = i
        shortestTripDist = 14*distanceUpperBound(allDistances)
        swap = None
        for currentTrip in aPop[i:]:
            distThisTrip = calcRouteDistance(currentTrip)
            if distThisTrip <= shortestTripDist:
                shortestTripDist = distThisTrip
                swap = j
            j += 1
        if swap != None:
            aPop[swap], aPop[i] = aPop[i], aPop[swap]


def mate(trip0, trip1):
    childTrip = []
    shortestSubroute = []
    shortestSubrouteDistance = 14*distanceUpperBound(allDistances)
    dominantTrait = 0

    for i in range(7):
        subRoute0Dist = calcRouteDistance(trip0[i:i+7])
        if subRoute0Dist < shortestSubrouteDistance:
            shortestSubrouteDistance = subRoute0Dist
            shortestSubroute = trip0[i:i+7]
            dominantTrait = 0

        subRoute1Dist = calcRouteDistance(trip1[i:i + 7])
        if subRoute1Dist < shortestSubrouteDistance:
            shortestSubrouteDistance = subRoute0Dist
            shortestSubroute = trip1[i:i + 7]
            dominantTrait = 1
    for i in shortestSubroute:
        childTrip.append(i)
    if dominantTrait == 0:
        for i in trip1:
            if i not in childTrip:
                childTrip.append(i)
    else:
        for i in trip0:
            if i not in childTrip:
                childTrip.append(i)
    return childTrip


def crossoverStage(aPop):
    nextGen = []
    nextGen.append(aPop[0])
    nextGen.append(aPop[1])
    for i in range(2,50):
        child = mate(aPop[i-1], aPop[i])
        nextGen.append(child)
    return nextGen


def mutate(aTrip):
    mutated = []
    for i in aTrip:
        mutated.append(i)
    mutated[0], mutated[-1] = mutated[-1], mutated[0]
    geneSwap = random.sample(range(1, 13), 2)
    mutated[geneSwap[0]], mutated[geneSwap[1]] = mutated[geneSwap[1]], mutated[geneSwap[0]]
    return mutated


def mutationStage(aPop, stdDev, average):
    postMutation = []
    postMutation.append(aPop[0])
    for trip in aPop[1:]:
        fitness = getFitness(trip, stdDev, average)
        naturalSelection = random.randint(0, 100)
        if naturalSelection < (50 - (fitness)):
            postMutation.append(mutate(trip))
        else: postMutation.append(trip)
    return postMutation


def evaluate(aPop):
    sortByFitness(aPop)
    sumOfAllDistances = 0
    sumOfSquares = 0
    for currentTrip in aPop:
        distanceThisTrip = calcRouteDistance(currentTrip)
        sumOfAllDistances += distanceThisTrip
        sumOfSquares += (distanceThisTrip ** 2)
    average = sumOfAllDistances / 50
    stdDev = math.sqrt((sumOfSquares - ((sumOfAllDistances ** 2) / 50)) / 50)
    return stdDev, average


def geneticTSP(generation, population, noProgression):
    evaluate(population)
    if generation == 0:
        for i in population:
            initPop.append(i)

    nextGen = crossoverStage(population)
    nextGenStdDev, nextGenAvg = evaluate(nextGen)

    postMutationNextGen = mutationStage(nextGen, nextGenStdDev, nextGenAvg)
    evaluate(postMutationNextGen)

    if calcRouteDistance(postMutationNextGen[0]) < calcRouteDistance(population[0]):
        noProgression = 0
    else:
        noProgression += 1

    if noProgression < 20:
       geneticTSP(generation + 1, postMutationNextGen, noProgression)

    else:
        print("Finished after", generation+1, "Generations")
        print("\nInitial Population:")
        for i in initPop:
            print(i, calcRouteDistance(i))
        print("\nFinal Population:")
        for i in postMutationNextGen:
            print(i, calcRouteDistance(i))
        print("\n")
        allBests.append(postMutationNextGen[0])


allBests = []

for i in range(50):
    initPop = []
    print("##### Trial", i + 1, "#####")
    population = getInitPop(14)
    geneticTSP(0, population, 0)
    sortByFitness(population)

stdDev, average = evaluate(allBests)
histogramBins = getHistBins()
a = (14 * distanceLowerBound(allDistances))
b = (14 * distanceUpperBound(allDistances))
dx = (b - a) / 100

print("Best Solutions from 50 Trials:")
for trip in allBests:
    distanceThisTrip = calcRouteDistance(trip)
    print(trip, distanceThisTrip)
    histogramBins[int((distanceThisTrip - a) // dx)] += 1

print("\nShortest Trip: ", allBests[0])
for i in allBests[0]:
    print(labelLookUp[i], end=" -> ")
print(labelLookUp[allBests[0][0]])
print("Distance of Shortest Trip:", calcRouteDistance(allBests[0]))

print("\nLongest Trip:", allBests[-1])
for i in allBests[-1]:
    print(labelLookUp[i], end=" -> ")
print(labelLookUp[allBests[-1][0]])
print("Distance of Longest Trip:", calcRouteDistance(allBests[-1]))

print("\nAverage Route Distance:", average)
print("Standard Deviation:", stdDev)

histMax = max(histogramBins)
for i in range(len(histogramBins)):
    print(histogramBins[i] / histMax, "\t", end="")