import os, json, requests


def getData():
    file = open('YahooTickers.json', 'r')
    tickers = json.loads(file.read())
    file.close()
    i = len(next(os.walk('Stocks/'))[2]) + 1

    while i < len(tickers['Stock']):
        currentTicker = tickers['Stock'][i]['Yahoo Stock Tickers']
        path = 'Stocks/' + currentTicker + '.json'
        url = "https://query1.finance.yahoo.com/v8/finance/chart/{0}?symbol={0}&period1=0&period2=9999999999&interval=1d&includePrePost=true&events=div%2Csplit".format(
            currentTicker)
        r = requests.get(url)
        json_string = json.dumps(r.json())
        f = open(path, 'w')
        f.write(json_string)
        f.close()
        i = i + 1

    file = open('YahooTickers.json', 'w')
    json_tickers = json.dumps(tickers)
    file.write(json_tickers)
    file.close()


def main():
    file = open('YahooTickers.json', 'r')
    tickers = json.loads(file.read())
    if len(tickers['Stock']) != (len(next(os.walk('Stocks/'))[2]) + 1):
        getData()
    file.close()


if __name__ == "__main__":
    main()