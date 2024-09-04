#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime as dt
import json
import urllib
import pandas as pd
import numpy as np
import yfinance as yf
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import mplfinance as mpf
import time
import csv
import os
import requests


#To display the plots
# get_ipython().run_line_magic('matplotlib', 'inline')

#Remove warnings
pd.options.mode.chained_assignment = None  # default='warn'
time.sleep(4)


# In[2]:


# Get DF data for S&P 500 to then be able to calculate the RS Line (Higher RS in Base)
dfSP = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = "^GSPC",

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "1y",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = "1d",

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

time.sleep(4)
# Eliminate all Rows with NaN data. 
dfSP = dfSP.dropna()

dfSP['SMA20'] = dfSP['Close'].rolling(20).mean()
dfSP['SMA50'] = dfSP['Close'].rolling(50).mean()
dfSP['SMA200'] = dfSP['Close'].rolling(200).mean()
dfSP['AvgVolume'] = dfSP['Volume'].rolling(50).mean()


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
    
    df['SMA20'] = df['Close'].rolling(20).mean()
    df['SMA50'] = df['Close'].rolling(50).mean()
    df['SMA150'] = df['Close'].rolling(150).mean()
    df['SMA200'] = df['Close'].rolling(200).mean()
    df['AvgVolume'] = df['Volume'].rolling(50).mean()
    df['SandP500Close'] = dfSP['Close']
    #df['RS'] = (df['Close']/df['SandP500Close'])*100
    
    time.sleep(2)
    
    return df


# In[5]:


StockList = []
BaseSymbolList = []


df = pd.read_csv("sFinal_Stock_List_Stage2.csv")

tickers = df['Symbol'].tolist()

# Add Symbols for Cryptocurrency
tickers.append('ETHE')
tickers.append('MSTR')
tickers.append('GBTC')

# For Testing
# tickers = ["RAPT", "LWAY", "MDB"]

time.sleep(2)

print(tickers)

time.sleep(2)

# Sample List TEMPORARY
# tickers = ["IR"]


# In[10]:


for ticker in tickers:
    try:
        print(ticker)
        df = RunStockToGraph(ticker,"2y","1wk", "Weekly") # Used 1 year, because I still need to calculate the 50 SMA.
        # time.sleep(2)
        
        print(df.tail(10))

        price_vcp_index = []
        price_vcp_value = []

        for rs_item in range(-4, -len(df), -1):

            # Maybe something like this...
            print("Index: " + str(rs_item) + " High Value: " + str(df['High'].iloc[rs_item]))

            # If RS left and right are less, add to List and continue the for loop but 5 positions (weeks) after. 
            # Although it says RS, it's really using the High in the DataFrame. 

            # Removed to allow for flat base which starts at 4 weeks. 
                    # df['High'].iloc[rs_item]*1.02 > df['High'].iloc[rs_item+3] and df['High'].iloc[rs_item]*1.02 > df['High'].iloc[rs_item+4] and \
                    # df['High'].iloc[rs_item]*1.05 > df['High'].iloc[rs_item+5]:

            if df['High'].iloc[rs_item] > df['High'].iloc[rs_item-1] and df['High'].iloc[rs_item] > df['High'].iloc[rs_item+1] and \
                    df['High'].iloc[rs_item] > df['High'].iloc[rs_item-2] and df['High'].iloc[rs_item] > df['High'].iloc[rs_item+2] and \
                    df['High'].iloc[rs_item] > df['High'].iloc[rs_item-3] and df['High'].iloc[rs_item] > df['High'].iloc[rs_item-4] and \
                    df['High'].iloc[rs_item]*1.0 > df['High'].iloc[rs_item+3] and df['High'].iloc[rs_item]*1.0 > df['High'].iloc[rs_item+4]:
                print("Base High " + str(rs_item) + " vs " + str(rs_item-1) + " and " + str(rs_item+1))
                print(df['High'].iloc[rs_item])
                # Now that we have the high, Find the low.
                priceHigh = df['High'].iloc[rs_item]
                priceLow = df['High'].iloc[rs_item] # Setting a temporary high number just to get the ball rolling on the for loop.
                priceLowRange = []
                
                # Find the low
                for priceLowItem in range(rs_item, -1, 1):
                    print("Index " + str(priceLowItem) + " Current Low: " + str(priceLow) + " Test Value: " + str(df['Low'].iloc[priceLowItem + 1]))
                    if priceLow >= df['Low'].iloc[priceLowItem + 1]:
                        print("Found price low on loop: " + str(priceLowItem))
                        priceLow = df['Low'].iloc[priceLowItem+1]
                        print("Lower index is: " + str(priceLowItem+1) + " " + str(priceLow))
                    
