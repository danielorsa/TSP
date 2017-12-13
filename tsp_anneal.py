import math
import random

# This module employs simulated annealing for attempting to find an optimal solution to TSP


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


def sortByDistance(aPop):
    for i in range(50):
        j = i
        shortestTripDist = 100
        swap = None
        for currentTrip in aPop[i:]:
            distThisTrip = calcRouteDistance(currentTrip)
            if distThisTrip <= shortestTripDist:
                shortestTripDist = distThisTrip
                swap = j
            j += 1
        if swap != None:
            aPop[swap], aPop[i] = aPop[i], aPop[swap]


def getNeighbor(aTrip):
    neighbor = []
    for i in aTrip:
        neighbor.append(i)
    randIndex = random.sample(range(14), 2)
    neighbor[randIndex[0]], neighbor[randIndex[1]] = neighbor[randIndex[1]], neighbor[randIndex[0]]
    return neighbor


def acceptanceProbability(oldDist, newDist, t):
    probability = math.e**((oldDist - newDist)/t)
    return probability


def simAnnealTSP(aTrip):
    currentTripDist = calcRouteDistance(aTrip)
    temp = 1.0
    tempMin = 0.1
    tempChange = 0.1

    while temp > tempMin:
        for i in range(500):
            newTrip = getNeighbor(aTrip)
            newTripDist = calcRouteDistance(newTrip)
            if newTripDist < currentTripDist:
                aTrip = newTrip
                currentTripDist = newTripDist
            else:
                ap = acceptanceProbability(currentTripDist, newTripDist, temp)
                if ap > random.random():
                    aTrip = newTrip
                    currentTripDist = newTripDist
        temp -= tempChange

    return aTrip


saSolutions = []

for i in range(50):
    print("\n########## Test",i+1,"##########")
    initialTrip = random.sample(range(14), 14)
    print("Initial:", initialTrip, calcRouteDistance(initialTrip))

    saTSP = simAnnealTSP(initialTrip)
    saSolutions.append(saTSP)
    print("Annealed:", saTSP, calcRouteDistance(saTSP))

sortByDistance(saSolutions)
histogramBins = getHistBins()
a = (14 * distanceLowerBound(allDistances))
b = (14 * distanceUpperBound(allDistances))
dx = (b - a) / 100

print("\n")
print("Best Solutions from 50 Trials:")

sumOfAllDistances = 0
sumOfSquares = 0
for trip in saSolutions:
    distanceThisTrip = calcRouteDistance(trip)
    print(trip, distanceThisTrip)
    histogramBins[int((distanceThisTrip - a) // dx)] += 1
    sumOfAllDistances += distanceThisTrip
    sumOfSquares += (distanceThisTrip ** 2)
average = sumOfAllDistances / 50
stdDev = math.sqrt((sumOfSquares - ((sumOfAllDistances ** 2) / 50)) / 50)

print("\nShortest Trip: ", saSolutions[0])
for i in saSolutions[0]:
    print(labelLookUp[i], end=" -> ")
print(labelLookUp[saSolutions[0][0]])
print("Distance of Shortest Trip:", calcRouteDistance(saSolutions[0]))

print("\nLongest Trip:", saSolutions[-1])
for i in saSolutions[-1]:
    print(labelLookUp[i], end=" -> ")
print(labelLookUp[saSolutions[-1][0]])
print("Distance of Longest Trip:", calcRouteDistance(saSolutions[-1]))

print("\nAverage Route Distance:", average)
print("Standard Deviation:", stdDev)

print("\nHistogram Frequencies:")
histMax = max(histogramBins)
for i in range(len(histogramBins)):
    print(histogramBins[i] / histMax, "\t", end="")

