#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import numpy as np
import yfinance as yf
import pandas_datareader as pdr
import datetime as dt
import matplotlib.pyplot as plt
import mplfinance as mpf
import time
import csv
import psycopg2 as pg2


#To display the plots
#get_ipython().run_line_magic('matplotlib', 'inline')

#Remove warnings
pd.options.mode.chained_assignment = None  # default='warn'
time.sleep(4)


now = dt.datetime.now()

start_time = now.strftime("%m/%d/%Y - %H:%M:%S")


def RunStockToGraph(ticker, myperiod, myinterval, timePeriod):
    # Get the Dataframe data from Yahoo Finance Ready for Pandas. 
    df = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers = ticker,

            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            period = myperiod,

            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            interval = myinterval,

            # group by ticker (to access via data['SPY'])
            # (optional, default is 'column')
            group_by = 'column',
            #group_by = 'ticker',

            # adjust all OHLC automatically
            # (optional, default is False)
            auto_adjust = False,

            # download pre/post regular market hours data
            # (optional, default is False)
            prepost = True,

            # use threads for mass downloading? (True/False/Integer)
            # (optional, default is True)
            threads = True,
        )
    
    time.sleep(2)
    # Eliminate all Rows with NaN data. 
    df = df.dropna()

    df['SMA5'] = df['Close'].rolling(5).mean()
    df['SMA10'] = df['Close'].rolling(10).mean()
    df['SMA20'] = df['Close'].rolling(20).mean()
    df['SMA50'] = df['Close'].rolling(50).mean()
    df['SMA150'] = df['Close'].rolling(150).mean()
    df['SMA200'] = df['Close'].rolling(200).mean()
    df['AvgVolume'] = df['Volume'].rolling(50).mean()
    
    return df




# # Main Loop

tickers = []

# Get all Tickers from Nasdaq CSV

# import tickers
df = pd.read_csv("nasdaq.csv")

tickers = df['Symbol'].str.strip().tolist()

print(tickers)
print(len(tickers))


time.sleep(2)

roc_List = []
rs_List = []
rs_List2 = []

dfSPY = RunStockToGraph("SPY","2y","1wk", "Weekly")

time.sleep(3)

