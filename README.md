# Stock Market Tracker with Technical Indicators

A real-time stock market tracking application built with Streamlit that provides technical analysis indicators and interactive charts.

## Features

- Real-time stock data fetching using yfinance
- Multiple stock tracking with parallel processing
- Technical indicators including:
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - Relative Strength Index (RSI)
- Interactive charts using Plotly
- Stock ticker lookup functionality
- Dark-themed visualization

## Prerequisites

Make sure you have Python 3.7+ installed on your system. The following Python packages are required:

```bash
streamlit
yfinance
pandas
ta
plotly
concurrent.futures
```

## Installation

1. Clone this repository or download the source code
2. Install the required packages:
```bash
pip install streamlit yfinance pandas ta plotly
```
3. Place the NYSE stock data file (`nyse.csv`) in the `data` directory

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. The application has two main pages:
   - **Stock Tracker**: Enter stock tickers to view real-time data and technical indicators
   - **Stock Tickers**: Browse the complete list of NYSE stocks and their company names

## Data Visualization

The application provides three types of charts for each stock:
1. Price chart with SMA and EMA indicators
2. Volume bar chart
3. RSI indicator with overbought/oversold levels

## File Structure

```
├── app                   
│   └── stocks.py         # Main application file
├── data/
│   └── nyse.csv          # NYSE stock data
├── notebooks/
│   └── Stocks.ipynb      # NYSE stock data
└── README.md             # This file
```

## Error Handling

- The application includes retry mechanisms for failed API calls
- Invalid tickers are gracefully handled
- Missing data file errors are properly reported to the user

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.
