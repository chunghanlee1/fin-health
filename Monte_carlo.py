# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 17:02:12 2017

@author: Chunghan
"""
import numpy as np
import scipy.stats as stats
import random
import pylab as plt
from six.moves import input #Needed for Python 2.X


def userInput():
    """
    User input information for health check.
    Input constraints specified.
    Set as global variable for ease of access.
    """
    while True:
        try:
            userCurrentAge = int(input("Your current age is: "))
        except ValueError:
            print("Make sure you type in numbers!")
            continue
        if userCurrentAge <0 or userCurrentAge > 100:
            print("Please put in sensible numbers...")
            continue
        break
    while True:
        try:
            userDeathAge = int(input("Your expect to live until (years old): "))
        except ValueError:
            print("Make sure you type in numbers!")
            continue
        if userDeathAge > 200 or userDeathAge <= userCurrentAge:
            print("Please put in sensible numbers...")
            continue
        break
    while True:
        try:
            userRetirementAge = int(input("Your planned retirement age: "))
        except ValueError:
            print("Make sure you type in numbers!")
            continue
        if userRetirementAge > userDeathAge:
            print("Please put in sensible numbers...")
            continue
        elif userRetirementAge < userCurrentAge:
            print("Have you already retired? If so, set this equal to your current age!")
            continue
        break
    while True:
        try:
            userIncome = int(input("Your average yearly income: "))
        except ValueError:
            print("Make sure you type in numbers!")
            continue
        if userIncome <0:
            print("You can't really have negative income...")
            continue
        break
    while True:
        try:
            incomeGrowth = float(input("Your expected income growth(in decimal places, default is 0.02): ") or 0.02)
        except ValueError:
            print("Make sure you type in numbers!")
            continue
        break
    while True:
        try:
            userSpending = int(input("Your spending every year: "))
        except ValueError:
            print("Make sure you type in numbers!")
            continue
        if userSpending <0:
            print("You can't really have negative spending...")
            continue
        break
    while True:
        try:
            inflation = float(input("Inflation rate (in decimal places, default is 0.02): ") or 0.02)
        except ValueError:
            print("Make sure you type in numbers!")
            continue
        break
    while True:
        try:
            userSavings = int(input("Your current savings amount: "))
        except ValueError:
            print("Make sure you type in numbers!")
            continue
        if userSavings <0:
            print("You can't really have negative savings...Don't count debt in")
            continue
        break
    while True:
        try:
            investmentRisk = int(input("Please rate your portfolio's risk from 0 (riskless) to 10 (risky): "))
        except ValueError:
            print("Make sure you type in numbers!")
            continue
        if investmentRisk <0 or investmentRisk >10:
            print("Please choose from the list of 0 to 10...")
            continue
        break
    return userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk, userCurrentAge, userDeathAge, userRetirementAge


def investmentResult(investmentRisk, userCurrentAge, userDeathAge):
    """
    Identifies user portfolio risk-return characteristics for simulation
    Input: User selected investment riskiness
    Output: List of simulated yearly investment return until death
    """
    yearlyInvestmentResult = []
    if investmentRisk < 2: 
        assetReturn = 0.01
        assetRisk = 0.01
    elif investmentRisk < 4:
        assetReturn = 0.03
        assetRisk = 0.08
    elif investmentRisk < 6:
        assetReturn = 0.05
        assetRisk = 0.1
    elif investmentRisk < 8:
        assetReturn = 0.07
        assetRisk = 0.15
    else:
        assetReturn = 0.1
        assetRisk = 0.2
    for i in range(userCurrentAge, userDeathAge):
        yearlyInvestmentResult.append(random.gauss(assetReturn, assetRisk))
    return yearlyInvestmentResult


def yearlyTotalIncome(userIncome, incomeGrowth, userCurrentAge, userDeathAge, userRetirementAge):
    """
    Exrapolate user income to future years until retirement. Income after retirement is assumed to be 0.
    Input: User provided income and growth information
    Output: List of extrapolated yearly income until death age. 
    """
    lifetimeIncome = []
    for i in range(userCurrentAge, userDeathAge):
        if i <= userRetirementAge:
            lifetimeIncome.append(userIncome*((1+incomeGrowth)**(i-userCurrentAge)))
        else:
            lifetimeIncome.append(0)
    return lifetimeIncome


def yearlyTotalSpending(userSpending, inflation, userCurrentAge, userDeathAge):
    """
    Exrapolate user spending to future years until death
    Input: User provided spending and inflation information
    Output: List of extrapolated yearly spending until death age
    """
    lifetimeSpending = []
    for i in range(userCurrentAge, userDeathAge):
        lifetimeSpending.append(userSpending*((1+inflation)**(i-userCurrentAge)))
    return lifetimeSpending

def simGraph(yearlyResult):
    """
    Visualize yearly result to show average and worst case scenarios
    Input: Nested list of yearly result over multiple simulations
    Output: Graph of results in different scenarios
    """
    worstCase = []
    poorCase = []
    averageCase = []
    for i in yearlyResult:
        worstCase.append(np.percentile(i, 5))
        poorCase.append(np.percentile(i, 25))
        averageCase.append(np.percentile(i, 50))
    plt.plot(list(range(len(yearlyResult))), worstCase, label = 'Worst Case')
    plt.plot(list(range(len(yearlyResult))), poorCase, label = 'Poor Case')
    plt.plot(list(range(len(yearlyResult))), averageCase, label = 'Average Case')
    plt.legend()
    plt.xlabel("Years from now")
    plt.ylabel("Net Wealth")
    plt.show()

def simOutputClassification(netWealth):
    """
    Classification of simulation data to present diagnosis result
    """
    p = np.percentile(netWealth, 5)
    probRuin = stats.percentileofscore(netWealth, 0)
    if probRuin < 1 :
        return ("-------------------------------\nCongratulations, your financial situation is excellent! In the worst case you will have " + str(p) + " dollars left. And the chance for you to get into financial trouble is: " + str(probRuin) + "%\n-------------------------------")
    elif probRuin <= 5:
        return ("-------------------------------\nYour condition is safe! In the worst case you will have " + str(p) + " dollars left. And the chance for you to get into financial trouble is: " + str(probRuin) + "%\n-------------------------------")
    elif probRuin <= 10:
        return ("-------------------------------\nYou have a pretty decent financial condition! In the worst case you will have " + str(p) + " dollars left. And the chance for you to get into financial trouble is: " + str(probRuin) + "%\n-------------------------------")
    elif probRuin <= 20:
        return ("-------------------------------\nYour financial condition is not bad. In the worst case you will have " + str(p) + " dollars left. And the chance for you to get into financial trouble is: " + str(probRuin) + "%\n-------------------------------")
    elif probRuin <= 30:
        return ("-------------------------------\nYour financial condition is a bit shaky... In the worst case you will have " + str(p) + " dollars left. And the chance for you to get into financial trouble is: " + str(probRuin) + "%\n-------------------------------")
    elif probRuin <= 40:
        return ("-------------------------------\nHmm...It seems like your current financial situation is not robust enough...There is a "+ str(probRuin) + "% chance you will not have enough money by the end of your life. In the worst case, you will have " + str(p) + " dollars...\n-------------------------------")
    elif probRuin > 40:
        return ("-------------------------------\nOh no...It seems like your current financial situation is pretty lousy...There is a "+ str(probRuin) + "% chance you will not have enough money by the end of your life. In the worst case, you will have " + str(p) + " dollars...\n-------------------------------")
    

def reqReturnOutputClassification(reqReturn):
    if reqReturn <= 0.001 :
        return ("-------------------------------\nCongratulations, your financial condition is awesome, you don't need any investment to achieve your financial goals! Your required return is: " + str(reqReturn*100) + "%\n-------------------------------")
    elif reqReturn < .02:
        return ("-------------------------------\nCongratulations, your financial condition is very secure, just need a little bit investment to achieve your financial goals! Your required return is: " + str(reqReturn*100) + "%\n-------------------------------")
    elif reqReturn < .04:
        return ("-------------------------------\nYour financial condition is pretty good. Your required return is: " + str(reqReturn*100) + "%\n-------------------------------")
    elif reqReturn < .06:
        return ("-------------------------------\nYour financial condition is ok. Your required return is: " + str(reqReturn*100) + "%\n-------------------------------")
    elif reqReturn < .08:
        return ("-------------------------------\nYour financial condition requires some attention... Your required return is: " + str(reqReturn*100) + "%\n-------------------------------")
    elif reqReturn < .09:
        return ("-------------------------------\nYour financial condition is a bit dangerous... Your required return is: " + str(reqReturn*100) + "%\n-------------------------------")
    elif reqReturn >= .09:
        return ("-------------------------------\nYou are in a very dangerous financial condition.... Your required return is: " + str(reqReturn*100) + "% or above\n-------------------------------")

def simHealthCheck(userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk, userCurrentAge, userDeathAge, userRetirementAge):
    """
    Monte Carlo based financial health check function: Using simulation to test the expected financial situation of user
    Input: user financial information inputs
    Output: Diagnosis result
    """
    yearlyDetails = [[] for _ in range(userDeathAge-userCurrentAge)]#create a nested list to hold yearly savings
    lifetimeIncome = yearlyTotalIncome(userIncome, incomeGrowth, userCurrentAge, userDeathAge, userRetirementAge)
    lifetimeSpending = yearlyTotalSpending(userSpending, inflation, userCurrentAge, userDeathAge)
    userCurrentSavings = userSavings
    for i in range(5000):#Repeat Lifetime 5000 times    
        userSavings = userCurrentSavings
        yearlyInvestmentResult = investmentResult(investmentRisk, userCurrentAge, userDeathAge)
        for j in range(userCurrentAge-userCurrentAge, userDeathAge-userCurrentAge):
            #Calculate net savings every period
            if userSavings < 0:
                userSavings = userSavings + lifetimeIncome[j] - lifetimeSpending[j]
            else:
                userSavings = (userSavings*(1+yearlyInvestmentResult[j]) + lifetimeIncome[j] - lifetimeSpending[j])
            yearlyDetails[j].append(userSavings)
    simGraph(yearlyDetails)
    return simOutputClassification(yearlyDetails[userDeathAge-userCurrentAge-1])

def reqReturnHealthCheck(userIncome, incomeGrowth, userSpending, inflation, userSavings, userCurrentAge, userDeathAge, userRetirementAge):
    """
    Input: User financial information
    Output: User required return to achieve financial goal. Result obtained using bisection search.
    """
    lifetimeIncome = yearlyTotalIncome(userIncome, incomeGrowth, userCurrentAge, userDeathAge, userRetirementAge)
    lifetimeSpending = yearlyTotalSpending(userSpending, inflation, userCurrentAge, userDeathAge)
    minReqReturn = 0
    maxReqReturn = 0.2#20% is a very high return requirement
    userCurrentSavings = userSavings
    for i in range(200):#Don't want to enter a loop forever in case there's no solution
        reqReturn = (minReqReturn + maxReqReturn)/2
        userSavings = userCurrentSavings#Reset financial condition
        for i in range(userCurrentAge-userCurrentAge, userDeathAge-userCurrentAge):
            if userSavings < 0:
                userSavings = userSavings + lifetimeIncome[i] - lifetimeSpending[i]
            else:
                userSavings = (userSavings*(1+reqReturn) + lifetimeIncome[i] - lifetimeSpending[i])
        if abs(userSavings) <= 1:#Solution found
            break
        elif userSavings >1:
            maxReqReturn = reqReturn
        elif userSavings <1:
            minReqReturn = reqReturn
    return reqReturnOutputClassification(reqReturn)

def beginHealthCheck(userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk, userCurrentAge, userDeathAge, userRetirementAge):
    """
    Begin health check. Can choose to use required return or Monte Carlo simulation method
    Input: User financial and personal information
    Output: Analysis Result
    """
    while True:
        try:
            healthCheckOption = str(input("If you would like to use our basic function, please enter 'b', if you want advanced function, enter 'a', if you want to leave, press 'e': \n"))
        except:
            print("Please enter a lower case 'b', 'a', or 'e'.")
            continue
        if healthCheckOption == 'b':
            print(reqReturnHealthCheck(userIncome, incomeGrowth, userSpending, inflation, userSavings, userCurrentAge, userDeathAge, userRetirementAge))
        elif healthCheckOption == 'a':
            print(simHealthCheck(userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk, userCurrentAge, userDeathAge, userRetirementAge))
        elif healthCheckOption == 'e': 
            print("GoodBye!")
            break
        else:
            print("Make sure you type in 'b', 'a', or 'e'!")
            continue
    
def userHealthCheck():
    userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk, userCurrentAge, userDeathAge, userRetirementAge = userInput()
    beginHealthCheck(userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk, userCurrentAge, userDeathAge, userRetirementAge)    
"""
End function definitions
"""


"""
Example cases
"""
class Examples(object):
    """
    Framework for building cases
    """
    def __init__(self, userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk):
        self.userIncome = userIncome
        self.incomeGrowth = incomeGrowth
        self.userSpending = userSpending
        self.inflation = inflation 
        self.userSavings = userSavings
        self.investmentRisk = investmentRisk
        self.userDeathAge = 90
        self.userRetirementAge = 60
        self.userCurrentAge = 'To be specified'
    def infoGetter(self):
        print('---------------------------\nThe Following is case information: \nIncome: %d \nIncome Growth: %d%% \nSpending: %d \nInflation rate: %d%% \nTotal savings: %d \nInvestment riskiness: %d out of 10 \nCurrent Age: %d \nExpected to live until: %d \nRetirement Age: %d\n--------------------------' \
        % (self.userIncome, self.incomeGrowth*100, self.userSpending, self.inflation*100, self.userSavings, self.investmentRisk, self.userCurrentAge, self.userDeathAge, self.userRetirementAge))
    def runTest(self):
        print(simHealthCheck(self.userIncome, self.incomeGrowth, self.userSpending, self.inflation, self.userSavings, self.investmentRisk, self.userCurrentAge, self.userDeathAge, self.userRetirementAge))

class YoungExamples(Examples):
    def __init__(self, userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk):
        Examples.__init__(self, userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk)
        self.userCurrentAge = 30
        
class MidExamples(Examples):
    def __init__(self, userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk):
        Examples.__init__(self, userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk)
        self.userCurrentAge = 40

class OldExamples(Examples):
    def __init__(self, userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk):
        Examples.__init__(self, userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk)
        self.userCurrentAge = 60

def runExample():
    while True:
        try:
            choice = str(input("We are ready to begin! Type 's' to start, 'e' to exit: "))
        except:
            print("Please type a letter.")
            continue
        if choice == 's':
            while True:
                try:
                    choice = str(input("Type 'h' for a healthy example, 's' for so-so, 'u' for a bit unhealthy: "))
                except:
                    print("Please type a letter.")
                    continue
                if choice=='h':
                    userIncome = 1000
                    incomeGrowth =.02
                    userSpending = 500
                    inflation = .02
                    userSavings = 100000
                    investmentRisk = 5
                    break
                elif choice=='s':
                    userIncome = 1000
                    incomeGrowth = .02
                    userSpending = 900
                    inflation = .02
                    userSavings = 25000
                    investmentRisk =8
                    break
                elif choice=='u':
                    userIncome = 1000
                    incomeGrowth = .02
                    userSpending = 1000
                    inflation = .02
                    userSavings = 10000
                    investmentRisk = 10
                    break
                else:
                    print("You did not select from 'h', 's', or 'u'.")
                    continue
            while True:
                try:
                    choice = str(input("Type 'y' for young example, 'm' for middle aged, 'o' for old: "))
                except:
                    print("Please type a letter.")
                    continue
                if choice == 'y':
                    ExampleChoice = YoungExamples(userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk)
                    break
                elif choice == 'm':
                    ExampleChoice = MidExamples(userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk)
                    break
                if choice == 'o':
                    ExampleChoice = OldExamples(userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk)
                    break
                else:
                    print("You did not select from 'y', 'm', or 'o'.")
                    continue
            while True:
                try:
                    choice = str(input("Type 'i' for detailed example information, 'r' to run a test on the example, or 'e' to go back to the start: "))
                except:
                    print("Please type a letter.")
                    continue
                if choice=='i':
                    ExampleChoice.infoGetter()
                elif choice=='r':
                    ExampleChoice.runTest()
                elif choice=='e':
                    break
                else:
                    print("You did not select from 'i', or 'r'.")
                    continue
        elif choice == 'e':
            break
        else:
            print("You did not select from 'i', or 'r'.")
            continue

"""
End example cases
"""
			
"""
Initiate Functions
"""
#userHealthCheck()#run health-check function
#runExample()
