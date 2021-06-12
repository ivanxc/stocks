import os, json, requests, re, numpy
from math import sqrt

def getTickers(): # Получаем список тикеров NASDAQ и MOEX
    url = "http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt"
    nasdaqTickers = list()
    r = requests.get(url)
    nasdaqTraded = r.content
    a = nasdaqTraded.splitlines()
    for i in range(1, len(a)):
        b = re.split( r'\|', str(a[i]))
        if b[2].__contains__("Common Stock"):
            nasdaqTickers.append(b[1])
    print(len(nasdaqTickers))

    url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json?iss.meta=off&iss.only=securities&securities.columns=SECID,SECNAME"
    moexTickers = list()
    r = requests.get(url)
    moexTraded = r.json()
    for i in range (0, len(moexTraded['securities']['data'])):
        moexTickers.append(moexTraded['securities']['data'][i][0])
    print(moexTickers)
    getTop20(nasdaqTickers, moexTickers)

def getTop20(nasdaqList, moexList):
    topVolat = list()
    i = 0
    while (i < len(nasdaqList)):
        currentTicker = nasdaqList[i]
        print(str(currentTicker) + " " + str(i))
        url = "https://query1.finance.yahoo.com/v8/finance/chart/{0}?symbol={0}&period1=0&period2=9999999999&interval=1d&includePrePost=true&events=div%2Csplit".format(
            currentTicker)
        r = requests.get(url)
        ticker = r.json()
        if ticker["chart"]["result"] == None or len(ticker["chart"]["result"][0]["indicators"]["quote"][0]) == 0 or len(ticker["chart"]["result"][0]["timestamp"]) < 33:
            i += 1
            continue
        volatility = getVolatility(ticker)
        topVolat.append([currentTicker, volatility])
        i += 1

    i = 0
    while (i < len(moexList)):
        currentTicker = moexList[i] + ".ME"
        print(str(currentTicker) + " " + str(i))
        url = "https://query1.finance.yahoo.com/v8/finance/chart/{0}?symbol={0}&period1=0&period2=9999999999&interval=1d&includePrePost=true&events=div%2Csplit".format(
            currentTicker)
        r = requests.get(url)
        ticker = r.json()
        if ticker["chart"]["result"] == None or len(ticker["chart"]["result"][0]["indicators"]["quote"][0]) == 0 or len(ticker["chart"]["result"][0]["timestamp"]) < 33:
            i += 1
            continue
        volatility = getVolatility(ticker)
        topVolat.append([currentTicker, volatility])
        i += 1

    topVolat.sort(key=volF, reverse = True)
    print(topVolat[0:20])
    file = open('topVolatility.json', 'w')
    file.write(json.dumps(topVolat[0:20]))
    file.close()

def volF(item):
    return item[1]

def getVolatility(ticker):
    length = len(ticker["chart"]["result"][0]["timestamp"])
    closeList = list()
    j = 1
    counter = 0
    while counter < 31:
        if ticker["chart"]["result"][0]["indicators"]["quote"][0]["close"][length-j] != None:
            closeList.append(ticker["chart"]["result"][0]["indicators"]["quote"][0]["close"][length-j])
            counter += 1
        j += 1

    volatList = list()
    lenOfCloseList = len(closeList)
    for i in range (0, 30):
        divide = closeList[i] / closeList[i + 1]
        volatList.append((divide - 1) * 100)
    return numpy.var(volatList)/sqrt(30)

def main():
    getTickers()

if __name__ == "__main__":
    main()