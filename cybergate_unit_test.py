import MetaTrader5 as mt
import pandas as pd 
import numpy as np
import plotly.express as px  
from datetime import datetime

import time


# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt.__author__)
print("MetaTrader5 package version: ",mt.__version__)

mt.initialize()


# In[71]:


# login to Trade Account with login()
# make sure that trade server is enabled in MT5 client terminal

# login = 80876458
# password = 'Passw0rd'
# server = 'Exness-MT5Trial9'

# mt.login(login, password, server)
# print(f"{login} has been logged in")

login = 80876458
password = 'Passw0rd'
server = 'Exness-MT5Trial9'

mt.login(login, password, server)
print(f"{login} has been logged in")


# In[72]:


# get account info
account_info = mt.account_info()
print(account_info)

# getting specific account data
login_number = account_info.login
balance = account_info.balance
equity = account_info.equity

print()  ## Returns empty space LIKE \r
print('login: ', login_number)
print('balance: ', balance)
print('equity: ', equity)


# In[73]:


# get number of symbols with symbols_total() Currency Pairs
num_symbols = mt.symbols_total()
 
# num_symbols


# In[74]:


# ["AUDUSDm", "GBPJPYm", "BTCUSDm", "EURUSDm"]
CURRENCY_PAIRS = "AUDUSDm"
INITIAL_PRICE = 0


# In[75]:


# get all symbols and their specifications
symbols = mt.symbols_get(CURRENCY_PAIRS)
sym = symbols[0]

# sym


# In[76]:


# get symbol specifications
symbol_info = mt.symbol_info(CURRENCY_PAIRS)._asdict()
# symbol_info

# print(type(symbol_info)) ## Returns A Dict


# In[77]:


# get current symbol price
symbol_price = mt.symbol_info_tick(CURRENCY_PAIRS)._asdict()
BID_PRICE = symbol_price['bid']
ASK_PRICE = symbol_price['ask']

# symbol_price
# BID_PRICE, ASK_PRICE


# In[78]:

# ohlc_data
ohlc_data = pd.DataFrame(mt.copy_rates_range(CURRENCY_PAIRS, 
                                             mt.TIMEFRAME_H1, 
                                             datetime(2022, 6, 21), 
                                             datetime.now()))

# fig = px.line(ohlc_data, x=ohlc_data['time'], y=ohlc_data['close'])
# test_fig = px.bar(ohlc_data, x=ohlc_data['time'], y=ohlc_data['close'])
### Candlesticks(ohlc_data, x=ohlc_data['time'], y=ohlc_data['close'])
# fig.show()

# ohlc_data['low']
# ohlc_data['high'][1]


# In[79]:


# requesting tick data
tick_data = pd.DataFrame(mt.copy_ticks_range(CURRENCY_PAIRS,
                                             datetime(2022, 6, 21), 
                                             datetime.now(), 
                                             mt.COPY_TICKS_ALL))

# fig = px.line(tick_data, x=tick_data['time'], y=[tick_data['bid'], tick_data['ask']])
# fig.show()
aa = px.scatter(ohlc_data, x=ohlc_data['time'], y=ohlc_data['close'])
# aa.show()
# tick_data


# In[80]:


# total number of orders
num_orders = mt.orders_total()
# num_orders


# In[81]:


# list of orders
orders = mt.orders_get()
# orders


# In[82]:


# total number of positions
num_positions = mt.positions_total()
# num_positions


# In[83]:


# list of positions
positions = mt.positions_get()

# positions[0]._asdict() #### Return it as a Dictionary
# ticket = positions[0]._asdict()['ticket'] ####### Return Single Ticket
# print(ticket)

# NOW Return All Tickets
tick_no = 1
for pos in positions:
    print(f"Ticket Number {tick_no}:", pos._asdict()['ticket'], pos._asdict()['price_open'], pos._asdict()['price_current'])
    ticketNumber = pos._asdict()['ticket']
    tick_no = tick_no + 1
# positions


# In[84]:


# number of history orders
num_order_history = mt.history_orders_total(datetime(2021, 1, 1), datetime(2022, 6, 22))
# num_order_history


# In[85]:


# list of history orders
order_history = mt.history_orders_get(datetime(2022, 6, 21), datetime(2022, 6, 21))
# order_history


# In[86]:


