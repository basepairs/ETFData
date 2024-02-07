# Importing functions from the respective modules
from providers.vanguard import get_fund_details, get_holdings_vanguard
from providers.ssga import get_holdings_ssga
from providers.ishares import get_ishares_data, get_holdings_ishares


def find_etfs_by_ticker(ticker):
    # Define a list to store results
    results = []

    # Check Vanguard ETFs
    vanguard_df = get_fund_details()
    for index, row in vanguard_df.iterrows():
        holdings_df = get_holdings_vanguard(row['ticker'])
        if ticker in holdings_df['ticker'].values:
            weight = holdings_df.loc[holdings_df['ticker'] == ticker, 'Weight'].iloc[0]
            results.append({'Provider': 'Vanguard', 'ETF Name': row['fundName'], 'Weight': weight})
    
    # Check SSGA ETFs
    ssga_df = get_fund_details()
    for index, row in ssga_df.iterrows():
        holdings_df = get_holdings_ssga(row['ticker'])
        if ticker in holdings_df['Name'].values:
            weight = holdings_df.loc[holdings_df['Name'] == ticker, 'Weight'].iloc[0]
            results.append({'Provider': 'SSGA', 'ETF Name': row['fundName'], 'Weight': weight})

    # Check iShares ETFs
    ishares_df = get_ishares_data()
    for index, row in ishares_df.iterrows():
        holdings_df = get_holdings_ishares(row['ticker'])
        if ticker in holdings_df['ticker'].values:
            weight = holdings_df.loc[holdings_df['ticker'] == ticker, 'Weight'].iloc[0]
            results.append({'Provider': 'iShares', 'ETF Name': row['fundName'], 'Weight': weight})

    return results

# Example usage:
results = find_etfs_by_ticker('AAPL')
print(results)

