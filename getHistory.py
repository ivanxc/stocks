import os, json, requests, re, numpy
from datetime import datetime

def getHistory(tickerName, period):
    url = "https://query1.finance.yahoo.com/v8/finance/chart/{0}?symbol={0}&period1=0&period2=9999999999&interval=1d&includePrePost=true&events=div%2Csplit".format(
        tickerName)
    r = requests.get(url)
    tickerData = r.json()
    print(len(tickerData))
    if tickerData["chart"]["result"] == None or len(tickerData["chart"]["result"][0]["indicators"]["quote"][0]) == 0 or len(tickerData["chart"]["result"][0]["timestamp"]) < 33:
        return

    totalDays = len(tickerData["chart"]["result"][0]["indicators"]["quote"][0]["close"])
    counter = 0
    result = list()
    day = totalDays - period - 1
    while (counter < period):
        field = dict()
        field.update({"c": tickerData["chart"]["result"][0]["indicators"]["quote"][0]["close"][day]})
        field.update({"h": tickerData["chart"]["result"][0]["indicators"]["quote"][0]["high"][day]})
        field.update({"l": tickerData["chart"]["result"][0]["indicators"]["quote"][0]["low"][day]})
        field.update({"o": tickerData["chart"]["result"][0]["indicators"]["quote"][0]["open"][day]})
        ts = int(tickerData["chart"]["result"][0]["timestamp"][day])
        time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        field.update({"time": time})
        field.update({"v": tickerData["chart"]["result"][0]["indicators"]["quote"][0]["volume"][day]})
        isRised = 0
        if (tickerData["chart"]["result"][0]["indicators"]["quote"][0]["close"][day]/tickerData["chart"]["result"][0]["indicators"]["quote"][0]["close"][day - 1] > 1):
            isRised = 1
        field.update({"isRised": isRised})
        result.append(field)
        day = day + 1
        counter = counter + 1
    return result