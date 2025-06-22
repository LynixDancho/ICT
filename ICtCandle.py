import pandas as pd
import mplfinance as mpf
import requests

def IsBerishOrBullish(data):
    candles = data["values"]
    candles_to_check = candles[:10][::-1]
   
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
        print("Its bullish")
    elif(counter < 0 ):
        print("its bearish")



 
 

    



url = "https://api.twelvedata.com/time_series?symbol=BTC&interval=5min&apikey=b1f81ac90e5d4297bc5a4e3704a79c31&start_date=2025-03-24"


response = requests.get(url)
data = response.json()
IsBerishOrBullish(data)


 