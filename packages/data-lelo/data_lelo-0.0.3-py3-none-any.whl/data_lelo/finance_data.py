import datetime
import requests 
from dotenv import load_dotenv
import os
load_dotenv()

headers = {
    "cookie":os.environ.get("cookie"),
    "user-agent":os.environ.get("user-agent")
}

def fdata(symbol="INFY",start=None,end=None,interval=None,range=None):
    symbol=symbol+".NS"
    base_url = "https://query1.finance.yahoo.com/v8/finance/chart/"
    url=base_url+symbol
    parameters = {}
    if(interval):
        parameters["interval"]=interval

    if(start and end):
        date = datetime.datetime.strptime(start, "%d/%m/%y")
        period1 = str(int(date.timestamp()))
        date = datetime.datetime.strptime(end, "%d/%m/%y")
        period2 = str(int(date.timestamp()))
        parameters["period1"]=period1
        parameters["period2"] = period2
    elif(range):
        parameters["range"]=range
    res=requests.get(url,headers=headers,params=parameters)
    status=res.status_code

    if(status>=400):
        return "Request not processed"

    res=res.json()
    closing_prices = res["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    return closing_prices

# Purely for testing purposes 

# datetime.datetime.fromtimestamp(820434600)
# type(datetime.datetime.now().timestamp())
# date="15/09/95"
# date=datetime.datetime.strptime(date,"%d/%m/%y")
# print(str(int(date.timestamp())))
# url = "https://query1.finance.yahoo.com/v8/finance/chart/INFY.NS?range=1mo&interval=1d"
# parameters={
#     "range":"max"
# }
# res=requests.get(url,headers=headers,params=parameters)
# print(res.status_code)


# url = "https://query1.finance.yahoo.com/v8/finance/chart/INFY.NS?range=1mo&interval=1d"
# parameters={
#     "range":"1mo",
#     "interval":"1d"
# }
# res=requests.get(url,headers=headers,params=parameters)
# print(res.status_code)

validRanges=[
    "1d",
    "5d",
    "1mo",
    "3mo",
    "6mo",
    "1y",
    "2y",
    "5y",
    "10y",
    "ytd",
    "max"
]

granularity=[
    "1m", 
    "2m",
    "5m",
    "15m",
    "30m", 
    "60m", 
    "90m", 
    "1h", 
    "1d", 
    "5d", 
    "1wk", 
    "1mo", 
    "3mo"
]
