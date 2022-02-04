from operator import index
import requests
import string
from pprint import pprint
import pandas as pd
from bs4 import BeautifulSoup


headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "Referer": "https://www.google.com"
        }

def get_all_symbols():
    '''Return symbols for every letter'''

    symbol_data = list()
    letters = list(string.ascii_lowercase)

    for letter in letters:
        symbols = get_symbols(letter)
        symbol_data.extend(symbols)
    
    return symbol_data

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
    print(response.status_code, symbol)

    try:
        soup = BeautifulSoup(response.text, 'html.parser')

        close = soup.find('fin-streamer', {"class":"Fw(b) Fz(36px) Mb(-4px) D(ib)"})
        price = soup.find('fin-streamer', {"class":"Fw(b) Fz(36px) Mb(-4px) D(ib)"})
        market_cap = soup.find('td', {"data-test":"MARKET_CAP-value"})
        name = soup.find('h1', {"class":"D(ib) Fz(18px)"})

        data = {
            "close": close.text,
            "price": price.text,
            "market_cap" : market_cap.text,
            "ticker":symbol,
            "name": name.text
        }

        return data
    except Exception as e:
        print(str(e))


def create_excel_file():
    '''Create excel file with realtime market data'''
    symbols = get_all_symbols()

    data = []

    for symbol in symbols:
        symbol_data = get_quote(symbol)
        data.append(symbol_data)
    
    dataframe = pd.DataFrame.from_dict(data=data, orient="columns", index=False)

    dataframe.to_excel("real_time_stock_data.xlsx")

create_excel_file()