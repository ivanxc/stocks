import os, tinvest, datetime, json, time
from datetime import datetime, timedelta
from tinvest import SyncClient

TOKEN = os.getenv('TINVEST_SANDBOX_TOKEN', open('TOKEN.txt', 'r').read())
client = SyncClient(TOKEN, use_sandbox=True)

def get_data(figi, securities):
    dt_now = datetime.now()
    dt_last = datetime.now() - timedelta(minutes=5)
    note = { }
    orderbook = client.get_market_orderbook(figi, 20).payload
    if (orderbook.trade_status == "NotAvailableForTrading"): # если акция недоступна для трейдинга, то удаляем её из списка
        del securities[figi]
        return None
    candles = client.get_market_candles(figi, dt_last.strftime("%Y-%m-%dT%H:%M:%S.000000+03:00"), dt_now.strftime("%Y-%m-%dT%H:%M:%S.000000+03:00"), tinvest.CandleResolution('1min')).payload.candles
    if (len(candles) > 0):
        del candles[len(candles)-1].figi
        del candles[len(candles)-1].interval
        note.update(candles[len(candles)-1])
        del orderbook.figi
        del orderbook.depth 
        note.update(orderbook)
    return note
     
def write_to_file(filename, note):
    if filename.find("*") != -1:
        filename = filename.replace("*", "")
    with open('data/' + str(datetime.now().strftime("%d-%m-%Y")) + '/' + filename + '.json', 'a+') as f:
        f.seek(0, os.SEEK_END)
        if not f.tell(): # проверка является ли файл пустым
            f.write("[")
        if (note != None):
            json.dump(note, f, default=str)
            f.write(",\n")
        else:
            f.seek(0, os.SEEK_END - 1)
            f.truncate()
            f.write("]")

def parse(securities):
    counter = 1
    print(datetime.now().strftime("%H:%M:%S"))
    for figi, name in list(securities.items()):
        if counter % 80 == 0:
            time.sleep(6)
        # print(str(counter))
        print(str(counter), name)
        counter += 1
        write_to_file(name, get_data(figi, securities))
        

def init():
    stocks = client.get_market_stocks()

    securities = { }
    for stock in stocks.payload.instruments:
        securities[stock.figi] = stock.name

    # print(len(securities))
    return securities

def get_stocks_by_ticker():
    securities = { }
    tickers = []
    with open('stable.json') as f:
        data = json.load(f)
        for item in data:
            if item.endswith('.ME'):
                item = item.replace('.ME', '')
            tickers.append(item) 
    with open('volat.json') as f:
        data = json.load(f)
        for item in data:
            if item[0].endswith('.ME'):
                item[0] = item[0].replace('.ME', '')
            tickers.append(item[0]) 
    count = 0
    for ticker in tickers:
        stock = client.get_market_search_by_ticker(ticker).payload.instruments
        if len(stock) > 0:
            securities[stock[0].figi] = stock[0].name 
            count += 1
            print(stock)
        if count == 40:
            break
    return securities

def is_workday():
    if datetime.today().weekday() < 5:
        return True
    else:
        return False

def main():
    if is_workday() == False:
        print("The exchange is closed. Relax and return to work day.")
    else:
        if not os.path.exists(os.getcwd() + '/data/' + str(datetime.now().strftime("%d-%m-%Y"))):
            path = os.getcwd()
            os.chdir(path + '/data')
            os.mkdir(str(datetime.now().strftime("%d-%m-%Y")))
            os.chdir(path)
        sec = get_stocks_by_ticker()
        while datetime.now().hour != 0:
            timer = time.time()
            parse(sec)
            stop = int(60 - (time.time() - timer) / 1000)
            if stop > 0:
                time.sleep(stop)

if (__name__ == '__main__'):
    main()
