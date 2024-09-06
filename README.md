Mark Minervini is a 2 time US Investment Champion who was generous enough to share his strategy through his books. 

If you have not read any of his books, here are the links on Amazon. 

https://www.amazon.com/Books-Mark-Minervini/s?rh=n%3A283155%2Cp_27%3AMark+Minervini

All of them are a must read if you really want to learn how to invest in the stock market. 

As a token of appreciation to Mark and to give back to the community I have decided to publish how Mark Minervini filters out Momentum Stocks using his trend template with through this python code. 

This is meant for College or even High School students who have an understanding of how to code in Python and can modify it to their liking. This programs are not guarenteed or warrenteed by any means. This program is not endorsed by Mark Minervini (He would probably advice you to use MarketSurge). I haven't even met him or discussed any of this with him. Do your testing first. Also I am no financial adviser and am not giving financial advise. Basically test until they have real money to invest. Think of this program for use for educational purposes. Mark would probably want you to invest ASAP. Get real world experience with real money. This is just meant to help and test when on a budget before you really invest money.

Now the code might not be pretty, but it works. It was one of those situations where I just started coding and just wanted it to work

Step 1.

If you don't have the libraries I use on the code, you will have to install them (ie pip install pandas).


Step 2. 

If you don't have access to IBD Digital to filter out stocks that have an RS Value of 89+, download the entire stock list from Nasdaq.com (screener).

https://www.nasdaq.com/market-activity/stocks/screener

Rename the file nasdaq.csv and save it in the same directory as these python files. For better results also add/combine the ETF list that appears on the same website. What's important from the list is the Stock Ticker List (including the first header).

Run RS_Weekly-EntireDB.py
python3 RS_Weekly-EntireDB.py

Minervini does use the RS Values from IBD Digital, but by using some hints online, this program can calculate a similar value for RS. The point is to be in High Momentum Stocks and this program does just that. 

This program will take a while to run, so run it on a Friday night, so you can analyze stocks Saturday morning. Note, this code doesn't really deal very well with stocks younger than 1 year. So young IPO's can be found by runnnig Stocks_Stage_2.py (step 3) using the entire nasdaq.csv file. 

Get all the stocks that have an RS_Rank of 89 or 90+ and save them to a new CSV file called IBD-Data.csv. Save that file in the same directory as the Python files. The program produces 3 files, you can play with all of them, but I like WeeklyRS_ListWeighted.csv.


Step 3.

Run Stocks_Stage_2.py
python3 Stocks_Stage_2.py

This will produce serveral files including sPower_Play_List.csv (the stocks have to be checked manually to make sure they are actually Power Plays as defined by Minervini) and sFinal_Stock_List_Stage2.csv (these are stocks in Stage 2 according to the Minervini Trend Template).

Here Minervini would probably manually check every single stock that is in this output file: sFinal_Stock_List_Stage2.csv

I like to make sure the stock is in an actual base, so I continue to step 4. 


Step 4. 

This code helps find stocks that are at least in a 5 week base. 

Run Stock_Base_Setup.py
python3 Stock_Base_Setup.py

The output file will be Base_Stock_List.csv

Now you have to manually check all these stocks and make sure they have good fundamentals. 

Again this is not a perfect process, but a simple way of doing this when on a budget would be to go to the SEC Edgar web-site. 

https://www.sec.gov/search-filings

Input the ticker symbol and find the 10-Q's and 10-K's for each stock on the list. 
Get the Revenue, Net Income, and Net Income Per Share on a quarterly and annual basis to calculate if the stock is growing (Operation or Operating Income and Revenue are very useful too). 
When in doubt, you can compare the data in Yahoo Finance or Wall Street Journal. 

And there you have it. 

Enjoy. 

And again thanks Mark Minervini, I'm grateful for what you've done for me and my investment.
