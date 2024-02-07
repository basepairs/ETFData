from flask import Flask, jsonify
from functions.alltickers import get_all_etfs
from functions.shareprice import get_stock_info
from functions.overlap import calculate_overlap_percentage, calculate_overlap_tickers
from flask_cors import CORS
from collections import defaultdict


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/all_etfs', methods=['GET'])
def get_all_etfs_endpoint():
    # Call the function to get all ETFs
    all_etfs_df = get_all_etfs()

    # Group tickers by provider
    tickers_by_provider = all_etfs_df.groupby('Provider')['ticker'].apply(list).to_dict()

    # Convert dictionary to JSON and return
    return jsonify(tickers_by_provider)

@app.route('/overlap_percentage/<ticker1>/<ticker2>', methods=['GET'])
def calculate_overlap_percentage_endpoint(ticker1, ticker2):
    overlap_percentage = calculate_overlap_percentage(ticker1, ticker2)  # Fix this line
    return jsonify({'overlap_percentage': overlap_percentage})

@app.route('/overlap_tickers/<ticker1>/<ticker2>', methods=['GET'])
def calculate_overlap_tickers_endpoint(ticker1, ticker2):
    overlap_tickers = calculate_overlap_tickers(ticker1, ticker2)
    formatted_json = overlap_tickers.to_dict(orient='records')
    return jsonify(formatted_json)

# Endpoint to get stock info
@app.route('/stock_info/<ticker>', methods=['GET'])
def get_stock_info_endpoint(ticker):
    stock_info = get_stock_info(ticker)
    if stock_info:
        return jsonify(stock_info)
    else:
        return jsonify({'error': 'Failed to retrieve information for ticker: {}'.format(ticker)}), 404

# Existing end

if __name__ == '__main__':
    app.run(debug=True, port=2005)