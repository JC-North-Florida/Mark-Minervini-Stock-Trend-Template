#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import yfinance as yf
import pandas_datareader as pdr
import datetime as dt
import matplotlib.pyplot as plt
import mplfinance as mpf
import time
import csv


#To display the plots
#get_ipython().run_line_magic('matplotlib', 'inline')

#Remove warnings
#pd.options.mode.chained_assignment = None  # default='warn'
time.sleep(5)


# In[2]:


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


# In[3]:


def isStage2(df):
    # Stage 2 for young or more mature stock
    # Removed the 150
    # df['close'].iloc[-1] > df['close'].max()*0.7 and \
    # Removed two year break, because IBD still recommends stocks within 2 years. 
    # secondHalfHighTwoYears > firstHalfHighTwoYears*0.9 and \
    # Note to self... I have seen when price is over all, but 50 is under 200 (trending), it does set up. 50 turned up********
    df = df.reset_index()
    
    
    if len(df.index) > 302:
        dfOneYear = df.tail(252)
        dfLowOneYears = dfOneYear['Low'].min()
        dfLowOneYearsLoc = dfOneYear['Low'].idxmin() 
        # High after the 52 week low.
        dfAfter52WeekLow = df['High'].iloc[dfLowOneYearsLoc+1:]
        dfHighAfter52WeekLow = dfAfter52WeekLow.max()
        # This is a new rule to try to get the all time or two year high. Within 95% of that high.
        firstHalfHighTwoYears = df['High'].head(200).max()
        secondHalfHighTwoYears = df['High'].tail(200).max()
        # Within 25% of 52 week high. The closer the better.
        dfHighOneYears = dfOneYear['High'].max()
        within25PerHigh = ((dfHighOneYears - df['Close'].iloc[-1]) / dfHighOneYears)*100

        # Changes I've made...
        # Moved to within 15%, not 25%. (O'neil) Compromise 20%
        # within25PerHigh <= 25.0 and \
        # Changed from 30% to 50%. Back to 30% because of AVGO.
        # dfHighAfter52WeekLow > dfLowOneYears*1.3 and \
        
        
        if df['Adj Close'].iloc[-1] > df['SMA200'].iloc[-1] and \
                df['Adj Close'].iloc[-1] > df['SMA150'].iloc[-1] and \
                df['Adj Close'].iloc[-1] > 10.00 and \
                df['SMA50'].iloc[-1] > df['SMA200'].iloc[-1] and \
                df['SMA50'].iloc[-1] > df['SMA150'].iloc[-1] and \
                df['AvgVolume'].iloc[-1] > 100000.00 and \
                df['SMA50'].iloc[-1] > df['SMA200'].iloc[-1] and \
                df['SMA150'].iloc[-1] > df['SMA200'].iloc[-1] and \
                dfOneYear['Close'].iloc[-1] > dfOneYear['High'].max()*0.7 and \
                dfHighAfter52WeekLow > dfLowOneYears*1.3 and \
                within25PerHigh <= 20.0 and \
                df['SMA200'].iloc[-1] > df['SMA200'].iloc[-110]:
            print("Added")
            return "yes"
        else:
            pass

    # For Older IPO stocks
    # df['SMA20'].iloc[-1] > df['SMA50'].iloc[-1] and \
    elif len(df.index) > 202:
        if df['Close'].iloc[-1] > df['SMA200'].iloc[-1] and \
                df['SMA50'].iloc[-1] > df['SMA200'].iloc[-1] and \
                df['SMA50'].iloc[-1] > df['SMA50'].iloc[-10] and \
                df['SMA50'].iloc[-1] > df['SMA150'].iloc[-1] and \
                df['SMA150'].iloc[-1] > df['SMA200'].iloc[-1] and \
                df['AvgVolume'].iloc[-1] > 100000.00 and \
                df['Close'].iloc[-1] > 12.00:
            return "ipo-older"
        else:
            pass
            
    # For Younger IPO stocks
    elif len(df.index) > 52:
        if df['Close'].iloc[-1] > df['SMA50'].iloc[-1] and \
                df['SMA20'].iloc[-1] > df['SMA50'].iloc[-1] and \
                df['Close'].iloc[-1] > 12.00:
            return "ipo"
        else:
            pass
            
    elif len(df.index) > 22:
        highLowDif = ((df['High'].max() - df['Low'].min())/df['Low'].min())*100
        if df['Close'].iloc[-1] > df['SMA20'].iloc[-1] and df['SMA10'].iloc[-1] > df['SMA20'].iloc[-1] and \
                df['Close'].iloc[-1] > 12.00 and highLowDif < 40.0:
            return "ipo"
        else:
            pass

    elif len(df.index) > 6:
        highLowDif = ((df['High'].max() - df['Low'].min())/df['Low'].min())*100
        if df['Close'].iloc[-1] > 12.00 and highLowDif < 40.0 and \
                df['Close'].iloc[-1] > df['SMA5'].iloc[-1]:
            return "ipo"
        else:
            pass


    else:
        #print("Nothing going on")
        return "no"
    
    


# # Main Loop

# In[4]:


StockList = []
IPOList = []
PowerPlay = []
IPOOlderList = []



# import tickers
# df = pd.read_csv("/home/debian/notebooks/Run_on_Fridays/RS_HIGH.csv")
df = pd.read_csv("IBD-Data.csv")

tickers = df['Symbol'].tolist()

time.sleep(4)



