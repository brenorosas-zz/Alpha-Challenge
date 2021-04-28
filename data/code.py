import pandas as pd
import os
dir = os.listdir('transactions')
tickers = set()
for file in dir:
    transaction_df = pd.read_csv("transactions/{}".format(file), sep = ';')
    transaction_list = transaction_df['TckrSymb'].tolist()
    print(len(transaction_list))
    for ticker in transaction_list:
        tickers.add(ticker)

tickers = pd.DataFrame({'TckrSymb' : list(tickers)})
tickers.to_csv('tickers.csv', index = False)