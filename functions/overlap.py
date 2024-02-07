import pandas as pd
from alltickers import get_all_etfs
from providers.vanguard import get_holdings_vanguard
from providers.ishares import get_holdings_ishares
from providers.ssga import get_holdings_ssga

def calculate_overlap_percentage(ticker1, ticker2):
    # Get all ETFs to determine the provider for each ticker
    all_etfs_df = get_all_etfs()

    # Determine the providers for the given tickers
    provider1 = all_etfs_df.loc[all_etfs_df['ticker'] == ticker1, 'Provider'].iloc[0]
    provider2 = all_etfs_df.loc[all_etfs_df['ticker'] == ticker2, 'Provider'].iloc[0]


    if provider1 is None or provider2 is None:
        return "Invalid ticker(s) provided."

    # Get holding details based on ETF provider and ticker
    if provider1 == 'Vanguard':
        df1 = get_holdings_vanguard(ticker1)
    elif provider1 == 'iShares':
        df1 = get_holdings_ishares(ticker1)
    else:  # provider1 == 'SSGA'
        df1 = get_holdings_ssga(ticker1)

    if provider2 == 'Vanguard':
        df2 = get_holdings_vanguard(ticker2)
    elif provider2 == 'iShares':
        df2 = get_holdings_ishares(ticker2)
    else:  # provider2 == 'SSGA'
        df2 = get_holdings_ssga(ticker2)

    # Rename columns for merging if necessary
    df1.rename(columns={'Weight': 'weight_x'}, inplace=True)
    df2.rename(columns={'Weight': 'weight_y'}, inplace=True)

    # Find overlapping holdings
    overlapping_holdings = pd.merge(df1, df2, how='inner', on=['ticker'])

    if overlapping_holdings.empty:
        return "No overlapping holdings found."

    # Calculate total weights of each ETF
    total_weight_df1 = df1['weight_x'].sum()
    total_weight_df2 = df2['weight_y'].sum()

    # Calculate total overlap percentage
    total_overlap_weight = overlapping_holdings['weight_x'].sum() + overlapping_holdings['weight_y'].sum()
    total_overlap_percentage = total_overlap_weight / (total_weight_df1 + total_weight_df2)

    return total_overlap_percentage


def calculate_overlap_tickers(ticker1, ticker2):
    # Get all ETFs to determine the provider for each ticker
    all_etfs_df = get_all_etfs()

    # Determine the providers for the given tickers
    provider1 = all_etfs_df.loc[all_etfs_df['ticker'] == ticker1, 'Provider'].iloc[0]
    provider2 = all_etfs_df.loc[all_etfs_df['ticker'] == ticker2, 'Provider'].iloc[0]

    if provider1 is None or provider2 is None:
        return pd.DataFrame()  # Return an empty DataFrame if invalid ticker(s) provided

    # Get holding details based on ETF provider and ticker
    if provider1 == 'Vanguard':
        df1 = get_holdings_vanguard(ticker1)
    elif provider1 == 'iShares':
        df1 = get_holdings_ishares(ticker1)
    else:  # provider1 == 'SSGA'
        df1 = get_holdings_ssga(ticker1)

    if provider2 == 'Vanguard':
        df2 = get_holdings_vanguard(ticker2)
    elif provider2 == 'iShares':
        df2 = get_holdings_ishares(ticker2)
    else:  # provider2 == 'SSGA'
        df2 = get_holdings_ssga(ticker2)

    # Check if either DataFrame is empty
    if df1.empty or df2.empty:
        return pd.DataFrame()  # Return an empty DataFrame if no data is retrieved for any ticker

    # Check if 'Weight' column exists in df1
    if 'Weight' not in df1.columns:
        return pd.DataFrame()  # Return an empty DataFrame if 'Weight' column is missing in df1

    # Check if 'Weight' column exists in df2
    if 'Weight' not in df2.columns:
        return pd.DataFrame()  # Return an empty DataFrame if 'Weight' column is missing in df2


    # Rename columns for merging if necessary
    df1.rename(columns={'Weight': 'weight_ETF1'}, inplace=True)
    df2.rename(columns={'Weight': 'weight_ETF2'}, inplace=True)

    # Find overlapping holdings
    overlapping_holdings = pd.merge(df1, df2, how='inner', on=['ticker'])

    if overlapping_holdings.empty:
        return pd.DataFrame()  # Return an empty DataFrame if no overlapping holdings found

    return overlapping_holdings[['ticker', 'weight_ETF1', 'weight_ETF2']]


# Example usage:
#overlap_tickers = calculate_overlap_tickers('VOO', 'SPY')
#print(overlap_tickers)