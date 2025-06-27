import pandas as pd
import mplfinance as mpf
import requests
import seaborn as sb

url = "https://api.twelvedata.com/time_series?symbol=BTC&interval=5min&apikey=b1f81ac90e5d4297bc5a4e3704a79c31&start_date=2025-03-24"
response = requests.get(url)
data = response.json()

def IsSlopingUp(data):
    counter = 0
    Average = MovingAverage(data)
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
    candles_to_check = candles[:39][::-1] 
    average = []

    for i in range(0, 21):  
        t = i + 5  
        if t > len(candles_to_check):
            break
        current_average = sum(float(candle['close']) for candle in candles_to_check[i:t]) / (t - i)
        average.append(current_average)
        #print(f"Moving Average {i} to {t}: {current_average}")
    return average
     
     
def BreakofStructure(data):
    boolean = IsBerishOrBullish(data)        
    if (boolean == True):

        candles = data["values"]
        candles_to_check = candles[:20][::-1]        
        max = float('-inf')                   
        for i in range(len(candles_to_check)-1) :
                
                 if (candles_to_check[i]["high"]>candles_to_check[i+1]["high"]):
                     current_High = float(candles_to_check[i]["high"])
                     if (  current_High > max):
                         max = current_High
                         print(f"Bos was Broken :{current_High} on date {candles_to_check[i]['datetime']}" )
    else:
            candles = data["values"]
            candles_to_check = candles[:20][::-1]
            max = float('inf')

            for i in range(len(candles_to_check)-1):
                
                if (candles_to_check[i]["low"]<candles_to_check[i+1]["low"]):
                      current_Low = float(candles_to_check[i]["low"])
                      if (  current_Low < max):
                         max = current_Low
                         print(f"Bos was Broken : {current_Low} on date {candles_to_check[i]['datetime']}" )
def FVG(data):
    fvg_zones = []
    
    candles = data["values"]
    candles_to_FVG = candles[:21][::-1]
    boolean = IsBerishOrBullish(data)
    if boolean==True:
        t =0
            
        for i in range(len(candles_to_FVG)//3):
            if (float(candles_to_FVG[t]['high'])<float(candles_to_FVG[t+2]["low"] )):
                 fvg_zones.append((float(candles_to_FVG[t]['high']),float(candles_to_FVG[t+2]["low"])))
                 print(f"fvg found on the range { float(candles_to_FVG[t]['high'])} to {float(candles_to_FVG[t+2]['low'])} on the date { candles_to_FVG[t+2]['datetime']}")
                 t+=3
            else :
                 t+=3
    if boolean==False:
        t =0
            
        for i in range(len(candles_to_FVG)//3):
            if (float(candles_to_FVG[t]['low'])>float(candles_to_FVG[t+2]["high"] )):
                 fvg_zones.append((float(candles_to_FVG[t]['low']),float(candles_to_FVG[t+2]["high"])))
                 print(f"fvg found on the range { float(candles_to_FVG[t]['low'])} to {float(candles_to_FVG[t+2]['high'])} on the date { candles_to_FVG[t+2]['datetime']}")
                 t+=3
            else :
                 t+=3
                 




def IsBerishOrBullish(data):
    candles = data["values"]
    candles_to_check = candles[:20][::-1]
   
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
       else :
         print("its jagged and not clear to Know if its Bullish Or Bearish but its quite Positive ! ")
    elif(counter > 0):
         return True
    elif(counter < 0 ):
        return False



 
 

    



BreakofStructure(data)
FVG(data)
print(len(MovingAverage(data)))
 