# get the number of deals in history
from_date=datetime(2022,5,21)
to_date=datetime.now()
deals=mt.history_deals_total(from_date, to_date)
if deals > 0:
    print("Total deals=", deals)
else:
    print("Deals not found in history")
# number of history deals
# num_deal_history = mt.history_deals_total(datetime(2022, 6, 21),  datetime(2022, 5, 21))
# num_deal_history


# In[87]:


# number of history deals

deal_history = mt.history_deals_get(datetime(2022, 6, 21), datetime(2022, 5, 21))
# deal_history


# # Support and Resistence

# Pivot Point Calculation
# The calculation for a pivot point is shown below:
# 
# Pivot point (PP) = (High + Low + Close) / 3
# 
# Support and resistance levels are then calculated off the pivot point like so:
# 
# First level support and resistance:
# 
# First resistance (R1) = (2 x PP) – Low
# 
# First support (S1) = (2 x PP) – High
# 
# Second level of support and resistance:
# 
# Second resistance (R2) = PP + (High – Low)
# 
# Second support (S2) = PP – (High – Low)
# 
# Third level of support and resistance:
# 
# Third resistance (R3) = High + 2(PP – Low)
# 
# Third support (S3) = Low – 2(High – PP)

# In[88]:


#### GET HIGH, LOW, CLOSE, OPEN
# ohlc_data
ohlc_data = pd.DataFrame(mt.copy_rates_range(CURRENCY_PAIRS, 
                                             mt.TIMEFRAME_D1, 
                                             datetime(2022, 6, 23), 
                                             datetime(2022, 6, 24)))
# df_plot_candles = px.line(ohlc_data, x=ohlc_data['high'], y=ohlc_data['low'])
# bb = df_plot_candles.show()
LOW = ohlc_data['low']
HIGH = ohlc_data['high']
OPEN = ohlc_data['open']
CLOSE = ohlc_data['close']
# print(HIGH, LOW, CLOSE)
# ohlc_data


# In[89]:


### GETTING THE HIGHEST AND LOWEST AND CLOSE
################# PIVOT POINT   #################
PP = (HIGH + LOW + CLOSE) / 3

###  PP ## Pivot Point
#   |||||     FIRST LEVEL SUPPORT AND RESISTANCE      |||||   #
R1 = (2 * PP) - LOW  # First_Resistance

S1 = (2 * PP) - HIGH  # First_Support

#   |||||     SECOND LEVEL SUPPORT AND RESISTANCE      |||||   #
R2 = PP + (HIGH - LOW)  # Second_Resistance

S2 = PP - (HIGH - LOW)  # Second_Support

#   |||||     THIRD LEVEL SUPPORT AND RESISTANCE      |||||   #
R3 = HIGH + 2 * (PP - LOW) # Third_Resistance

S3 = LOW - 2 * (HIGH - PP) # Third_Support



# In[90]:


### FIBONACCI PP
FR3 = PP + ((HIGH - LOW) * 1.000)
FR2 = PP + ((HIGH - LOW) * 0.618)
FR1 = PP + ((HIGH - LOW) * 0.382)

# PP

FS1 = PP - ((HIGH - LOW) * 0.382)
FS2 = PP - ((HIGH - LOW) * 0.618)
FS3 = PP - ((HIGH - LOW) * 1.000)



# ### Thinking of Adding PIP_BEFORE and PIP_AFTER

# In[91]:


# PIPS Positions
positions = mt.positions_get()
# PRICE = 0
def return_pip(percentage):
    if len(positions) > 0:
        # pip_num = 1
        for pips in positions:
            # print(f"pip Price {pip_num}:", pips._asdict()['price_current'])
            # pip_num = pip_num + 1
            price = pips._asdict()['price_current']
        # Calculating PIP
            pip,PRICE = (percentage/100) * price, price
            # print(pip, PRICE)
            return pip, PRICE
    else:
        price = ASK_PRICE
        # Calculating PIP
        pip, PRICE = (percentage/100) * price, price
        # print(pip, PRICE)
        return pip, PRICE

# def split_float(mypip):
#     '''split float into parts before and after the decimal'''
#     x = return_pip(mypip)
#     before, after = str(x).split('.')
#     return int(before), (int(after) if len(after) > 1 else int(after))

# split_float(0.1)
pip, PRICE = return_pip(0.1)
# print(pip, PRICE)

# return_pip(0.1)


# ### SETTING SL && TP

# In[92]:


