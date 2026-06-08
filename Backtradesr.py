import pandas as pd
import mplfinance as mpf
import requests
import seaborn as sb
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go 
import mplfinance as mpf
import backtrader as bt


url = "https://api.twelvedata.com/time_series?symbol=AAPL&interval=5min&outputsize=5000&apikey=b1f81ac90e5d4297bc5a4e3704a79c31&format=JSON"
#url = "https://api.twelvedata.com/time_series?symbol=BTC&interval=5min&apikey=b1f81ac90e5d4297bc5a4e3704a79c31&start_date=2025-03-24"
response = requests.get(url)
data = response.json()
copy_data = response.json()
candles = data["values"]

df = pd.DataFrame(candles)
df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime' , inplace=True)
df = df.sort_index()
for col in ['open','high','low','close','volume']:
     df[col] = df[col].astype(float)



class youtubeStrategy(bt.Strategy):
    params =(
        ('fast_ema_period',9),
        ('slow_ema_period',21)
    )
    def __init__(self):
        
        self.fast_ema=  bt.indicators.ExponentialMovingAverage(self.data.close , period=self.params.fast_ema_period)
        self.slow_ema=  bt.indicators.ExponentialMovingAverage(self.data.close , period=self.params.slow_ema_period)
        self.crossover= bt.indicators.CrossOver(self.fast_ema,self.slow_ema)
    def next(self):
        if self.crossover >0:
            if not self.position:
                    self.buy()
        if self.crossover <0 :
            if self.position:
                self.sell()



class Strategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

    def __init__(self):
        self.atr = bt.indicators.AverageTrueRange(self.data, period=14)
        self.Rsi=bt.indicators.RSI_SMA(self.data)
        self.macd=bt.indicators.MACD(self.data)
        ema1 = bt.indicators.ExponentialMovingAverage()
        sma1 = bt.indicators.MovingAverageSimple(self.data)
        
        close_over_sma = self.data.close > sma1
        close_over_ema = self.data.close > ema1
        sma_ema_diff = sma1 - ema1
        self.order=None
        self.holding_time=0
        self.highest_price = 0.0
        self.highest_close = 0.0

        self.buy_sig = bt.And(close_over_sma, close_over_ema, sma_ema_diff > 0)
         
    def next(self): 

         
        untested=[]
        isNear=False
        NearLiquidity= False
        NearLiquidityDown=False
        self.highest_price = max(self.highest_price, self.datas[0].close[0])


        if len(self)<20:
            return 
        trend = self.isBearishorBullish()
        fvg_zones, _, _, testedFvgs = self.FVG()
        bos = self.Break_of_Structure()
        liquidity_tolerance =0.0012
        for (high,low ) in fvg_zones:
            if (high,low) not in  testedFvgs and (high,low) not in untested:
                untested.append((high,low))
        for (high,low) in untested:
            expanded_low= low*(1-liquidity_tolerance)
            expanded_high=high*(1+liquidity_tolerance)

                    
            if expanded_low<= self.datas[0].close[0] <= expanded_high:
                isNear=True
                break
        Volume= self.VolumeCheck()
        (swinghigh,swinglow) = self.LiquidtyCheck()
        LiquidityUp= sorted([level for level in swinghigh if level > self.datas[0].close[0]],  reverse=True)
        LiquidityDown= sorted([level for level in swinglow if level < self.datas[0].close[0]])
        if LiquidityUp:
            nearest_up=LiquidityUp[0]
            NearLiquidity = abs(self.datas[0].close[0] - nearest_up)/nearest_up < liquidity_tolerance
        else:
            NearLiquidity= False

        if LiquidityDown:
            nearest_Down=LiquidityDown[0]
            NearLiquidityDown = abs(self.datas[0].close[0] - nearest_Down)/nearest_Down < liquidity_tolerance
        else:
            NearLiquidityDown= False

         

        current_close=self.datas[0].close[0]
        if self.order:
            return
        if not self.position :
             
            if not trend and NearLiquidityDown and Volume and  self.buy_sig :
                if self.datas[0].close[0] > self.datas[0].open[0] and self.Rsi[0]<45 and self.datas[0].close[-1] > self.datas[0].open[-1] and self.datas[0].close[-2] > self.datas[0].open[-2]:
                    if self.datas[0].close[0]>max (self.datas[0].close[-1],self.datas[0].close[-2]) and self.Rsi[0]>self.Rsi[-1]>self.Rsi[-2]:
                        if self.datas[0].low[0] < self.datas[0].low[-1] and self.datas[0].close[0] > self.datas[0].open[0] * 1.002:


 
                            self.order= self.buy()
                            self.log(f"the Volume is {Volume} |  Trend is {trend} Nearliquidity {NearLiquidityDown}")
            elif trend and Volume:
                if 50<self.Rsi[0]<65:
                    if self.data.close[0] >   max(self.datas[0].high[-1], self.datas[0].high[-2]):
                        if not NearLiquidity and self.datas[0].close[0] > self.datas[0].open[0] and self.datas[0].close[-1] > self.datas[0].open[-1] and self.datas[0].close[-2] > self.datas[0].open[-2]:
                            self.log(f"the Volume is {Volume} | isNear is {isNear} Trend is {trend} Nearliquidity {NearLiquidity}")
                            self.order= self.buy()



   
        if self.position:
            self.highest_close = max(self.highest_close, self.datas[0].close[0])
            raw_target = 2 * self.atr[0] / self.datas[0].close[0]
            target_profit_pct = 0.0045 
            current_time = self.datas[0].datetime.time(0) 
            market_close = datetime.time(15,50)
            
            self.highest_price = max(self.highest_price ,current_close)
            trailing_stop = self.buyprice * (1 - 2 * self.atr[0] / self.data.close[0])
            Commision =  (self.datas[0].close[0]-self.buyprice -(self.datas[0].close[0] *0.01))>0  
            stoploss= 0.01
            
         
             
             
            if trend and Volume and NearLiquidity and self.Rsi[0] > 70:
                #self.log(f"the Volume is {Volume} | the RSI is {self.Rsi[0]} Trend is {trend} Nearliquidity {NearLiquidity}")
                if self.datas[0].close[0]<self.datas[0].close[-1] and self.datas[0].close[0]> self.buyprice * (1 + target_profit_pct):
                    self.order = self.sell()
            elif   self.datas[0].close[0]> self.buyprice * (1 + target_profit_pct):
                self.order = self.sell()
            elif current_time >= market_close and self.datas[0].close[0] > self.buyprice * (1 + target_profit_pct):
                self.order = self.sell()
            elif self.Rsi[0]>75 and self.datas[0].close[0] > self.buyprice and Commision:
                self.order=self.sell()
            elif self.datas[0].close[0] <= self.buyprice-(self.buyprice*stoploss):
                self.order=self.sell()


                
                

                


            
 







        self.log(f"LiquidityUP {LiquidityUp} and Liquidity {LiquidityDown}")   
        self.log(f"LiquidityUP {NearLiquidity} and Liquidity {NearLiquidityDown}")
        self.log(f"Candle {len(self)} | Date: {self.data.datetime.date(0)} | Close: {self.data.close[0]} | RSI : {self.Rsi[0]} | trend {trend}| Volume {Volume} | Nearliquidity {NearLiquidity}  ")



            

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)
            

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None    

    def notify_trade(self, trade):
        if trade.isclosed:
            print(f"Trade closed. Gross PnL: {trade.pnl}, Net PnL (after commission): {trade.pnlcomm}")

    def LiquidtyCheck(self):
        lookback=20
        swinghighs=[]
        swinglows=[]
        for i in range (-(lookback-1),-1):
            if self.datas[0].high[i-1]<self.datas[0].high[i]>self.datas[0].high[i+1]:
                if self.datas[0].high[i]>self.datas[0].close[0]:
                    swinghighs.append(self.datas[0].high[i])
            if self.datas[0].low[i-1]<self.datas[0].low[i]>self.datas[0].low[i+1]:
                if self.datas[0].low[i]<self.datas[0].close[0]:
                    swinglows.append(self.datas[0].low[i])
        return swinghighs,swinglows
    def VolumeCheck(self):
        volume = 0
        if len(self) <10+1:
            return False
        for i in range (-10,-1):
            volume += float(self.datas[0].volume[i])
        average_volume=volume/15
        if float(self.datas[0].volume[0]) > average_volume:
            return True
        return False    

    def Break_of_Structure(self):
        bos=[]
        lookback=20
        boolean=self.isBearishorBullish()
        if boolean == True:
            max = float("-inf")
            for i in range(-lookback,-1):
                previous_candle=self.datas[0].high[i]
                current_candle=self.datas[0].high[i+1]
                if (float(previous_candle)> float(current_candle)):
                    current_high= previous_candle
                    max = current_high
                    if (float(max),self.datas[0].datetime.date(i)) not in bos :

                        bos.append((float(max),self.datas[0].datetime.date(i)))
        else:
            max = float("inf")
            for i in range(-lookback,-1):
                previous_candle=self.datas[0].low[i]
                current_candle=self.datas[0].low[i+1]
                if (float(previous_candle)< float(current_candle)):
                    current_low= previous_candle
                    max = current_low
                    if ((float(max),self.datas[0].datetime.date(i))) not in bos :
                        bos.append((float(max),self.datas[0].datetime.date(i)))
        return bos
    def FVG(self):
        is_bullish = self.isBearishorBullish()
        fvg_zones = []
        fvg_places = []
        fvg_datetime = []

        
        lookback = 20
        if len(self)<lookback:
            return
        

        for t in range(-lookback, -3):  
            try:
                if is_bullish ==True:
                    high1 = self.datas[0].high[t]
                    low3 = self.datas[0].low[t + 2]
                    if float(high1) < float(low3):  # Bullish FVG
                        fvg_zones.append((float(high1), float(low3)))
                        fvg_places.append(t)
                        fvg_datetime.append(self.datas[0].datetime.date(t))
                elif is_bullish == False:
                    low1 = self.datas[0].low[t]
                    high3 = self.datas[0].high[t + 2]
                    if float(low1) > float(high3):  # Bearish FVG
                        fvg_zones.append((float(high3), float(low1)))
                        fvg_places.append(t)
                        fvg_datetime.append(self.datas[0].datetime.date(t))
            except IndexError:
                continue

        testedFvgs = self.IsFVGTested(fvg_places, is_bullish)
        return fvg_zones, fvg_places, fvg_datetime, testedFvgs
    def IsFVGTested(self, fvg_places, is_bullish):
        tested_fvg = []
        data_len = len(self.datas[0])
        lookback=20
        

        for t in fvg_places:
            if t + 3 >= lookback:
                continue

            try:
                if is_bullish:
                    fvg_low = float(self.datas[0].low[t + 2])
                    fvg_high = float(self.datas[0].high[t])
                    for i in range(t + 3, -lookback,-1):
                        candle_low = float(self.datas[0].low[i])
                        candle_high = float(self.datas[0].high[i])
                        if candle_low <= fvg_low <= candle_high:
                            tested_fvg.append((fvg_low, fvg_high))
                            break
                else:
                    fvg_low = float(self.datas[0].high[t + 2])
                    fvg_high = float(self.datas[0].low[t])
                    for i in range(t + 3, -lookback,-1):
                        candle_low = float(self.datas[0].low[i])
                        candle_high = float(self.datas[0].high[i])
                        if candle_low <= fvg_high and candle_high >= fvg_low:
                            tested_fvg.append((fvg_low, fvg_high))
                            break
            except IndexError:
                continue

        return tested_fvg
    def isBearishorBullish(self):
        up_count = 0
        down_count = 0
        lookback=20
        if len(self.datas[0]) < lookback + 1:
            return
         
        for i in range(-lookback, -1):
            prev_close = self.datas[0].close[i]
            
            curr_close = self.datas[0].close[i + 1]
            
            if float(curr_close) > float(prev_close):
                
                up_count += 1
            else:
                down_count += 1

        if up_count > down_count:
            
            return True
        elif down_count > up_count:
            
            return False
        else:
            return None
        

        
data = bt.feeds.PandasData(dataname=df,
                           high=1,
                           low=2,
                           open=0,
                           close=3,
                           volume=4,
                           openinterest=-1
                           )
 
# -------------- BACKTEST ----------------
cerebro = bt.Cerebro()
cerebro.addstrategy(Strategy)
cerebro.adddata(data)
cerebro.broker.set_cash(10000)
cerebro.addsizer(bt.sizers.FixedSize, stake=1)

cerebro.broker.setcommission(commission=0.001)
print(f"Starting Portfolio Value: {cerebro.broker.getvalue()}")
cerebro.run()
print(f"Final Portfolio Value: {cerebro.broker.getvalue()}")

cerebro.plot(style="candles")