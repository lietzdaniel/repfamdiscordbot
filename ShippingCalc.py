import requests
import json

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import pandas as pd
from cycler import cycler
from shippingData import *


class shippingMethod:
    def __init__(self,name, firstWeight, continueWeight, firstFee, continueFee, maxWeight):
        self.name = name
        self.firstWeight = firstWeight
        self.continueWeight = continueWeight
        self.firstFee = firstFee
        self.continueFee = continueFee
        self.maxWeight = maxWeight
    def __str__(self):
        return f"{self.name}"

    name = ""
    firstWeight= 0.0
    continueWeight=0.0
    firstFee= 0.0
    continueFee = 0.0
    maxWeight = 0.0

def getNewShippingData(weight):
    with requests.Session() as session:
        payload = {'TotleWeight':weight,'TotleVolume':10,'DeliveryType':0,'TotleProductCost':'0','Area':'53'}
        response = session.post("https://cssbuy.com/ajax/estimates_ajax.php?action=getdetails",json=payload).text
    
        shippingData = json.loads(response[1:])

       

def getShippingList():
    jsonresult = shippingData
    ShippingList = []
    for x in jsonresult:
        name = x["shipping_name"]
        
        
        if name not in ["BJ-EUB :","China Post SAL（BJ） ↑5:","CSS-JW-Tariffless-F :0-4kg","CSS-FJ-B-Tariffless 0-3kg10-25daysDhl-Delivery"]:
            continue
        if name == "BJ-EUB :":
            name = "EUB"
        if name == "CSS-FJ-B-Tariffless 0-3kg10-25daysDhl-Delivery":
            name = "FJ B Tariffless"
          
        if name == "China Post SAL（BJ） ↑5:":
            name = "SAL"
        if name == "CSS-JW-Tariffless-F :0-4kg":
            name = "JW Tarifless"
        firstWeight = float(x["first_weight"])
        continueWeight = float(x["continue_weight"])
        firstFee = float(x["first_fee"])
        continueFee = float(x["continue_fee"])
        maxWeight = float(x["max_weight"])
        ShippingList.append(shippingMethod(name,firstWeight,continueWeight,firstFee,continueFee,maxWeight))
    return ShippingList


def generateTable(shippingList, weight):
    weightList = []
    costList = []
    nameList = []
    for x in shippingList:
        nameList.append(x.name)
        xList = []
        xList.append(0.0)
        xWeight = x.firstWeight
        xList.append(xWeight)
        xContinueWeight = x.continueWeight
        weightsPerPackage = (x.maxWeight - xWeight)/(xContinueWeight) 

        
        
        xMaxWeight = x.maxWeight
        newPackage = False
        while xWeight < weight:
            if xWeight > xMaxWeight:
                xWeight += x.firstWeight
                xList.append(xWeight)
                continue
            xWeight += xContinueWeight
            
            xList.append(xWeight)
        weightList.append(xList)
        yList = []
        
        yCost = 0
        counter = 0

        
        for a in xList:
            if a == 0:
                yList.append(x.firstFee)
                continue
            if counter <= weightsPerPackage:
                
                if counter == 0:
                    yCost+= x.firstFee
                    yList.append(yCost)
                    counter += 1

                    continue
                yCost+= x.continueFee
                yList.append(yCost)
                
                counter += 1
                continue
            else:
                counter = 0
                yCost+= x.firstFee
                yList.append(yCost)
        costList.append(yList)
        
    
    
    
    test= {}
    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y', 'purple'])))
    for i in range(0,len(weightList)):
        test["x_values"] = weightList[i]
        test[nameList[i]] = costList[i]
        df =pd.DataFrame(test) 
        plt.plot( 'x_values', nameList[i], data=df,  marker='', linewidth=2)
        test = {}
    plt.grid()
    plt.xlabel("Gewicht in g")
    plt.ylabel("Preis in Y")
    plt.title("CSSBuy Shipping Preisvergleich")
    plt.legend()
    #plt.show()
    plt.savefig("ShippingPlot.PNG")
    plt.clf()


def getPlotandPrices(weight):
    shippingList = getShippingList()
    if weight < 20000:
        generateTable(shippingList,weight)
    else: 
        generateTable(shippingList,20000)
        weight=20000

    prices = ""
    for x in shippingList:
        tempWeight = 0.0
        price = 0.0
        counter = 0.0
        amount = (x.maxWeight-x.firstWeight) // (x.continueWeight) + 1
        while tempWeight < weight:
            if counter == 0:
                price += x.firstFee
                tempWeight += x.firstWeight
                counter += 1
            elif counter > amount:
                price += x.firstFee
                tempWeight += x.firstWeight
                counter = 1
            else: 
                price += x.continueFee
                tempWeight += x.continueWeight
                counter += 1

        

        
        prices = "".join((prices, x.name," 0-", str(int(x.maxWeight/1000))," kg: **",str(int(price)), " Yuan**", "\n"))
    
    return prices





    

        