####    ||||||||        SET   SL && TP       ||||||||   ######
SL = 0.0
TP = 0.0
def buyStopLost():
    """ Function to Return All Stop Loss Position """
    PP_SL = PP - pip
    R1_SL = R1 - pip
    R2_SL = R2 - pip
    R3_SL = R3 - pip
    return PP_SL, R1_SL, R2_SL, R3_SL

def buyTakeProfit():
    """ Returns All  Positions To Take Profit """
    PP_TP = R1 + pip
    S1_TP = R2 + pip
    S2_TP = R3 + pip
    S3_TP = S2 - pip
    return PP_TP, S1_TP, S2_TP, S3_TP

def sellStopLost():
    """ Function to Return All Stop Loss Position """
    PP_SL = PP + pip
    R1_SL = R1 + pip
    R2_SL = R2 + pip
    R3_SL = R3 + pip
    return PP_SL, R1_SL, R2_SL, R3_SL

def sellTakeProfit():
    """ Returns All  Positions To Take Profit """
    PP_TP = S1 + pip
    S1_TP = S2 + pip
    S2_TP = S3 + pip
    S3_TP = S3 + pip
    return PP_TP, S1_TP, S2_TP, S3_TP



# ### INITIALIZING A BUY || SELL STRATEGY

# In[93]:


# send order to the market
# documentation: https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py

# BUY
BUY_PP_SL, BUY_R1_SL, BUY_R2_SL,BUY_R3_SL = buyStopLost()
BUY_PP_TP, BUY_S1_TP, BUY_S2_TP, BUY_S3_TP = buyTakeProfit()
# SELL
SELL_PP_SL, SELL_R1_SL, SELL_R2_SL, SELL_R3_SL = sellStopLost()
SELL_PP_TP, SELL_S1_TP, SELL_S2_TP, SELL_S3_TP = sellTakeProfit()
# CURRENCY_PAIRS AS DEFINED ABOVE
# Buy
def Buy():
    # SL = 0.0
    # TP = 0.0
    ORDER_TYPE = mt.ORDER_TYPE_BUY
    request = {
        "action": mt.TRADE_ACTION_DEAL,
        "symbol": CURRENCY_PAIRS,
        "volume": 0.2, # FLOAT
        "type": ORDER_TYPE,
        "price": mt.symbol_info_tick(CURRENCY_PAIRS).ask,
        "sl": SL, # FLOAT
        "tp": TP, # FLOAT
        "deviation": 20, # INTERGER
        "magic": 234000, # INTERGER
        "comment": "Cybergate_BOT: STARTED",
        "type_time": mt.ORDER_TIME_GTC,
        "type_filling": mt.ORDER_FILLING_IOC,
    }
    order = mt.order_send(request)
    return order

# Buy()

#######     |||||||||||  Check Support && Resistence Before Initiating a Trade
# Sell
def Sell():
    # SL = SL else 0.0
    # TP = SL else 0.0
    ORDER_TYPE = mt.ORDER_TYPE_SELL
    request = {
        "action": mt.TRADE_ACTION_DEAL,
        "symbol": CURRENCY_PAIRS,
        "volume": 0.2, # FLOAT
        "type": ORDER_TYPE,
        "price": mt.symbol_info_tick(CURRENCY_PAIRS).bid,
        "sl": SL, # FLOAT
        "tp": TP, # FLOAT
        "deviation": 20, # INTERGER
        "magic": 234000, # INTERGER
        "comment": "Cybergate_BOT: STARTED",
        "type_time": mt.ORDER_TIME_GTC,
        "type_filling": mt.ORDER_FILLING_IOC,
    }
    order = mt.order_send(request)
    return order

# Sell()


# ### CLOSING A TRADE STRATEGY AND CONDITIONS

# In[94]:


# close position

def CloseTrade(e_SL, e_TP, POS, tick_no):
    # SL = SL else 0.0
    # TP = SL else 0.0
    request = {
        "action": mt.TRADE_ACTION_DEAL,
        "symbol": CURRENCY_PAIRS,
        "volume": 0.2, # FLOAT
        "type": mt.ORDER_TYPE_SELL,
        "position": tick_no, # select the position you want to close
        "price": mt.symbol_info_tick(CURRENCY_PAIRS).ask,
        "sl": e_SL, # FLOAT
        "tp": e_TP, # FLOAT
        "deviation": 20, # INTERGER
        "magic": 234000, # INTERGER
        "comment": "Cybergate_BOT: CLOSED",
        "type_time": mt.ORDER_TIME_GTC,
        "type_filling": mt.ORDER_FILLING_IOC,
    }
    order = mt.order_send(request)
    print(order, f"POS: {POS}")
    mt.Close(CURRENCY_PAIRS)

