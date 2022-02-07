from multiprocessing import Pool
import multiprocessing
import requests
from datetime import datetime
import string
import pandas as pd
from bs4 import BeautifulSoup
from pprint import pprint

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

    url = f"https://eoddata.com/stocklist/NASDAQ/{letter}.htm"
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
        prev_close = soup.find('td', {"data-test":"OPEN-value"})
        open = soup.find('td', {"data-test":"PREV_CLOSE-value"})
        price = soup.find('fin-streamer', {"class":"Fw(b) Fz(36px) Mb(-4px) D(ib)"})
        market_cap = soup.find('td', {"data-test":"MARKET_CAP-value"})
        name = soup.find('h1', {"class":"D(ib) Fz(18px)"})

        data = {
            "ticker":symbol,
            "name": name.text,
            "prev_close": prev_close.text,
            "open": open.text,
            "price": price.text,
            "market_cap" : market_cap.text,
            "timestamp": datetime.now()
        }

        return data
    except Exception as e:
        pass


def get_most_active_stocks():
    '''get the most active stocks of the day'''

    url = f'https://finance.yahoo.com/most-active'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        most_active = []

        table_data_faded = soup.find_all("tr", {"class":"simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv2BgColor)"})
        table_data_not_faded = soup.find_all("tr", {"class": "simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv1BgColor)"})
        
        table_data = table_data_faded + table_data_not_faded
        
        for td in table_data:
            symbol = td.find("a", {"data-test": "quoteLink"}).text
            name = td.find("td", {"class": "Va(m) Ta(start) Px(10px) Fz(s)"}).text
            price = td.find("fin-streamer", {"data-field": "regularMarketPrice"}).text
            change = td.find("fin-streamer", {"data-field": "regularMarketChange"}).text
            percent_change = td.find("fin-streamer", {"data-field": "regularMarketChangePercent"}).text
            volume = td.find("fin-streamer", {"data-field": "regularMarketVolume"}).text
            market_cap = td.find("fin-streamer", {"data-field": "marketCap"}).text

            data = {
                "symbol": symbol,
                "name": name,
                "price": price,
                "change": change,
                "percent_change": percent_change,
                "volume": volume,
                "market_cap": market_cap
            }

            most_active.append(data)
        
        dataframe = pd.DataFrame(most_active)
        dataframe.dropna()

        dataframe.to_excel("most_active_stock_data.xlsx", index=False)

        return "Fin!"

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

def main():
    '''Main Function'''

    data = []
    symbols = get_all_symbols()

    for symbol_list in symbols:
        data.extend(symbol_list)

    create_excel_file(data)

    print("\n\nfin!")

if __name__ == '__main__':
    # pprint(get_all_symbols())
    # main()
    pprint(get_most_active_stocks())



   