#                 # Calculate the % Difference from High to Low. 
#                 percentageValue = ((priceHigh - priceLow) / priceHigh)*100

#                 if percentageValue <= 7.5:
#                     print("We found a Base")
#                     StockList.append(str(ticker) + " Base " + str(rs_item) + " Percentage: " + str(round(percentageValue,2)) + "%")

                print("This is the Low: " + str(df['Low'].iloc[rs_item+1:].min()))
                baseHigh = df['High'].iloc[rs_item]
                baseLow = df['Low'].iloc[rs_item+1:].min()
                currentHigh = df['High'].iloc[rs_item+1:].max()

                # Calculate Base thirds
                thirds = (baseHigh - baseLow)/3
                topThird = baseHigh - thirds
                middleThird = baseHigh - (thirds*2)
                
                # Base Depth
                percentageValue = ((baseHigh - baseLow) / baseHigh)*100
                
                # Dif from base high and current high. 
                currentHighPercentage = ((currentHigh - baseHigh) / baseHigh)*100

                # 7% used to be within 5%. But some stocks go up higher then setup again as a VCP. 
                # Changed from 4 week flat base... Instead of -5, should be -4 (for flat base)
                if percentageValue <= 15.0 and currentHighPercentage < 10.0 and percentageValue >= 3.5 and rs_item < -4:
                    print(str(ticker) + " Flat Base " + str(rs_item) + " % base depth: " + str(percentageValue) + " % from Base High: " + str(currentHighPercentage))
                    StockList.append([str(ticker), str(rs_item) + ' week TIGHT base', str(percentageValue) + '%', str(topThird)])
                    BaseSymbolList.append(ticker)

                elif percentageValue < 50.0 and currentHighPercentage < 10.0 and percentageValue >= 3.5 and rs_item < -5:
                    print(str(ticker) + " Base " + str(rs_item) + " % base depth: " + str(percentageValue) + " % from Base High: " + str(currentHighPercentage))
                    StockList.append([str(ticker), str(rs_item) + ' week base', str(percentageValue) + '%', str(topThird)])
                    BaseSymbolList.append(ticker)

                elif percentageValue < 50.0 and currentHighPercentage < 10.0 and percentageValue >= 3.5 and rs_item < -4:
                    print(str(ticker) + " Base " + str(rs_item) + " % base depth: " + str(percentageValue) + " % from Base High: " + str(currentHighPercentage))
                    StockList.append([str(ticker), str(rs_item) + ' week SHORT base', str(percentageValue) + '%', str(topThird)])
                    BaseSymbolList.append(ticker)
                    
    
                
                # Calculate the % Difference between high and low.
                # If the % is within 8%, add it to the list.
                # price_high_index.append(rs_item)
                # price_high_value.append(df['High'].iloc[rs_item])
                break
                
            # Check base almost a year. 
            # Seems like a lot for the way I'm currently playing. 
            if rs_item < -52:
                break
    except Exception as e:
        print("The error is: ",e)


StockList.insert(0,['Symbol','Base Length','Base Depth', 'Top Third of Base', 'Base Count', '1 yr Supply', 'Notes', 'RS Weekly', 'Shares Outstanding', 'QTR %', 'QTR Avg','QTR Curr','Sales %','Margin','Earnings Date','Comp','RS Rating', 'IPO Date'])

with open('Base_Stock_List.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # writer.writerow(['Symbol'])
    writer.writerows(StockList)
    # for item in StockList:
    #     writer.writerow([item,])
        


print("Done with Base Code")