############  ||||||||||   CHECK SUPPORT AN RESISTANCE BEFORE CLOSING TRADE |||||

# order = mt.order_send(request)
# print(order)


# In[95]:


# Check Trade and Return the Closing Position
# def take_profit_or_stop_lost(currentPosition):
#     """ Return (price == currentPosition) """
#     PP_SL, R1_SL, R2_SL = sl()
#     if currentPosition == PP_SL or R1_SL or R2_SL:
#         CloseTrade(currentPosition, ticket_number)

#     PP_TP, S1_TP, S2_TP = tp()
#     if currentPosition == PP_TP or S1_TP or S2_TP:
#         CloseTrade(currentPosition, ticket_number)


# In[96]:


def split_float(num):
    '''split float into parts before and after the decimal'''
    x = num
    before, after = str(x).split('.')
    # return int(before), (int(after) if len(after) > 1 else int(after))
    newNum = int(before)
    return newNum

# Return Existing position
# position = mt.positions_get()
# position
def fetchExistingTrade():
    if num_positions > 0:
        """ CHeck for Existing Trade and Return their Props """
        for position in positions:
            POS = position._asdict()
            # print(POS)
            return POS['price_open']
    else:
        return 0.0

#### Implement Check Trade #############    CHECK FOR BUG in CHECKTRADE
def checkTrade(cp):
    p = fetchExistingTrade()
    ex_price = str(split_float(p))
    new_price = str(split_float(cp))
    # print(type(new_price), type(ex_price))
    if ex_price == new_price:
        # mt.Close(CURRENCY_PAIRS)
        return 1
    else:
        return 0

Buy()

try:
    while True:
        check = checkTrade(PRICE)
        if check < 1 & num_orders <= 4 & num_positions <= 4:   
            if np.all((PRICE >= (PP + pip)) & (PRICE <= (R1 - pip))):
                Buy()
                print(f"Buy Signal at PP {PRICE} 'PP + pip'= {PP + pip}")
                
            elif np.all((PRICE <= (PP - pip)) & (PRICE >= (S1 + pip))):
                Sell()
                print(f"Sell Signal at PP")

            elif np.all((PRICE >= (R1 + pip)) & (PRICE <= (R2 - pip))):
                Buy() #  BUY_R1_TP
                print(f"Buy Signal at R1")

            elif np.all((PRICE <= (R1 - pip)) & (PRICE >= (PP + pip))):
                Sell() #  SELL_R1_TP
                print(f"Sell Signal at R1")

            elif np.all((PRICE >= (R2 + pip)) & (PRICE <= (R2 - pip))):
                Buy() # BUY_R2_TP
                print(f"Buy Signal at {R2 + pip} : R2")

            elif np.all((PRICE <= (R2 - pip)) & (PRICE >= (R1 + pip))):
                Sell() # SELL_R2_TP
                print(f"Sell Signal at R2")

            elif np.all((PRICE >= (S1 + pip)) & (PRICE <= (PP - pip))):
                Buy()
                print(f"Buy Signal at S1")

            elif np.all((PRICE <= (S1 - pip)) & (PRICE >= (S2 - pip))):
                Sell() # SELL_S1_SL
                print(f"Sell Signal at S1")

            elif np.all((PRICE >= (S2 + pip)) & (PRICE <= (S1 - pip))):
                Buy() # BUY_S2_SL
                print(f"Buy Signal at S2")

            elif np.all((PRICE <= (S2 - pip)) & (PRICE >= (S3 + pip))):
                Sell()
                print(f"Sell Signal at S2")

            elif np.all((PRICE >= (S3 + pip)) & (PRICE <= (S2 - pip))):
                Buy()
                print(f"Buy Signal at S3")
                        
            else:
                # mt.Close(CURRENCY_PAIRS)s
                # print('Waiting for new signal...')
                check = 1
        time.sleep(60)

except:
    # CloseTrade(SL, TP, PRICE, ticketNumber)
    mt.shutdown()
    print("No Trade Match... shutting Down (:")