for ticker in tickers:
    print(ticker)
    df = RunStockToGraph(ticker,"2y","1d", "Daily")
    time.sleep(1)
    
    # Calculate Stage 2 also IPO
    if isStage2(df) == "yes":
        StockList.append(ticker)
        
    elif isStage2(df) == "ipo":
        IPOList.append(ticker)

    elif isStage2(df) == "ipo-older":
        IPOOlderList.append(ticker)

    
        
    # Calculate powerplay
    if len(df.index) > 230:
        # Use 70 is 8 weeks for power play and consider the 6 weeks of the max size base of the Power Play. So I used 67 days...
        powerPlayPer = (df['Adj Close'].tail(20).max()-df['Adj Close'].tail(67).min())/abs(df['Adj Close'].tail(67).min())

        powerPlayHigh = df['High'].iloc[-50].max()

        powerPlayLow = df['Low'].iloc[-5].min()

        powerBaseHigh = df['High'].iloc[-8:].max()

        powerBaseLow = df['Low'].iloc[-8:].min()

        powerBaseDepth = ((powerBaseHigh - powerBaseLow)/powerBaseHigh)*100

        # I don't know why I did this one.. It's just the difference of two distinct periods. Not two range of periods. 
        PowerPlayPerDif = ((powerPlayHigh-powerPlayLow)/powerPlayHigh)*100

        # New power play 100% in 8 weeks calculation.

        dfPP = df

        dfPP.reset_index(inplace=True)

        print(str(dfPP.tail(10)))
        
        # Price High
        sixWeekHigh = dfPP['High'].iloc[-30:].max()
        # Index High
        sixWeekHighIndex = dfPP['High'].iloc[-30:].idxmax()

        # Price Low of 8 weeks from the Index point.
        sixWeekLow = dfPP['Low'].iloc[sixWeekHighIndex-40:sixWeekHighIndex].min()

        eightWeekOneHundredPercent = ((sixWeekHigh - sixWeekLow)/sixWeekLow)*100

        print("JC the Value of SIX week high is: " + str(sixWeekHigh) + " with index: " + str(sixWeekHighIndex) + " 8 week low of " + str(sixWeekLow) + " Percentage: " + str(eightWeekOneHundredPercent))

        if eightWeekOneHundredPercent > 95.0 and \
                df['Adj Close'].iloc[-1] > df['SMA200'].iloc[-1] and \
                df['Adj Close'].iloc[-1] > 10.00 and \
                df['SMA50'].iloc[-1] > df['SMA200'].iloc[-1] and \
                df['SMA50'].iloc[-1] > df['SMA150'].iloc[-1] and \
                df['SMA150'].iloc[-1] > df['SMA200'].iloc[-1] and \
                df['SMA200'].iloc[-1] > df['SMA200'].iloc[-30] and powerBaseDepth <= 22.0:

            # Daily 8 days for PowerPlay Base. Should be 10-12 day base according to Minervini
            for rs_item in range(-8, -50, -1):

                # Maybe something like this...
                print("Index: " + str(rs_item) + " High Value: " + str(df['High'].iloc[rs_item]))

                # If RS left and right are less, add to List and continue the for loop but 5 positions (weeks) after. 
                # Although it says RS, it's really using the High in the DataFrame. 

                if df['High'].iloc[rs_item] > df['High'].iloc[rs_item-1] and df['High'].iloc[rs_item] > df['High'].iloc[rs_item+1] and \
                        df['High'].iloc[rs_item] > df['High'].iloc[rs_item-2] and df['High'].iloc[rs_item] > df['High'].iloc[rs_item+2] and \
                        df['High'].iloc[rs_item] > df['High'].iloc[rs_item-3] and df['High'].iloc[rs_item] > df['High'].iloc[rs_item-4] and \
                        df['High'].iloc[rs_item]*1.0 > df['High'].iloc[rs_item+3] and df['High'].iloc[rs_item]*1.0 > df['High'].iloc[rs_item+4] and \
                        df['High'].iloc[rs_item]*1.0 > df['High'].iloc[rs_item+5]:
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

                    if percentageValue <= 25.0 and currentHighPercentage < 2.0:
                        print(str(ticker) + " Base " + str(rs_item) + " % base depth: " + str(percentageValue) + " % from Base High: " + str(currentHighPercentage))
                        PowerPlay.append([str(ticker), str(rs_item) + ' day base', str(percentageValue) + '%', str(topThird)])
                        break


# In[5]:


StockList


# In[6]:


IPOList


# In[7]:


len(StockList)


# In[8]:


with open('/home/debian/notebooks/Run_on_Fridays/sStock_List.csv', 'w') as f:
     
    # using csv.writer method from CSV package
    write = csv.writer(f)
     
    write.writerow(StockList)
    #write.writerows(rows)
    
# with open('/home/debian/notebooks/Run_on_Fridays/sPower_Play_List.csv', 'w') as f:
     
#     # using csv.writer method from CSV package
#     write = csv.writer(f)
     
#     write.writerow(PowerPlay)
#     #write.writerows(rows)

with open('/home/debian/notebooks/Run_on_Fridays/sIPO_List.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Symbol'])
    for item in IPOList:
        writer.writerow([item,]) 

with open('/home/debian/notebooks/Run_on_Fridays/sIPO-Older_List.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Symbol'])
    for item in IPOOlderList:
        writer.writerow([item,]) 

PowerPlay.insert(0,['Symbol','Base Length','Base Depth', 'Top Third of Base'])
with open('/home/debian/notebooks/Run_on_Fridays/sPower_Play_List.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(PowerPlay)
#     # writer.writerow(['Symbol'])
#     # for item in PowerPlay:
#     #     writer.writerow([item,]) 

with open('/home/debian/notebooks/Run_on_Fridays/sFinal_Stock_List_Stage2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Symbol'])
    for item in StockList:
        writer.writerow([item,]) 

print("Program is Done")
# # End Program

# In[10]:

#get_ipython().system('pwd')
print("Done")


# In[ ]:
