import requests
import pprint
import json
from bs4 import BeautifulSoup
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
api_url = os.getenv('API_URL')
bse_api_url = os.getenv('BSE_API_URL')


def grow_in_get_data(search_string):
    url = f"{api_url}/{search_string}"

    payload = {}
    headers = {

        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/108.0.0.0 Safari/537.36 '
    }

    # response = requests.request("GET", url, headers=headers, data=payload, proxies=proxies, verify=False)
    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:

        data = json.loads(response.text)

        pprint.pprint(data)

        symbol = data['symbol']
        open = data['open']
        day_high = data['high']
        day_low = data['low']
        previous_close = data['close']
        last_trading_price = data['ltp']
        volume = data['volume']
        lowPriceRange = data['lowPriceRange']
        highPriceRange = data['highPriceRange']
        day_change = data['dayChange']
        day_change_percent = data['dayChangePerc']
        totalBuyQty = data['totalBuyQty']
        totalSellQty = data['totalSellQty']
        lastTradeTime = data['lastTradeTime']

        last_trading_time = datetime.datetime.fromtimestamp(lastTradeTime).strftime('%Y-%m-%d %H:%M:%S')

        data = {
            "symbol": symbol,
            "open": open,
            "day_high": day_high,
            "day_low": day_low,
            "previous_close": previous_close,
            "last_trading_price": last_trading_price,
            "lowPriceRange": lowPriceRange,
            "highPriceRange": highPriceRange,
            "volume": volume,
            "day_change": day_change,
            "day_change_percent": day_change_percent,
            "totalBuyQty": totalBuyQty,
            "totalSellQty": totalSellQty,
            # "lastTradeTime": last_trading_time
        }

        pprint.pprint(data)

    else:
        bse_url = f"{bse_api_url}{search_string}&flag=nw"

        bse_payload = {}
        bse_headers = {

            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/108.0.0.0 Safari/537.36 '
        }

        response = requests.request("GET", bse_url, headers=bse_headers, data=bse_payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        symbol_number = soup.find_all("span")[0].get_text()

        # symbol_number = soup.getText()
        # symbol_number = symbol_number.replace(' ', '-')
        symbol_number = symbol_number.replace('\xa0', '-')
        symbol = symbol_number.split('-')[0]
        scrip_id = symbol_number.split('-')[-1]
        print(scrip_id)
        print(symbol)
        data = {
            "symbol": search_string,
            "Description": 'Entered Symbol is Invalid or Listed on BSE with Scrip ID',
            "BSE Data": symbol_number,
            "Scrip ID": scrip_id,
            "Suggestion": 'Please Enter the Scrip ID in the search_string'
        }

    return data


# grow_in_get_data("M&M")
