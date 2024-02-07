import providers.vanguard
import providers.ishares
import providers.ssga

def select_etf_provider():
    while True:
        provider = input("Enter the ETF provider (Vanguard, iShares, or SSGA): ").strip().lower()
        if provider in ['vanguard', 'ishares', 'ssga']:
            return provider
        else:
            print("Invalid input. Please enter either Vanguard, iShares, or SSGA.")

def main():
    #this code is unused
    provider = select_etf_provider()

    if provider == 'vanguard':
        # Get Vanguard ETF details
        vanguard_etf_details = vanguard.get_fund_details()
        print("Vanguard ETFs:")
        print(vanguard_etf_details)
        
        # Prompt user to select an ETF
        selected_etf = input("Enter the number of the ETF: ").strip()
        
        # Get holding details for the selected Vanguard ETF
        holding_details = vanguard.get_holdings_vanguard(selected_etf)
        print("Holding Details:")
        print(holding_details)
    
    elif provider == 'ishares':
        # Get iShares ETF details
        ishares_etf_details = ishares.get_ishares_data()
        print("iShares ETFs:")
        print(ishares_etf_details)
        
        # Prompt user to select an ETF
        selected_etf = input("Enter the number of the ETF: ").strip()
        
        # Get holding details for the selected iShares ETF
        holding_details = ishares.get_holdings_ishares(selected_etf)
        print("Holding Details:")
        print(holding_details)

    elif provider == 'ssga':
        # Get SSGA ETF details
        ssga_etf_details = ssga.get_fund_details()
        print("SSGA ETFs:")
        print(ssga_etf_details)
        
        # Prompt user to select an ETF
        selected_etf = input("Enter the ticker of the ETF: ").strip()
        
        # Get holding details for the selected SSGA ETF
        holding_details = ssga.get_holdings_ssga(selected_etf)
        print("Holding Details:")
        print(holding_details)

if __name__ == "__main__":
    main()

