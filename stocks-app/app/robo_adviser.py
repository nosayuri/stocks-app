#Noemi Higashi
#Stock Recommendation App

import json
import os
import requests
import csv
import pdb
import datetime

api_key = "ALPHAVANTAGE_API_KEY"

#Welcome
print ("-----------------------------------")
print ("Welcome to the Stock Recommendation App")
symbol = input ("Input here the stock symbol (e.g. 'NFLX', 'AAPL', 'AMZN'): ")


#Error Messages
#with TRY we don't need to run, just validate. Exception means Error
try:
    float(symbol)
    quit ("Request Error. Please check the stock symbol")
except ValueError as e:
    pass
    print ("Issuing a request:")

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
response = requests.get(request_url)

response_body = json.loads(response.text)

if "Error Message" in response_body:
    print ("Symbol not valid. Please check your stock symbol (e.g. 'NFLX', 'AAPL', 'AMZN')")
    quit ("Stopping the program")

metadata = response_body["Meta Data"]
data = response_body["Time Series (Daily)"]
dates = list (data) #List of Dates Only
latest_day = dates[0]


#Adding data to CSV File
x = -1
list = []

for d in data:
    x+=1
    day_data = data [dates[x]]

    new_item = {
        "symbol":symbol,
        "timestamp":d,
        "open":day_data["1. open"],
        "high":day_data ["2. high"],
        "low":day_data ["3. low"],
        "close":day_data ["4. close"],
        "volume":day_data["5. volume"]
        }
    list.append (new_item)


#Writing prices to CSV file
def write_products_to_file(filename="prices.csv", list=[]):
    filepath = os.path.join(os.path.dirname(__file__), "..", "data", filename)
    print ("-----------------------------------")
    print(f"WRITING CONTENTS OF FILE: '{filepath}' ... WITH {symbol} PRICES")
    print ("-----------------------------------")

    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["symbol","timestamp","open","high","low","close","volume"])
        writer.writeheader() # uses fieldnames set above to write a dictionary
        for l in list:
            writer.writerow(l)

write_products_to_file (list=list)


#Running Calculations lists
len_data = len (data)-1
prices = []
x = -1
while x < len_data:
    x+=1
    x=int(x)
    seq_dates = data [dates[x]]
    prices.append (seq_dates)

open_prices = []
high_prices = []
low_prices = []
close_prices = []

for p in prices:
    open_prices.append (float(p["1. open"]))
    high_prices.append (float(p["2. high"]))
    low_prices.append (float(p["3. low"]))
    close_prices.append (float(p["4. close"]))

def mean(var):
    return (float(sum(var)) / int(len(var)))

#Calculations
latest_closing_price = close_prices[0]
latest_closing_price_format = "${0:,.2f}".format(float((latest_closing_price)))
max_high_prices = "${0:,.2f}".format(float(max(high_prices)))
min_low_prices = "${0:,.2f}".format(float(min(low_prices)))
max_close_prices = "${0:,.2f}".format(float(max(close_prices)))
average_high_prices = "${0:,.2f}".format(float(mean(high_prices)))
average_low_prices = "${0:,.2f}".format(float(mean(low_prices)))
now = datetime.datetime.now()
run_time = now.strftime("%I:%M %p on %B %d, %Y")
#

print (f"STOCK: {symbol}")
print (f"RUN AT: {run_time}")
print (F"LATEST DATA FROM: {latest_day}")
print (f"LATEST CLOSING PRICE FOR {symbol} IS {latest_closing_price_format}")
print (f"RECENT AVERAGE HIGH PRICE FOR {symbol} IS {average_high_prices}")
print (f"RECENT HIGHEST PRICE FOR {symbol} IS {max_high_prices}")
print (f"RECENT AVERAGE LOW PRICE FOR {symbol} IS {average_low_prices}")
print (f"RECENT LOWEST PRICE FOR {symbol} IS {min_low_prices}")
print ("-----------------------------------")


#Recommendations
total_mean = ((mean(low_prices))+(mean(high_prices)))/2

if ((0.96*(total_mean)) <= latest_closing_price < (1.01*(total_mean))) == True:
    print ("Recommendation: Wait")
    print ("Explanation: The stock latest closing price is within the regular range price of "
    + "${0:,.2f}".format(float(0.96*(total_mean))) + " and " + "${0:,.2f}".format(float (1.01*(total_mean))))

if ((0.94*(total_mean)) <= latest_closing_price < (0.96*(total_mean))) == True:
    print ("Recommendation: Buy (Level of Confidence: Low)")
    print ("Explanation: The stock latest closing price is within the low return range price of "
    + "${0:,.2f}".format(float(0.94*(total_mean))) + " and " + "${0:,.2f}".format(float (0.96*(total_mean))))

if ((0.90*(total_mean)) <= latest_closing_price < (0.94*(total_mean))) == True:
    print ("Recommendation: Buy (Level of Confidence: Medium)")
    print ("Explanation: The stock latest closing price is within the medium return range price of "
    + "${0:,.2f}".format(float(0.90*(total_mean))) + " and " + "${0:,.2f}".format(float (0.94*(total_mean))))

if (latest_closing_price < (0.90*(total_mean))) == True:
    print ("Recommendation: Buy (Level of Confidence: High)")
    print ("Explanation: The stock latest closing price exceeds the high return range price of "
    + "${0:,.2f}".format(float(0.90*(total_mean))))

if ((1.01*(total_mean)) <= latest_closing_price < (1.03*(total_mean))) == True:
    print ("Recommendation: Sell (Level of Confidence: Low)")
    print ("Explanation: The stock latest closing price is within the low return range price of "
    + "${0:,.2f}".format(float(1.01*(total_mean))) + " and " + "${0:,.2f}".format(float (1.03*(total_mean))))

if ((1.03*(total_mean)) <= latest_closing_price < (1.05*(total_mean))) == True:
    print ("Recommendation: Sell (Level of Confidence: Medium)")
    print ("Explanation: The stock latest closing price is within the medium return range price of "
    + "${0:,.2f}".format(float(1.03*(total_mean))) + " and " + "${0:,.2f}".format(float (1.05*(total_mean))))

if (latest_closing_price > (1.05*(total_mean))) == True:
    print ("Recommendation: Sell (Level of Confidence: High)")
    print ("Explanation: The stock latest closing price exceeds the high return range price of "
    + "${0:,.2f}".format(float(1.05*(total_mean))))
