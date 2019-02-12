from time import sleep, strftime
from time import time as nowTime
import math
import datetime

def getCurrentTime():
    midnight = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    now = nowTime()
    return (now - midnight)

def generateBaseValuesAndSymbols(seedNumber):
    oned = seedNumber
    tenthed = oned/10
    hundrethed = oned/100
    tenned = oned*10

    baseValues = [tenned+oned+tenthed,tenned+oned,oned+tenthed,round(tenthed+hundrethed,2),tenthed]
    baseSymbols = [str(i).lstrip('0') for i in baseValues]
    return (baseValues,baseSymbols)

def transmuteSourceList(values,symbols):
    allOptions = []
    allSymbols  = []
    for sourceValue,sourceSymbol in zip(values,symbols):
        for newValue,newSymbol in zip(values,symbols):
            newChoices = [sourceValue+newValue,sourceValue-newValue,sourceValue*newValue]
            newSymbols = [sourceSymbol+"+"+newSymbol,sourceSymbol+"-"+newSymbol,sourceSymbol+"*"+newSymbol]

            if sourceValue != 0:
                newChoices += [newValue/sourceValue]
                newSymbols += [newSymbol+"/"+sourceSymbol]

            if newValue != 0:
                newChoices += [sourceValue/newValue]
                newSymbols += [sourceSymbol+"/"+newSymbol]

            if sourceValue>0 and sourceValue<10 and newValue>0 and newValue<10:
                newChoices += [sourceValue**newValue,newValue**sourceValue]
                newSymbols += [sourceSymbol+"^"+newSymbol,newSymbol+"^"+sourceSymbol]

            allOptions += newChoices
            allSymbols += newSymbols

    listOfSymbols = symbols + allSymbols
    listOfValues =  values + allOptions
    return listOfValues,listOfSymbols

numberOfChoice = 1

(baseValues,baseSymbols) = generateBaseValuesAndSymbols(numberOfChoice)
firstPassValues,firstPassSymbols = transmuteSourceList(baseValues,baseSymbols)
secondPassValues,secondPassSymbols = transmuteSourceList(firstPassValues,firstPassSymbols)

sortedValues,sortedSymbols = list(list(t) for t in zip(*sorted(zip(secondPassValues, secondPassSymbols))))

def expressionToLatex(expressionIn):
    if "/" in expressionIn:
        latexPrefix = "\\frac{"
        strComponents = expressionIn.split("/")
        latexSuffix = "}{".join(strComponents) + "}"
        return latexPrefix + latexSuffix

    else:
        return expressionIn

import latex2mathml.converter

def latexToMathMl(latexInput):
    return latex2mathml.converter.convert(latexInput)

def subtractOffNearestAmount(amountToSubtract):
    for valueIndex,valueAmount in enumerate(sortedValues):
        #if the next value is too big
        if valueAmount > amountToSubtract:
            #get the one just before it (which will be greatest without going over)
            correctIndex = valueIndex - 1
            activeAmount = sortedValues[correctIndex]
            # print (correctIndex,)
            activeSymbol = sortedSymbols[correctIndex]
            latexExpression = expressionToLatex(activeSymbol)
            mathMlString = latexToMathMl(latexExpression)

            return (activeAmount,mathMlString)

errors = []
def countup():
    secondsLeft = getCurrentTime()
    strNow = datetime.timedelta(seconds=secondsLeft)

    #hours
    numHours = secondsLeft/3600
    activeHours,activeHourSymbol = subtractOffNearestAmount(numHours)
    secondsLeft = secondsLeft - (activeHours*3600)

    #minutes
    numMinutes = secondsLeft/60
    activeMinutes,activeMinuteSymbol = subtractOffNearestAmount(numMinutes)
    secondsLeft = secondsLeft - (activeMinutes*60)

    #seconds
    numSeconds = secondsLeft
    activeSeconds,activeSecondSymbol = subtractOffNearestAmount(numSeconds)
    secondsLeft = secondsLeft - (activeSeconds)

    #milliseconds
    numMilliseconds = secondsLeft
    activeMilliSeconds, activeMilliSecondsSymbol = subtractOffNearestAmount(numMilliseconds)
    secondsLeft = secondsLeft - (activeMilliSeconds)

    # secondsLeft = round(secondsLeft,4)
    # print ()
    # print (activeHours,activeMinutes,activeSeconds,activeMilliseconds)
    # print (activeHourSymbol,activeMinuteSymbol,activeSecondSymbol,activeMilliSecondsSymbol)
    # print (timedelta(seconds=secondsLeft))
    errors.append(secondsLeft)
    outputText = (activeHourSymbol + ' h '+ activeMinuteSymbol + ' m ' + activeSecondSymbol + ' s' + activeMilliSecondsSymbol + " ms")
    return outputText,secondsLeft,strNow


def testCounter():
    numTrials = 1000
    for trial in range(numTrials):
        countup()

testCounter()