import requests
from pprint import pprint
from bs4 import BeautifulSoup


def get_quote(symbol):
    '''Get Symbol Data'''

    symbol = symbol.upper()
    URL = f"https://finance.yahoo.com/quote/{symbol}"

    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "Referer": "https://www.google.com"
        }

    response = requests.get(URL, headers=headers)

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

while True:
    pprint(get_quote('FB'))
