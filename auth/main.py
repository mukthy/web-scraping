from fastapi import FastAPI, Depends
from fastapi import Response
import os
import json
import random
import string
import sys
from fastapi.security.api_key import APIKey
import auth

app = FastAPI()


@app.get("/")
def read_root():
    return {"Details": "Welcome to All in ONE API"}


''' Steam Games API '''


# Steam Games List API to get list of games on offer.

print(sys.path.append('..'))
from steam.steamgames import get_list_of_games
from steam.steamgames import scrapy_runner


@app.get("/games_list/")
async def games_list(start: int, count: int, region: str, api_key: APIKey = Depends(auth.get_api_key)):
    games_lists, boolean, total_count = get_list_of_games.games_with_offers(start, count, region)
    # print(games_lists, boolean, total_count)
    return {
        "games_list": games_lists,
        "possible_has_more": boolean,
        "total_games": total_count
    }


# Steam Game DATA such as price and discount from the Steam, using the AppID.


@app.get("/games_data/")
async def games_data(app_id, api_key: APIKey = Depends(auth.get_api_key)):
    if app_id.isdigit():

        print(type(app_id))
        len_of_chars = 8
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=len_of_chars))

        full_name = '/tmp/' + filename + '.json'
        print(full_name)

        # if os.path.exists(f"{path}/{filename}.js"):
        #     os.remove(f"{path}/games_data.js")

        scrapy_runner.steam_games_data(app_id, full_name)
        f = open(f"{full_name}")
        print(f)
        d = json.load(f)
        json_str = json.dumps(d[0], indent=4, sort_keys=True, default=str)
        print(json_str)
        os.remove(f"{full_name}")
        return Response(json_str, media_type='application/json')

    else:

        print(type(app_id))
        json_str = json.dumps({
                                  "Error": f"AppID you entered is '{app_id}' and it is incorrect or not an Integer as in Digits (Ex: 123456), Please enter the correct APP_ID and try agein. Also refer to the API Documentation for more details."})
        return Response(json_str, media_type='application/json')


''' AMAZON REVIEWS API '''


@app.get("/amazonreviews/")
async def amazon_reviews(asin: str, domain: str, pageNum: int, api_key: APIKey = Depends(auth.get_api_key)):


    len_of_chars = 8
    filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=len_of_chars))

    full_name = '/tmp/' + filename + '.json'
    print(full_name)

    scrapy_runner.amazon_reviews_starter(asin, domain, pageNum, full_name)
    f = open(f"{full_name}")
    print(f)
    d = json.load(f)
    json_str = json.dumps(d[0], indent=4, sort_keys=True, default=str)
    print(json_str)
    os.remove(f"{full_name}")
    return Response(json_str, media_type='application/json')


''' BESTBUY PRODUCT API '''


@app.get("/bestbuy/")
async def bestbuy_products(page: int, keyword: str, api_key: APIKey = Depends(auth.get_api_key)):

    len_of_chars = 8
    filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=len_of_chars))

    full_name = '/tmp/' + filename + '.json'
    print(full_name)

    scrapy_runner.bestbuy_data(page, keyword, full_name)
    f = open(f"{full_name}")
    print("Printing the file")
    print(f)
    d = json.load(f)
    json_str = json.dumps(d, indent=4, sort_keys=True, default=str)
    print(json_str)
    os.remove(f"{full_name}")
    return Response(json_str, media_type='application/json')


sys.path.append('..')
from finance_data_mining.grow_in_stocks import grow_in
from finance_data_mining.yahoo_finance_news import news

''' Finance Data Mining API '''


# from finance_data_mining.zerodha_ticker_api import zerodha_ticket_api
#
#
# @app.get("/stock_price/{search_string}")
# def get_data(search_string: str):
#     data = zerodha_ticket_api.get_data(search_string)
#     return data

# Getting the live Stock Prices from GrowInStocks using the Ticker Symbol.


@app.get("/stock_price/")
async def games_list(symbol: str, api_key: APIKey = Depends(auth.get_api_key)):
    data = grow_in.grow_in_get_data(symbol)
    # print(games_lists, boolean, total_count)
    return data


# Getting the latest news from Yahoo Finance, using the ticker or symbol.

@app.get("/market_india/news/")
async def market_news_india(symbol: str, api_key: APIKey = Depends(auth.get_api_key)):
    data = news.yahoo_finance_news_india(symbol)
    return data


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=8080)