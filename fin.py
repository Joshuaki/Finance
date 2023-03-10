import requests
import csv
import options
import pandas as pd
import datetime 
import time

#Starting timestamp to check how long script takes
start = time.time()

print(datetime.datetime.now())

API_Key = '6MKN651IJ6G2RXCS'

CSV_URL = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={API_Key}'
#url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={API_Key}'

with requests.Session() as s:
    
    download = s.get(CSV_URL, verify=False)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)

    # for row in my_list:
    #     print(row)

with open('tickers.csv', 'w', newline='') as csvfile:
    tickerwriter = csv.writer(csvfile)
    tickerwriter.writerows(my_list)

#df = pd.DataFrame(my_list[1:], columns=my_list[0])
#print (df)



options_stats = {}
for stock in my_list:
    
    try:
        #print(stock[0])
        stats = options.iv_stats(stock[0]) 
        options_stats[stock[0]] = stats[stock[0]]   
    except AttributeError:
        pass


#print(options_stats)


options_stats_df = pd.DataFrame(options_stats)
options_stats_df = options_stats_df.transpose()

today = datetime.date.today()
options_stats_df.to_excel(f'options_stats{today}.xlsx', sheet_name=f'options_stats_{today}')

end = time.time()

print(f'Seconds: {end - start}')



def main():
    pass

if __name__ == "__main__":
    main()






