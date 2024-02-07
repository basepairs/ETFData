import requests
import pandas as pd
import json

# Define a dictionary to store cached results
cache = {}

def get_ishares_data():
    # Check if data is already cached
    if 'ishares_data' in cache:
        return cache['ishares_data']

    url = "https://www.ishares.com/us/product-screener/product-screener-v3.1.jsn?dcrPath=/templatedata/config/product-screener-v3/data/en/us-ishares/ishares-product-screener-excel-config&disclosureContentDcrPath=/templatedata/content/article/data/en/us-ishares/DEFAULT/product-screener-all-disclaimer"
    response = requests.get(url)
    data = response.json()

    # Extract relevant information from the JSON response
    ishares_data = []
    for fund_id, fund_details in data.items():
        ishares_data.append({
            'fundId': fund_id,
            'fundName': fund_details['fundName'],
            'ticker': fund_details['localExchangeTicker']
        })

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(ishares_data)

    # Cache the data
    cache['ishares_data'] = df

    return df


def get_holdings_ishares(ticker, fund_id=None):
    # Check if data is already cached
    cache_key = ticker if fund_id is None else fund_id
    if cache_key in cache:
        return cache[cache_key]

    # Use the fundID if provided, otherwise retrieve it directly
    if fund_id is None:
        df_ishares = get_ishares_data()
        if ticker not in df_ishares['ticker'].values:
            return pd.DataFrame()  # Return an empty DataFrame if ticker not found
        fund_id = df_ishares[df_ishares['ticker'] == ticker]['fundId'].iloc[0]

    url = f"https://www.ishares.com/us/products/{fund_id}/fund/1467271812596.ajax?tab=all&fileType=json"
    response = requests.get(url)

    # Decode the response content, removing the UTF-8 BOM if present
    content = response.content.decode('utf-8-sig')

    # Load the JSON data from the response content
    data = json.loads(content)

    # Extract relevant information from the JSON response
    holdings_data = []
    for row in data['aaData']:
        holdings_data.append({
            'ticker': row[0],
            'company_name': row[1],
            'sector': row[2],
            'type': row[3],
            'market_value': row[4]['raw'],
            'Weight': row[5]['raw']
        })

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(holdings_data)

    # Cache the data
    cache[cache_key] = df

    return df