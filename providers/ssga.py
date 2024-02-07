import requests
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO

# Define a dictionary to store cached results
cache = {}

def get_fund_details():
    # Check if data is already cached
    if 'fund_details' in cache:
        return cache['fund_details']
    
    url = "https://www.ssga.com/bin/v1/ssmp/fund/fundfinder?country=us&language=en&role=intermediary&product=etfs&ui=fund-finder"
    response = requests.get(url)
    data = response.json()

    # Extract relevant information from the JSON response for ETFs only
    fund_data = []
    for fund in data['data']['funds']['etfs']['datas']:
        daily_holdings_url = None
        for doc in fund.get('documentPdf', []):
            for doc_info in doc.get('docs', []):
                if doc_info['name'] == 'Daily Holdings':
                    daily_holdings_url = doc_info['path']
                    break
        fund_data.append({
            'fundName': fund['fundName'],
            'ticker': fund['fundTicker'],
            'dailyHoldingsURL': daily_holdings_url
        })

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(fund_data)

    # Cache the data
    cache['fund_details'] = df

    return df


def get_holdings_ssga(ticker):
    # Check if data is already cached
    if ticker in cache:
        return cache[ticker]

    # Get the daily holdings URL for the given ticker
    df_fund_details = get_fund_details()
    url = df_fund_details[df_fund_details['ticker'] == ticker]['dailyHoldingsURL'].iloc[0]

    # Construct the full URL
    full_url = f"https://www.ssga.com{url}"
    
    # Download the XLSX file
    response = requests.get(full_url)
    
    # Load the XLSX file into a DataFrame
    df = pd.read_excel(BytesIO(response.content), header=None, skiprows=5, names=['Name', 'ticker', 'FIGI', 'Coupon', 'Weight', 'Maturity', 'Par Value', 'Market Value'])
        
    # Drop rows where "Name" is NaN
    df = df.dropna()

    # Cache the data
    cache[ticker] = df
    
    return df

# Example usage:
#df_holdings = get_holding_details_from_ticker('SPY')
#print(df_holdings)