import pandas as pd
import mplfinance as mpf
import requests
import seaborn as sb
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches

url = "https://api.twelvedata.com/time_series?symbol=BTC&interval=5min&apikey=b1f81ac90e5d4297bc5a4e3704a79c31&start_date=2025-03-24"
response = requests.get(url)
data = response.json()
candles = data["values"][:90][::-1] 

df = pd.DataFrame(candles)
df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime' , inplace=True)
df = df.sort_index()
for col in ['open','high','low','close','volume']:
     df[col] = df[col].astype(float)


def IsSlopingUp(data):
    counter = 0
    Average,_ = MovingAverage(data)
    for i  in range(len(Average)-1):
         if float(Average[i]) > float(Average[i+1]):
                if counter < 0 :
                     counter = 0
                counter +=1
         else:
              if counter >0:
                   counter = 0
              counter -=1
    if counter > 0 :
         return True 
    elif counter < 0:
         return False
    elif counter == 0:
         return None
         
def MovingAverage(data):
    candles = data["values"]
    candles_to_check = candles[:90][::-1] 
    average = []
    count=0

    for i in range(len(candles_to_check) - 5 + 1):  
        t = i + 5  
        if t > len(candles_to_check):
            break
        current_average = sum(float(candle['close']) for candle in candles_to_check[i:t]) / (t - i)
        average.append((current_average))
        #print(f"Moving Average {i} to {t}: {current_average}")
    for i in range(len(average)):
          candle_close = float(candles_to_check[i+4]['close'])
          if candle_close > average[i]:
               if count <0 :
                    count = 0
                    count +=1
               count +=1
          elif candle_close < average[i]:
               if count > 0:
                    count =0
                    count -=1
               count -=1
          
    if count >0:
         return average,True
    elif count <0:
         return average,False
    elif count ==0:
         return average, None
         
         
def BreakofStructure(data):
    bos= []
    boolean = IsBerishOrBullish(data)        
    if (boolean == True):

        candles = data["values"]
        candles_to_check = candles[:90][::-1]        
        max = float('-inf')                   
        for i in range(len(candles_to_check)-1) :
                
                 if (candles_to_check[i]["high"]>candles_to_check[i+1]["high"]):
                     current_High = float(candles_to_check[i]["high"])
                     if (  current_High > max):
                         max = current_High
                         bos.append((float(max),candles_to_check[i]["datetime"]))
    else:
            candles = data["values"]
            candles_to_check = candles[:90][::-1]
            max = float('inf')

            for i in range(len(candles_to_check)-1):
                
                if (candles_to_check[i]["low"]<candles_to_check[i+1]["low"]):
                      current_Low = float(candles_to_check[i]["low"])
                      if (  current_Low < max):
                         max = current_Low
                         bos.append((float(max),candles_to_check[i]["datetime"]))
                         
    return bos

def IsFVGTested(data,fvg_zones,boolean):
     tested_fvg = []
     for t in fvg_zones:
          if boolean == True:               
            fvg_high = data[t+2]['low']
            fvg_low = data[t]['high']
            for Fcandle in data[t+3 :]:
                 if float(fvg_low) >= float(Fcandle['low']) and float(fvg_low) <= float(Fcandle['high']):
                    if(float(fvg_low),float(fvg_high)) not in tested_fvg:

                         #print(f"this Bulish Fvg was tested {fvg_high} : {fvg_low}")          
                         tested_fvg.append((float(fvg_low),float(fvg_high)))

          elif boolean == False:
            fvg_low = data[t+2]['high']
            fvg_high = data[t]['low']    
            for Fcandle in data[t+3 :]:
                 if float(fvg_high) >= float(Fcandle['low']) and float(fvg_low) <= float(Fcandle['high']):
                    if (float(fvg_low),float(fvg_high)) not in tested_fvg:

                         #print(f"this Bearish Fvg was tested {fvg_high} : {fvg_low}")
                         tested_fvg.append((float(fvg_low),float(fvg_high)))
          elif boolean == None:
               break
     return tested_fvg
                    
