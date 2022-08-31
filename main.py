#importing all the libraries required
from time import time_ns
from alpaca_trade_api.rest import REST,TimeFrame
import requests


URL = "https://paper-api.alpaca.markets"
APIKEY = "Put your key here"
SECRETKEY = "Put your key here"





#starting alpaca
api = REST(APIKEY, SECRETKEY, URL)
account = api.get_account()

#threshold values to decide weather to sell or buy
UPWARDTHRES = 1.5
DIP_THRES = -2.25

PROFIT_THRES = 1.25
LOSS_THRES = -2.00

#global variables used for last price and tracking weather buying/selling
lastOpPrice = 100.00
isNextOpBuy = True


#main Function which decides weather to buy or sell given the current price
def Bot(request):

    global lastOpPrice
    global isNextOpBuy
    currentPrice = float(getPrice())
    percentageDiff = (currentPrice - lastOpPrice) / lastOpPrice * 100
    if isNextOpBuy:
        if percentageDiff >= UPWARDTHRES or percentageDiff <= DIP_THRES:
            lastOpPrice = placeBuyOrder()
            isNextOpBuy = False
    else:
        if percentageDiff >= PROFIT_THRES or percentageDiff <= LOSS_THRES:
            lastOpPrice = placeSellOrder()
            isNextOpBuy = True
    return {
        "code":"success",
        "Bought/Sold": "Success"
    }


#uses the coidesk api to get the price of BTC at the moment
def getPrice():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    price = (data["bpi"]["USD"]["rate"])
    price = price.replace(",","")
    fPrice = float(price)
    return fPrice

#places a buy order using all the money deposited in the account
def placeBuyOrder():
    buyingPower = account.cash
    print(buyingPower)
    quantity = int(float(buyingPower) / getPrice())
    print(getPrice())
    if (quantity > 0):
        order_buy = api.submit_order('BTCUSD', qty=quantity, side='buy', time_in_force='gtc')
    return getPrice()

#liquidates all assests
def placeSellOrder():
    getQuantity = api.get_position('BTCUSD').qty_available
    if (getQuantity > 0):
        order_sell = api.submit_order('BTCUSD',qty=getQuantity, side='sell', time_in_force='gtc')
    return getPrice()




