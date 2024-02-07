import requests

def get_stock_info(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?region=US&lang=en-US&includePrePost=false&interval=5m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad response status codes
        data = response.json()
        
        if 'chart' in data and 'result' in data['chart'] and len(data['chart']['result']) > 0:
            result = data['chart']['result'][0]['meta']
            instrument_type = result['instrumentType']
            regular_market_price = result['regularMarketPrice']
            exchange_name = result['exchangeName']
            return {
                'instrumentType': instrument_type,
                'regularMarketPrice': regular_market_price,
                'exchangeName': exchange_name
            }
        else:
            print("No valid data found in response")
            return None
    except requests.exceptions.RequestException as e:
        print("Error occurred while fetching stock info:", e)
        return None

