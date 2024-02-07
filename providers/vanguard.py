import requests
from datetime import datetime, timedelta
import pandas as pd

# Define a dictionary to store cached results
vanguard_cache = {}

def get_fund_details():
    # Check if data is already cached
    if 'fund_details' in vanguard_cache:
        return vanguard_cache['fund_details']

    url = "https://investor.vanguard.com/investment-products/list/funddetail"
    response = requests.get(url)
    data = response.json()

    # Extract relevant information from the JSON response for ETFs only
    fund_data = []
    for entity in data['fund']['entity']:
        if entity['profile']['isETF']:
            fund_data.append({
                'fundId': entity['profile']['fundId'],
                'ticker': entity['profile']['ticker'],
                'fundName': entity['profile']['longName'],
            })

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(fund_data)

    # Cache the data
    vanguard_cache['fund_details'] = df

    return df

def get_holdings_vanguard(ticker, fund_id=None):

    # Check if either fund_id or ticker is provided
    if not fund_id and not ticker:
        raise ValueError("Either 'fund_id' or 'ticker' must be provided.")
    
    if not fund_id:
        # Get the fund ID corresponding to the provided ticker
        df_fund_details = get_fund_details()
        fund_id = df_fund_details[df_fund_details['ticker'] == ticker]['fundId'].iloc[0]

    # Check if data is already cached
    if fund_id in vanguard_cache:
        return vanguard_cache[fund_id]

    # Get current date
    current_date = datetime.now()
    
    # Initialize the DataFrame
    df = pd.DataFrame()
    
    # Loop through the months, starting with the most recent completed month
    while True:
        # Calculate the last day of the current month
        last_day_of_month = current_date.replace(day=1) - timedelta(days=1)
        
        # Construct the API endpoint URL with the last day of the current month
        query_date = last_day_of_month.strftime('%Y-%m-%d')
        url = f"https://eds.ecs.gisp.c1.vanguard.com/eds-eip-distributions-service/holdings/holding-details-history/{fund_id}.json?as-of-date={query_date}"
        
        # Make GET request to the API endpoint
        response = requests.get(url)
        data = response.json()
        
        # Check if response is not empty
        if data:
            # Extract relevant information from the JSON response
            holdings_data = []
            for item in data:
                for holdingDetailItem in item.get("holdingDetailItem", []):
                    holdings_data.append({
                        'ETF Name': holdingDetailItem.get('reportingName', ''),
                        'Name': holdingDetailItem.get('name', ''),
                        'ticker': holdingDetailItem.get('bticker', ''),
                        'Quantity': holdingDetailItem.get('quantity', ''),
                        'Weight': holdingDetailItem.get('mktValPercent', ''),
                        'Market': holdingDetailItem.get('market', ''),
                        'CUSIP': holdingDetailItem.get('CUSIP', ''),
                        'Sales Position': holdingDetailItem.get('salesPosition', ''),
                        'Issue Type Name': holdingDetailItem.get('issueTypeName', ''),
                        'Parent Issue Type Name': holdingDetailItem.get('parentIssueTypeName', ''),
                        'Sector': holdingDetailItem.get('sector', ''),
                        'As of Date': query_date
                    })
            
            # Create a DataFrame from the extracted data
            df = pd.DataFrame(holdings_data)
            
            # Cache the data
            vanguard_cache[fund_id] = df
            
            # Break the loop as we found non-empty response
            break
        
        # Move to the previous month for the next iteration
        current_date = current_date.replace(day=1) - timedelta(days=1)
    
    return df


#print(get_holding_details_latest('VOO'))