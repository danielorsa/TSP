import math
import time
import random
from itertools import permutations

# This module employs a random and exhaustive search for finding an optimal solution to TSP


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


def calcRunTime(time0):
    seconds = time0
    minutes = time0//60
    hours = time0//3600
    if hours > 0:
        minutes = (seconds - (hours*3600))//60
        seconds = (seconds - (hours*3600)) - (minutes*60)
    else:
        if minutes > 0:
            seconds = (seconds - (minutes*60))
    print("\n##### Finished in {0} hour(s), {1} minute(s), and {2} second(s) #####".format(int(hours), int(minutes), round(seconds, 5)))


def getRandomPerms(n, sampleSize):
    print("Creating New Random Sample")
    randomPerms = []
    rangeEnd = int(math.floor(math.factorial(n-1)/sampleSize))
    i = random.randint(0, rangeEnd)
    j = 0
    for perm in permutations(range(n)):
        if len(randomPerms) == sampleSize:
            break
        if j == i:
            randomPerms.append(perm)
            # print(len(randomPerms))
            i += random.randint(1, (((len(randomPerms)+1)*rangeEnd)-j))
        j += 1
    return randomPerms


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


def randomTSP(n, sampleNum):
    randomPerms = getRandomPerms(n, sampleNum)

    a = (n*distanceLowerBound(allDistances))
    b = (n*distanceUpperBound(allDistances))
    dx = (b - a)/100

    shortestTripDistance = n*distanceUpperBound(allDistances)
    longestTripDistance = n*distanceLowerBound(allDistances)
    sumOfAllDistances = 0
    count = 0
    sumOfSquares = 0
    histogramBins = getHistBins()
    startTime = time.clock()
    for currentTrip in randomPerms:
        distanceThisTrip = calcRouteDistance(currentTrip)
        sumOfAllDistances += distanceThisTrip
        count +=1
        histogramBins[int((distanceThisTrip - a)//dx)] += 1
        sumOfSquares += (distanceThisTrip**2)
        if distanceThisTrip < shortestTripDistance:
            shortestTripDistance = distanceThisTrip
            shortestTrip = currentTrip
        elif distanceThisTrip > longestTripDistance:
            longestTripDistance = distanceThisTrip
            longestTrip = currentTrip

    stopTime = time.clock()
    finishTime = stopTime-startTime

    stdDev = math.sqrt((sumOfSquares-((sumOfAllDistances**2)/count))/count)

    print("########## ", n, "Cities ##########")

    print("\nShortest Trip: ", shortestTrip)
    for i in shortestTrip:
        print(labelLookUp[i], end=" -> ")
    print(labelLookUp[shortestTrip[0]])
    print("Distance of Shortest Trip:", shortestTripDistance)

    print("\nLongest Trip:", longestTrip)
    for i in longestTrip:
        print(labelLookUp[i], end=" -> ")
    print(labelLookUp[shortestTrip[0]])
    print("Distance of Longest Trip:", longestTripDistance)

    print("\nAverage Route Distance:", sumOfAllDistances/count)
    print("Standard Deviation:", stdDev)

    print("\r")
    print("Histogram Frequecies:")
    histMax = max(histogramBins)
    for i in range(len(histogramBins)):
        print(histogramBins[i]/histMax, "\t", end="")

    print("\r")
    calcRunTime(finishTime)


def exhaustiveTSP(n):
    a = (n*distanceLowerBound(allDistances))
    b = (n*distanceUpperBound(allDistances))
    dx = (b - a)/100

    shortestTripDistance = n*distanceUpperBound(allDistances)
    longestTripDistance = n*distanceLowerBound(allDistances)
    sumOfAllDistances = 0
    count = 0
    sumOfSquares = 0
    histogramBins = getHistBins()
    startTime = time.clock()
    for currentTrip in permutations(range(n)):
        if currentTrip[0] == 0:
            distanceThisTrip = calcRouteDistance(currentTrip)
            sumOfAllDistances += distanceThisTrip
            count +=1
            histogramBins[int((distanceThisTrip - a)//dx)] += 1
            sumOfSquares += (distanceThisTrip**2)
            if distanceThisTrip < shortestTripDistance:
                shortestTripDistance = distanceThisTrip
                shortestTrip = currentTrip
            elif distanceThisTrip > longestTripDistance:
                longestTripDistance = distanceThisTrip
                longestTrip = currentTrip
        else:
            break

    stopTime = time.clock()
    finishTime = stopTime-startTime

    stdDev = math.sqrt((sumOfSquares-((sumOfAllDistances**2)/count))/count)

    print(n, "Cities")

    print("Shortest Trip: ", shortestTrip)
    for i in shortestTrip:
        print(labelLookUp[i], end=" -> ")
    print(labelLookUp[shortestTrip[0]])
    print("Distance of Shortest Trip:", shortestTripDistance)

    print("\nLongest Trip:", longestTrip)
    for i in longestTrip:
        print(labelLookUp[i], end=" -> ")
    print(labelLookUp[shortestTrip[0]])
    print("Distance of Longest Trip:", longestTripDistance)

    print("\nAverage Route Distance:", sumOfAllDistances/count)
    print("Standard Deviation:", stdDev)
    print("Trips Checked:", count)

    print("\r")
    print("Histogram Frequecies:")
    histMax = max(histogramBins)
    for i in range(len(histogramBins)):
        print(histogramBins[i] / histMax, "\t", end="")

    print("\r")
    calcRunTime(finishTime)

# exhaustiveTSP(10)

# randomTSP(14, 1000000)

sum = 14*distanceLowerBound(allDistances)
interval = ((14*distanceUpperBound(allDistances))- (14*distanceLowerBound(allDistances)))/100
histInts = []
histInts.append(sum)
for i in range(100):
    sum += interval
    histInts.append(sum)
for i in histInts:
    print(i, end="\t")