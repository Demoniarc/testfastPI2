# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:40:41 2020

@author: win10
"""

import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import json
import ccxt
import pickle

app = FastAPI()
pickle_in = open("model_eth.pkl","rb")
classifier_2=pickle.load(pickle_in)

@app.get("/")
def index():
    cex_x = ccxt.binance().fetch_ohlcv('ETH/USDT', '5m')
    open_price = cex_x[499][1]
    prediction = classifier_2.predict([[open_price]])
    data = {
        'open price': open_price,
        'prediction': prediction[0][0]
    }
    # Ajouter l'en-tête Content-Disposition
    headers = {
        "Content-Disposition": "attachment; filename=data.json"
    }
    return JSONResponse(content=data, headers=headers)

        #uvicorn app:app --reload
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
