from multiprocessing import Pool
import requests
import string
import pandas as pd
from bs4 import BeautifulSoup
import time



headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "Referer": "https://www.google.com"
        }

def get_all_symbols():
    '''Return symbols for every letter'''

    pool = Pool()

    letters = list(string.ascii_lowercase)
    symbols = pool.map(get_symbols, letters)

    return symbols

def get_symbols(letter):
    '''Get all symbols'''
    symbols = []

    letter = letter.upper()

    url = f"https://eoddata.com/stocklist/NYSE/{letter}.htm"
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    symbols_table = soup.find_all('tr', {"class": "ro"})

    for symbol_table in symbols_table:
        symbols_parsed_list = symbol_table.find_all('a')

        for object in symbols_parsed_list:
            symbol = object.text

            if symbol: symbols.append(symbol)

    return symbols

def get_quote(symbol):
    '''Get Symbol Data'''

    symbol = symbol.upper()
    URL = f"https://finance.yahoo.com/quote/{symbol}"

    response = requests.get(URL, headers=headers)
    
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        close = soup.find('fin-streamer', {"class":"Fw(b) Fz(36px) Mb(-4px) D(ib)"})
        price = soup.find('fin-streamer', {"class":"Fw(b) Fz(36px) Mb(-4px) D(ib)"})
        market_cap = soup.find('td', {"data-test":"MARKET_CAP-value"})
        name = soup.find('h1', {"class":"D(ib) Fz(18px)"})

        data = {
            "ticker":symbol,
            "name": name.text,
            "close": close.text,
            "price": price.text,
            "market_cap" : market_cap.text,
        }

        print(data)

        return data
    except Exception as e:
        print(str(e))

def create_excel_file(symbols):
    '''Create excel file with realtime market data'''

    pool = Pool()
    data = pool.map(get_quote, symbols)
    new_data = [x for x in data if x != None]

    dataframe = pd.DataFrame(new_data)
    dataframe.dropna()

    dataframe.to_excel("real_time_stock_data.xlsx", index=False)

if __name__ == '__main__':
    start = time.perf_counter()

    data = []
    symbols = get_all_symbols()

    for symbol_list in symbols:
        data.extend(symbol_list)

    create_excel_file(data)
    finish = time.perf_counter()

    print(f"Program Finished in {finish}")
