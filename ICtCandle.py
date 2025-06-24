import pandas as pd
import mplfinance as mpf
import requests

url = "https://api.twelvedata.com/time_series?symbol=BTC&interval=5min&apikey=b1f81ac90e5d4297bc5a4e3704a79c31&start_date=2025-03-24"
response = requests.get(url)
data = response.json()

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
                         print(f"Bos was Broken :{current_High}" )
    else:
            candles = data["values"]
            candles_to_check = candles[:20][::-1]
            max = float('inf')

            for i in range(len(candles_to_check)-1):
                
                if (candles_to_check[i]["low"]<candles_to_check[i+1]["low"]):
                      current_Low = float(candles_to_check[i]["low"])
                      if (  current_Low < max):
                         max = current_Low
                         print(f"Bos was Broken : {current_Low}" )


                





def FVG(data):
    print("placeholder")
    candles = data["values"]
    candles_to_FVG = candles[:10][::-1]
    boolean = IsBerishOrBullish(data)




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


 