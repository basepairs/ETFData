import pandas as pd

# Import functions from each provider's module
from providers.vanguard import get_fund_details as vanguard_fund_details
from providers.ishares import get_ishares_data as ishares_fund_details
from providers.ssga import get_fund_details as ssga_fund_details

def get_all_etfs():
    # Get ETF details from Vanguard
    vanguard_df = vanguard_fund_details()
    vanguard_df['Provider'] = 'Vanguard'

    # Get ETF details from iShares
    ishares_df = ishares_fund_details()
    ishares_df['Provider'] = 'iShares'

    # Get ETF details from SSGA
    ssga_df = ssga_fund_details()
    ssga_df['Provider'] = 'SSGA'
    ssga_df = ssga_df[['fundName', 'ticker', 'Provider']]

    # Combine dataframes
    all_etfs_df = pd.concat([vanguard_df, ishares_df, ssga_df], ignore_index=True)

    # Drop the 'fundId' column if it exists
    if 'fundId' in all_etfs_df.columns:
        all_etfs_df.drop(columns=['fundId'], inplace=True)

    return all_etfs_df

