import yfinance as yf
import pandas as pd
import requests
import csv
import time

start = time.time()

API_Key = '6MKN651IJ6G2RXCS'

CSV_URL = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={API_Key}'
#url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={API_Key}'

with requests.Session() as s:
    
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)


stock = 'IBM'

ticker = yf.Ticker(stock)

dividends = ticker.dividends


income_statement = ticker.income_stmt


cashflows = ticker.cashflow

balance_sheet = ticker.quarterly_balance_sheet


def CFPerShare_qtr(stock):

    ticker = yf.Ticker(stock)

    income_statement_qtr = ticker.quarterly_income_stmt 
    cashflow_qtr = ticker.quarterly_cashflow
    income_statement_qtr = income_statement_qtr.transpose()
    cashflow_qtr = cashflow_qtr.transpose()

    df_CFPershare_qtr = pd.DataFrame(index=cashflow_qtr.index, columns=[stock])
    df_CFPershare_qtr[stock] = cashflow_qtr["Free Cash Flow"] / income_statement_qtr["Diluted Average Shares"]

    df_CFPershare_qtr = df_CFPershare_qtr.transpose()

    return df_CFPershare_qtr 

def CFPerShare(stock):

    ticker = yf.Ticker(stock)

    income_statement = ticker.income_stmt
    cashflows = ticker.cashflow
    income_statement = income_statement.transpose()
    cashflows = cashflows.transpose()

    df_CFPershare = pd.DataFrame(index=cashflows.index, columns=[stock])
    df_CFPershare[stock] = cashflows["Free Cash Flow"] / income_statement["Diluted Average Shares"]

    df_CFPershare = df_CFPershare.transpose()

    return df_CFPershare



CF_share_qtr = CFPerShare_qtr(stock)
CF_share = CFPerShare(stock)

print(CF_share_qtr)
print(CF_share)


df_CF_share_qtr = pd.DataFrame()
df_CF_share = pd.DataFrame()



for stock in my_list[1:]:
    
    try:
        df_CF_share_qtr = pd.concat([df_CF_share_qtr, CFPerShare_qtr(stock[0])])
        df_CF_share = pd.concat([df_CF_share, CFPerShare(stock[0])])
    except KeyError:
        pass

df_CF_share_qtr.to_excel('CF_Per_Share_qtr.xlsx', sheet_name='CF_Per_Share_qtr')
df_CF_share.toexcel('CF_Per_Share.xlsx', sheet_name='CF_Per_Share')

end = time.time()

print(f'Seconds: {end - start}')

#print(df_CF_share_qtr)

def main():
    pass

if __name__ == "__main__":
    main()