def FVG(data):
    fvg_zones = []
    fvg_Place=[]
    fvg_dateTime=[]
    candles = data["values"]
    candles_to_FVG = candles[:90][::-1]
    boolean = IsBerishOrBullish(data)
    if boolean==True:
        t =0
            
        for i in range(len(candles_to_FVG)//3):
            if (float(candles_to_FVG[t]['high'])<float(candles_to_FVG[t+2]["low"] )):
                 fvg_Place.append(t)
                 fvg_zones.append((float(candles_to_FVG[t]['high']),float(candles_to_FVG[t+2]["low"] )))
                 fvg_dateTime.append(candles[t]['datetime'])
                 #print(f"Bullish fvg found on the range { float(candles_to_FVG[t]['high'])} to {float(candles_to_FVG[t+2]['low'])} on the date { candles_to_FVG[t+2]['datetime']}")
                 t+=3
            else :
                 t+=3
    if boolean==False:
        t =0
            
        for i in range(len(candles_to_FVG)//3):
            if (float(candles_to_FVG[t]['low'])>float(candles_to_FVG[t+2]["high"] )):
                 fvg_Place.append(t)
                 fvg_zones.append((float(candles_to_FVG[t]['low']),float(candles_to_FVG[t+2]["high"] )))
                 fvg_dateTime.append(candles[t]['datetime'])
                 #print(f"Bearish fvg found on the range { float(candles_to_FVG[t]['low'])} to {float(candles_to_FVG[t+2]['high'])} on the date { candles_to_FVG[t+2]['datetime']}")
                 t+=3
            else :
                 t+=3
    testedFvgs = IsFVGTested(candles_to_FVG,fvg_Place,boolean)
    return (fvg_zones,testedFvgs,fvg_Place,fvg_dateTime)

def IsBerishOrBullish(data):
    candles = data["values"]
    candles_to_check = candles[:90][::-1]
   
    counter = 0
    

    for i in range(len(candles_to_check) -1 ):
        current_candle = candles_to_check[i]
        next_candle = candles_to_check[i+1]
        if (float(current_candle['close']) > float(next_candle['close'])):
            if (counter < 0 ):
                counter = 0
            counter +=1 
            
        else:
             if(counter > 0):
                counter = 0
             counter -= 1   

            
    if (counter == 0):
       if float(candles_to_check[0]['close']) < float(candles_to_check[9]['close']):

                print("its jagged and not clear to Know if its Bullish Or Bearish but its quite negative ! ")
                return None
       else :
         print("its jagged and not clear to Know if its Bullish Or Bearish but its quite Positive ! ")
         return None
    elif(counter > 0):
         return True
    elif(counter < 0 ):
        return False

def ShouldYouBuyorSell(data):
     (fvg_zones,testedFvgs,fvg_Place,fvg_dateTime)=FVG(data)
     IsitBullishOrBearish= IsBerishOrBullish(data)
     Sloping=IsSlopingUp(data)
     Bos=BreakofStructure(data)
     average,boolean=MovingAverage(data)
     margin = 0.01
     untestedFVG = [] 
     isNear= False
     for (high,low ) in fvg_zones : 

        if (low,high) not in testedFvgs:
             untestedFVG.append((high,low))
     for (high,low ) in untestedFVG:

          if low -low*margin <= float(data["values"][0]["close"])<= high - high*margin:
               isNear= True
               return isNear

     if (
        IsitBullishOrBearish is True and
        Sloping is True and
        boolean is True and
        untestedFVG and
        isNear
    ):
        return "BUY"
     elif (
        IsitBullishOrBearish is False and
        Sloping is False and
        boolean is False and
        untestedFVG
    ):
        last_fvg = untestedFVG[-1]
        low, high = last_fvg
        if low > float(data["values"][0]["close"]):
            return "SELL"

    
     return "WAIT"

          


mpf.plot(df,type='candle')
print(ShouldYouBuyorSell(data))

