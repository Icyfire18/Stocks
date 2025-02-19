import streamlit as st
import concurrent.futures
import yfinance as yf
import pandas as pd
import ta  
import time
import plotly.express as px
import plotly.graph_objects as go
import io


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.ticker_company_path = "data/nyse.csv"
        self.data = None

    def fetch_stock_data(self, ticker):
        """Fetch real-time stock data along with technical indicators.
        Parameters:
            ticker (str): Stock ticker symbol.
        Returns:
            pd.DataFrame: Stock data with technical indicators. 
        """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="6mo")  # Fetch last 6 months of data

            if data.empty:
                return None

            # Calculate Technical Indicators
            data["SMA_20"] = ta.trend.sma_indicator(data["Close"], window=20)
            data["EMA_20"] = ta.trend.ema_indicator(data["Close"], window=20)
            data["RSI_14"] = ta.momentum.rsi(data["Close"], window=14)

            return data
        except Exception as e:
            return None


    def fetch_multiple_stocks(self, tickers, max_attempts=3):
        """Fetch multiple stocks in parallel using threads.
        Parameters:
            tickers (list): List of stock tickers.
            max_attempts (int): Maximum number of attempts to fetch the data.
        Returns:
            dict: Dictionary containing stock data for each ticker.
        """
        stock_data = {}

        for attempt in range(max_attempts):
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    future_to_ticker = {executor.submit(self.fetch_stock_data, ticker): ticker for ticker in tickers}

                    for future in concurrent.futures.as_completed(future_to_ticker):
                        ticker = future_to_ticker[future]
                        data = future.result()
                        if data is not None:
                            stock_data[ticker] = data
                return stock_data  # Successful attempt
            except Exception as e:
                time.sleep(5)

        return {}

    @st.cache_data
    def load_stock_tickers(_self, _file_path):
        """Load stock tickers and company names from a local CSV file.
        Parameters:
            file_path (str): Path to the CSV file.
        Returns:
            pd.DataFrame: DataFrame containing stock tickers and company names.
        """
        try:
            df = pd.read_csv(_file_path)
            return df[["ACT Symbol", "Company Name"]].rename(columns={"ACT Symbol": "Ticker", "Company Name": "Company"})
        except Exception as e:
            return None

    def app(self):
        # Streamlit App
        st.set_page_config(page_title="Stock Market Tracker", page_icon="📈", layout="wide")

        # Streamlit Sidebar Navigation
        st.sidebar.title("Stock Market Tracker")
        st.sidebar.subheader("📌 Navigation")
        page = st.sidebar.radio("Go to", ["Stock Tracker", "Stock Tickers"])

        # Page 1: Stock Tracker with Technical Indicators & Charts
        if page == "Stock Tracker":
            st.title("📈 Real-Time Stock Market Tracker with Technical Indicators & Charts")

            # Sidebar: Input tickers
            self.ticker = st.text_input("Enter stock tickers (comma-separated)", self.ticker)

            # Convert input string to list
            tickers = [ticker.strip().upper() for ticker in self.ticker.split(",")]

            # Button to fetch data
            if st.button("Fetch Stock Data"):
                st.write("Fetching stock data... 📊")
                stock_data = self.fetch_multiple_stocks(tickers)

                if stock_data:
                    for ticker, data in stock_data.items():
                        # Convert data to CSV for download
                        csv_data = data.to_csv(index=True)
                        csv_buffer = io.StringIO(csv_data)

                        # Create layout with columns: Title & Download Button
                        col1, col2 = st.columns([0.8, 0.2])  # Adjust proportions for spacing
                        
                        with col1:
                            st.subheader(f"📊 {ticker} Stock Data")
                        
                        with col2:
                            st.download_button(
                                label="📥 Download CSV",
                                data=csv_buffer.getvalue(),
                                file_name=f"{ticker}_stock_data.csv",
                                mime="text/csv",
                            )

                        # Expander for charts
                        with st.expander(f"View {ticker} Analysis"):  
                            
                            # Create two columns for charts
                            col1, col2 = st.columns(2)

                            # Stock Price Chart with SMA & EMA
                            with col1:
                                fig = go.Figure()
                                fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode='lines', name='Close Price', line=dict(color='blue')))
                                fig.add_trace(go.Scatter(x=data.index, y=data["SMA_20"], mode='lines', name='SMA 20', line=dict(color='orange')))
                                fig.add_trace(go.Scatter(x=data.index, y=data["EMA_20"], mode='lines', name='EMA 20', line=dict(color='green')))
                                fig.update_layout(title=f"{ticker} Stock Price with SMA & EMA", xaxis_title="Date", yaxis_title="Price (USD)", template="plotly_dark")
                                st.plotly_chart(fig, use_container_width=True)

                            # Volume Bar Chart
                            with col2:
                                fig_vol = px.bar(data, x=data.index, y="Volume", title=f"{ticker} Trading Volume", labels={"Volume": "Volume"}, template="plotly_dark")
                                st.plotly_chart(fig_vol, use_container_width=True)

                            # RSI Chart
                            fig_rsi = go.Figure()
                            fig_rsi.add_trace(go.Scatter(x=data.index, y=data["RSI_14"], mode='lines', name='RSI 14', line=dict(color='purple')))
                            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
                            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
                            fig_rsi.update_layout(title=f"{ticker} RSI Indicator", xaxis_title="Date", yaxis_title="RSI", template="plotly_dark")
                            st.plotly_chart(fig_rsi, use_container_width=True)

                        # Add a divider between different stocks
                        st.divider()

                else:
                    st.warning("No data available for the entered tickers.")


        # Page 2: Stock Tickers with Full Names
        elif page == "Stock Tickers":
            st.title("🔍 Stock Tickers and Company Names")

            st.write("Loading stock tickers from local CSV file...")

            # Load the stock tickers from the local CSV file
            df_tickers = self.load_stock_tickers(self.ticker_company_path)  
            if df_tickers is not None:
                st.dataframe(df_tickers, width=800, hide_index=True)
            else:
                st.error("Failed to load stock ticker data. Please ensure the 'nyse.csv' file is available.")

        st.sidebar.markdown("---")
        st.sidebar.text("©️ 2025 Stock Market Tracker Test")  # Footer


def main():
    stock = Stock("AAPL, MSFT, GOOGL, TSLA")
    stock.app()


if __name__ == "__main__":
    main()