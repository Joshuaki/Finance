import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
import requests


def get_implied_volatility(ticker: str) -> pd.DataFrame():

    #create a blank dataframe
    options = pd.DataFrame()

    #retrieve options exporty dates
    stock = yf.Ticker(ticker)
    exps = stock.options

    #get options chain for each expiry
    for date in exps:
        option_chain = stock.option_chain(date)

        #print(option_chain)

        option_chain = pd.concat([option_chain.calls, option_chain.puts], keys=[f'calls{date}', f'puts{date}'])
        options = pd.concat([option_chain, options])

    options["lastTradeDate"] = options["lastTradeDate"].dt.tz_localize(None)

    return options

def iv_stats(ticker: str) -> dict:

    url = f'https://volafy.net/equity/{ticker}'
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    stats =  {}
    stats[ticker] = {}
    #print(soup.prettify())
    
    for child in soup.tbody.children:
        try:
            #print(child.th.contents, child.td.div.contents)
            stats[ticker][child.th.contents[0]] = child.td.div.contents[0]
        except AttributeError:
            #print(child.th.contents, child.td.contents)
            stats[ticker][child.th.contents[0]] = child.td.contents[0]
    

    
    #stats = soup.find_all('table')
    return stats



ticker = "AAPL"

#get implied volatility
implied_volatility = get_implied_volatility(ticker)

iv_statistics = iv_stats(ticker)

#print(iv_statistics)

#print(implied_volatility)

#implied_volatility.to_excel(f'implied_vol_{ticker}.xlsx', sheet_name="implied_vol")

def main():
    pass

if __name__ == "__main__":
    main()
