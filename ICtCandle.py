import pandas as pd
import mplfinance as mpf
import requests
import seaborn as sb
import matplotlib.pyplot as plt

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
    candles_to_check = candles[:90][::-1] 
    average = []

    for i in range(0, 21):  
        t = i + 5  
        if t > len(candles_to_check):
            break
        current_average = sum(float(candle['close']) for candle in candles_to_check[i:t]) / (t - i)
        average.append((current_average))
        #print(f"Moving Average {i} to {t}: {current_average}")
    return average
         
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
    
    candles = data["values"]
    candles_to_FVG = candles[:90][::-1]
    boolean = IsBerishOrBullish(data)
    if boolean==True:
        t =0
            
        for i in range(len(candles_to_FVG)//3):
            if (float(candles_to_FVG[t]['high'])<float(candles_to_FVG[t+2]["low"] )):
                 fvg_zones.append(t)
                 fvg_Place.append((float(candles_to_FVG[t]['high']),float(candles_to_FVG[t+2]["low"] )))
                 #print(f"Bullish fvg found on the range { float(candles_to_FVG[t]['high'])} to {float(candles_to_FVG[t+2]['low'])} on the date { candles_to_FVG[t+2]['datetime']}")
                 t+=3
            else :
                 t+=3
    if boolean==False:
        t =0
            
        for i in range(len(candles_to_FVG)//3):
            if (float(candles_to_FVG[t]['low'])>float(candles_to_FVG[t+2]["high"] )):
                 fvg_zones.append(t)
                 fvg_Place.append((float(candles_to_FVG[t]['low']),float(candles_to_FVG[t+2]["high"] )))
                 #print(f"Bearish fvg found on the range { float(candles_to_FVG[t]['low'])} to {float(candles_to_FVG[t+2]['high'])} on the date { candles_to_FVG[t+2]['datetime']}")
                 t+=3
            else :
                 t+=3
    testedFvgs = IsFVGTested(candles_to_FVG,fvg_zones,boolean)
    return (fvg_Place,testedFvgs)

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


 
(fvg_zones,testedfvgs) = FVG(data)
fig, axlist = mpf.plot(
        df,
        type='candle',
        style='charles',
        title='FVG Zones',
        volume=False,
        returnfig=True
)
ax = axlist[0]
for low , high in fvg_zones:
     if (low,high) in testedfvgs:
          color = 'green'
          alpha = 0.3
     else:
          color='red'
          alpha= 0.3
     
     ax.axhspan(float(low), float(high), color=color, alpha=alpha)
bos_levels= BreakofStructure(data)
for level, dt in bos_levels:
    ax.axhline(level, linestyle='--', color='blue', alpha=0.7, linewidth=1)
plt.show()
mpf.plot(df, type='candle', style='charles', title="BTC 5min", volume=False,mav=5)

 