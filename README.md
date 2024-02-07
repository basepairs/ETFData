# ETF-Data

Scraping Data on ETFs

The goal of this project is to easily compile the holdings of any ETF from a major ETF provider (iShares/Vanguard/State Street/Invesco/etc) to identify overlap in ETF holdings.

## Overview

This project provides a collection of scripts and a Flask web service to retrieve and compile ETF details from various providers. The main components of the project include:

- **alltickers.py:** Script to compile ETF details from iShares, Vanguard, and SSGA.
- **app.py:** Flask application serving as a web service to access ETF details via RESTful API endpoints.
- **ishares.py:** Module to retrieve ETF data from iShares.
- **ssga.py:** Module to retrieve ETF data from State Street Global Advisors.
- **vanguard.py:** Module to retrieve ETF data from Vanguard.
- **main.py:** Entry point for the application, containing the main logic and API routes.
- **getetfs.py:** Get a list of all ETFs indexed and their provider.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
