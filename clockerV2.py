def generateBaseValuesAndSymbols(seedNumber):
    oned = seedNumber
    tenthed = oned/10
    hundrethed = oned/100
    tenned = oned*10

    baseValues = [tenned+oned+tenthed,tenned+oned,oned+tenthed,round(tenthed+hundrethed,2),tenthed]
    baseSymbols = [str(i).lstrip('0') for i in baseValues]
    return (baseValues,baseSymbols)

def transmuteSourceList(values,symbols):
    #produces the combination of all the entries and all the valid arithatic operations between them
    allOptions = []
    allSymbols  = []
    for sourceValue,sourceSymbol in zip(values,symbols):
        for newValue,newSymbol in zip(values,symbols):
            newChoices = [sourceValue+newValue, sourceValue*newValue]
            newSymbols = [sourceSymbol+"+"+newSymbol,sourceSymbol+"*"+newSymbol]

            if sourceValue > newValue:
                newChoices.append(sourceValue-newValue)
                newSymbols.append(sourceSymbol+"-"+newSymbol)
            else:
                newChoices.append(newValue - sourceValue)
                newSymbols.append(newSymbol+"-"+sourceSymbol)

            if abs(sourceValue) >.1:
                newChoices.append(newValue/sourceValue)
                newSymbols.append(newSymbol+"/"+sourceSymbol)

            if abs(newValue) > .1:
                newChoices.append(sourceValue/newValue)
                newSymbols.append(sourceSymbol+"/"+newSymbol)

            if (sourceValue>0 and newValue>0) and (sourceValue + newValue) < 10:
                newChoices += [sourceValue**newValue,newValue**sourceValue]
                newSymbols += [sourceSymbol+"^"+newSymbol,newSymbol+"^"+sourceSymbol]

            allOptions += newChoices
            allSymbols += newSymbols

    listOfSymbols = symbols + allSymbols
    listOfValues =  values + allOptions
    return listOfValues,listOfSymbols

def createSourceLists(seedNumber,numPasses = 2):
    (values,symbols) = generateBaseValuesAndSymbols(seedNumber)

    for passNumber in range(numPasses):
        values, symbols = transmuteSourceList(values,symbols)

    sortedValues,sortedSymbols = list(list(t) for t in zip(*sorted(zip(values, symbols))))
    return sortedValues, sortedSymbols

from latex2mathml.converter import convert as latexToMathMl

def expressionToLatex(expressionIn):
    if "/" in expressionIn:
        latexPrefix = "\\frac{"
        strComponents = expressionIn.split("/")
        latexSuffix = "}{".join(strComponents) + "}"
        return latexPrefix + latexSuffix

    return expressionIn

def expressionToMathMl(expressionIn):
    return latexToMathMl(expressionToLatex(expressionIn))


from datetime import datetime, timedelta
from time import time as nowTime

class countup:
    # much faster (~30x) implementation of the any digit countdown timer
    # keeps track of which direction each power (hour,min,sec,ms) changes in to intelligently look for new values on update

    def __init__(self):
        seedNumber = 1
        self.maxError = 0

        self.numberIn = 0
        self.numberWrong = 0
        self.sortedValues, self.sortedSymbols = createSourceLists(seedNumber)
        self.initializeValues()

    def initializeValues(self):
        self.maxIndex = len(self.sortedValues) - 1
        self.hourIndex = 0
        self.minuteIndex = 0
        self.secondIndex = 0
        self.millisecondIndex = 0
        self.getModdedTime()

    def findClosestIndex(self,lastKnownIndex,amountToSubtract,direction = 1):
        testIndex = lastKnownIndex

        if self.sortedValues[testIndex] > amountToSubtract:
            direction = 0

        if direction:
            while (testIndex < self.maxIndex):
                testValue = self.sortedValues[testIndex]
                if testValue > amountToSubtract:
                    return (testIndex - 1)
                else:
                    testIndex += 1
            #if nothing was found in the forward direction, start over at 0 and continue
            return (self.findClosestIndex(0,amountToSubtract))
        else:
            while (testIndex > 0):
                testValue = self.sortedValues[testIndex]
                if testValue < amountToSubtract:
                    return (testIndex)
                else:
                    testIndex -= 1 
            #if nothing was found in the backward direction, start over at the end and continue
            return (self.findClosestIndex(self.maxIndex,amountToSubtract,direction))

    def getCurrentTime(self):
        midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        now = nowTime()
        return (now - midnight)

    def getModdedTime(self):
        secondsLeft = self.getCurrentTime()
        strNow = timedelta(seconds=secondsLeft)

        #minutes
        numHours = secondsLeft/3600
        newHourIndex = self.findClosestIndex(self.hourIndex,numHours)

        #check if the hour index has gone up
        minuteDirection = not (newHourIndex > self.hourIndex)
        """if the hour index has increased, then the minute index should decrease (negative), 
            and you should search backwards from the current minute to check for the new index
        if the hour index has not increased, then the minute index should increase"""

        self.hourIndex = newHourIndex
        activeHours,activeHourSymbol = self.sortedValues[self.hourIndex], expressionToMathMl(self.sortedSymbols[self.hourIndex])
        secondsLeft = secondsLeft - (activeHours*3600)
        
        #minutes
        numMinutes = secondsLeft/60
        newMinuteIndex = self.findClosestIndex(self.minuteIndex,numMinutes,minuteDirection)

        #if the minute index has increased, the second index should have decreased
        secondDirection = not (newMinuteIndex > self.minuteIndex)

        self.minuteIndex = newMinuteIndex
        activeMinutes,activeMinuteSymbol = self.sortedValues[self.minuteIndex], expressionToMathMl(self.sortedSymbols[self.minuteIndex])
        secondsLeft = secondsLeft - (activeMinutes*60)

        #seconds
        numSeconds = secondsLeft
        newSecondIndex = self.findClosestIndex(self.secondIndex,numSeconds,secondDirection)

        #if the second index has increased, the millisecond one should have decreased
        millisecondDirection = not (newSecondIndex > self.secondIndex)

        self.secondIndex = newSecondIndex
        activeSeconds,activeSecondSymbol = self.sortedValues[self.secondIndex], expressionToMathMl(self.sortedSymbols[self.secondIndex])
        secondsLeft = secondsLeft - (activeSeconds)

        #milliseconds
        numMilliseconds = secondsLeft
        self.millisecondIndex = self.findClosestIndex(self.millisecondIndex,numMilliseconds,millisecondDirection)
        activeMilliseconds, activeMilliSecondsSymbol =  self.sortedValues[self.millisecondIndex], expressionToMathMl(self.sortedSymbols[self.millisecondIndex])
        
        secondsLeft = secondsLeft - (activeMilliseconds)

        if abs(secondsLeft)>self.maxError:
            self.maxError = abs(secondsLeft)
            print (secondsLeft)

        # realTime = "%s:%s:%s.%s" % (round(activeHours,3),round(activeMinutes,3),round(activeSeconds,3),(str(activeMilliseconds).split(".")[1][:4]))
        # print (realTime)
        
        outputText = (activeHourSymbol + ' h \t'+ activeMinuteSymbol + ' m \t' + activeSecondSymbol + ' s \t' + activeMilliSecondsSymbol + " ms")

        return outputText,secondsLeft,strNow


def testCounter():
    cc = countup()

    for trial in range(numTrials):
        cc.getModdedTime()

# testCounter()