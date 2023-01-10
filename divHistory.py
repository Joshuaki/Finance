import requests
import pandas as pd
import numpy as np

def getData(func: str, ticker: str) -> dict:

    Alpha_Key = '6MKN651IJ6G2RXCS'

    Alpha_URL = "https://www.alphavantage.co/query"
    data = {
        "function": func,
        "symbol": ticker,
        "apikey": Alpha_Key
    }

    r = requests.get(Alpha_URL, params=data)

    result = r.json()

    return result

def divHistory(stock: str) -> pd.DataFrame():

    #get balance sheet and cashflow json data
    BS = getData('BALANCE_SHEET', stock)
    CF = getData('CASH_FLOW', stock)

    #convert balance sheet and cashflows into dataframes
    df_BS = pd.DataFrame(BS['quarterlyReports'])
    df_CF = pd.DataFrame(CF['quarterlyReports'])

    #merge balance sheet and cashflows into one dataframe
    df_BS_CF = pd.merge(df_BS, df_CF, how="left", on="fiscalDateEnding")

    #convert numeric strings into floats
    df_BS_CF = df_BS_CF.apply(pd.to_numeric, errors='coerce').fillna(df_BS_CF)

    #calculate dividendPershare from dividend payouts and dividends per share
    df_BS_CF["dividendPerShare"] = (df_BS_CF["dividendPayoutCommonStock"]/df_BS_CF["commonStockSharesOutstanding"])
    dividends = df_BS_CF[["fiscalDateEnding", "dividendPerShare"]]

    return dividends




dividendHistory = divHistory('IBM')



def main():
    pass

if __name__ == "__main__":
    main()