for ticker in tickers:
    if "^" not in ticker:
        print(ticker)
        df = RunStockToGraph(ticker,"2y","1wk", "Weekly")
        # time.sleep(1)
    else:
        continue
    
    # Test for ROC value.
    # This ROC calculation is not testing for Stage 2.
    # df['Close'].iloc[-1] > 10.00 and \
            # df['AvgVolume'].iloc[-1] > 25000.00:
    if len(df.index) >= 52:
        rocThirdQtr = 0
        rocFourthQtr = 0
        rocSecondQtr = 0
        rocFirstQtr = 0

        # rocFourthQtr = ((df['High'].iloc[-1] - df['High'].iloc[-62]) / df['High'].iloc[-62]) * 100

        # rocFirstQtr = ((df['High'].iloc[-190] - df['High'].iloc[-252]) / df['High'].iloc[-252]) * 100

        # rocSecondQtr = ((df['High'].iloc[-127] - df['High'].iloc[-189]) / df['High'].iloc[-189]) * 100

        # rocThirdQtr = ((df['High'].iloc[-63] - df['High'].iloc[-126]) / df['High'].iloc[-126]) * 100

        # Run RS O'neil Style from Formula found on YouTube.

        rocFourthQtr = ((df['High'].iloc[-1] - df['High'].iloc[-13]) / df['High'].iloc[-13]) * 100

        rocFirstQtr = ((df['High'].iloc[-1] - df['High'].iloc[-52]) / df['High'].iloc[-52]) * 100

        rocSecondQtr = ((df['High'].iloc[-1] - df['High'].iloc[-39]) / df['High'].iloc[-39]) * 100

        rocThirdQtr = ((df['High'].iloc[-1] - df['High'].iloc[-26]) / df['High'].iloc[-26]) * 100

        roc_calculation = 0
        roc_calculation = (rocFourthQtr*0.4) + (rocFirstQtr*0.2) + (rocSecondQtr*0.2) + (rocThirdQtr*0.2) 
        roc_List.append([ticker, roc_calculation])


        # This is RS Calculation. 
        rsThirdQtr = 0
        rsFourthQtr = 0
        rsSecondQtr = 0
        rsFirstQtr = 0


        # Formula from Youtube Video for RS value More Weighted Quarters.
        rsFourthQtr = (((df['High'].iloc[-1]/dfSPY['High'].iloc[-1]) - (df['High'].iloc[-13]/dfSPY['High'].iloc[-13])) / (df['High'].iloc[-13]/dfSPY['High'].iloc[-13])) * 100
        rsFirstQtr = (((df['High'].iloc[-1]/dfSPY['High'].iloc[-1]) - (df['High'].iloc[-52]/dfSPY['High'].iloc[-52])) / (df['High'].iloc[-52]/dfSPY['High'].iloc[-52])) * 100
        rsSecondQtr = (((df['High'].iloc[-1]/dfSPY['High'].iloc[-1]) - (df['High'].iloc[-39]/dfSPY['High'].iloc[-39])) / (df['High'].iloc[-39]/dfSPY['High'].iloc[-39])) * 100
        rsThirdQtr = (((df['High'].iloc[-1]/dfSPY['High'].iloc[-1]) - (df['High'].iloc[-26]/dfSPY['High'].iloc[-26])) / (df['High'].iloc[-26]/dfSPY['High'].iloc[-26])) * 100

        rs_calculation = 0
        rs_calculation = (rsFourthQtr*0.4) + (rsFirstQtr*0.2) + (rsSecondQtr*0.2) + (rsThirdQtr*0.2) 
        rs_List.append([ticker, rs_calculation])


        # This is RS Calculation Ryan Each Quarter (Straight Forward). 
        rsThirdQtr = 0
        rsFourthQtr = 0
        rsSecondQtr = 0
        rsFirstQtr = 0

        # Like Ryan said in YouTube
        rsFourthQtr = (((df['High'].iloc[-1]/dfSPY['High'].iloc[-1]) - (df['High'].iloc[-13]/dfSPY['High'].iloc[-13])) / (df['High'].iloc[-13]/dfSPY['High'].iloc[-13])) * 100
        rsThirdQtr = (((df['High'].iloc[-14]/dfSPY['High'].iloc[-14]) - (df['High'].iloc[-26]/dfSPY['High'].iloc[-26])) / (df['High'].iloc[-26]/dfSPY['High'].iloc[-26])) * 100
        rsSecondQtr = (((df['High'].iloc[-27]/dfSPY['High'].iloc[-27]) - (df['High'].iloc[-39]/dfSPY['High'].iloc[-39])) / (df['High'].iloc[-39]/dfSPY['High'].iloc[-39])) * 100
        rsFirstQtr = (((df['High'].iloc[-40]/dfSPY['High'].iloc[-40]) - (df['High'].iloc[-52]/dfSPY['High'].iloc[-52])) / (df['High'].iloc[-52]/dfSPY['High'].iloc[-52])) * 100

        rs_calculation = 0
        # rs_calculation = (rsFourthQtr*0.4) + (rsFirstQtr*0.1) + (rsSecondQtr*0.2) + (rsThirdQtr*0.2) 
        rs_calculation = (rsFourthQtr*0.4) + (rsFirstQtr*0.2) + (rsSecondQtr*0.2) + (rsThirdQtr*0.2) 
        # rs_List_Ryan.append([ticker, rs_calculation])
        rs_List2.append([ticker, rs_calculation])
        


roc_List = sorted(roc_List,key=lambda l:l[1], reverse=True)
df = pd.DataFrame(roc_List, columns=['Symbol', 'RS_Value'])
df['Position'] = len(df) - df.index.values
df['RS_Rank'] = (df['Position']*99/len(df)).round()
roc_List = df.values.tolist()
roc_List.insert(0,['Symbol','RS_Value','Position','RS_Rank'])

rs_List = sorted(rs_List,key=lambda l:l[1], reverse=True)
df = pd.DataFrame(rs_List, columns=['Symbol', 'RS_Value'])
df['Position'] = len(df) - df.index.values
df['RS_Rank'] = (df['Position']*99/len(df)).round()
rs_list = df.values.tolist()
rs_List.insert(0,['Symbol','RS_Value','Position','RS_Rank'])

rs_List2 = sorted(rs_List2,key=lambda l:l[1], reverse=True)
df = pd.DataFrame(rs_List2, columns=['Symbol', 'RS_Value'])
df['Position'] = len(df) - df.index.values
df['RS_Rank'] = (df['Position']*99/len(df)).round()
rs_List2 = df.values.tolist()
rs_List2.insert(0,['Symbol','RS_Value','Position','RS_Rank'])



          
with open('WeeklyROC_List.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # writer.writerow()
    # writer.writerow(['Symbol','ROC_Value'])
    writer.writerows(roc_List)

with open('WeeklyRS_ListWeighted.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # writer.writerow()
    # writer.writerow(['Symbol','ROC_Value'])
    writer.writerows(rs_List)

with open('RSWeekly_List_RyanStraight.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # writer.writerow()
    # writer.writerow(['Symbol','ROC_Value'])
    writer.writerows(rs_List2)


print("Done")
# # End Program

now = dt.datetime.now()

current_time = now.strftime("%m/%d/%Y - %H:%M:%S")
print("Started at: ", start_time)
print("Ended at: ", current_time)

print("Program is Done")

#get_ipython().system('pwd')
print("Done")
