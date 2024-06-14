import requests

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
API_KEY = 'YOUR_API_KEY'
BASE_URL = 'https://www.alphavantage.co/query'

def get_stock_price(ticker):
    """Fetch the real-time stock price for the given ticker using Alpha Vantage API."""
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': ticker,
        'interval': '1min',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    try:
        latest_time = max(data['Time Series (1min)'])
        return float(data['Time Series (1min)'][latest_time]['1. open'])
    except KeyError:
        print(f"Error fetching data for {ticker}. Please check the ticker symbol or try again later.")
        return None

class StockPortfolio:
    def __init__(self):
        self.portfolio = {}

    def add_stock(self, ticker, shares):
        price = get_stock_price(ticker)
        if price is not None:
            if ticker in self.portfolio:
                self.portfolio[ticker]['shares'] += shares
            else:
                self.portfolio[ticker] = {
                    'shares': shares,
                    'price': price
                }
            print(f"Added {shares} shares of {ticker} to the portfolio at ${price} each.")

    def remove_stock(self, ticker, shares):
        if ticker in self.portfolio:
            if self.portfolio[ticker]['shares'] > shares:
                self.portfolio[ticker]['shares'] -= shares
                print(f"Removed {shares} shares of {ticker} from the portfolio.")
            elif self.portfolio[ticker]['shares'] == shares:
                del self.portfolio[ticker]
                print(f"Removed all shares of {ticker} from the portfolio.")
            else:
                print("You don't have that many shares to remove.")
        else:
            print(f"{ticker} is not in the portfolio.")

    def update_prices(self):
        for ticker in self.portfolio:
            price = get_stock_price(ticker)
            if price is not None:
                self.portfolio[ticker]['price'] = price

    def display_portfolio(self):
        self.update_prices()
        total_value = 0.0
        print("\nCurrent Portfolio:")
        for ticker, data in self.portfolio.items():
            value = data['shares'] * data['price']
            total_value += value
            print(f"{ticker}: {data['shares']} shares at ${data['price']} each, Total Value: ${value:.2f}")
        print(f"Total Portfolio Value: ${total_value:.2f}\n")

def main():
    portfolio = StockPortfolio()
    while True:
        print("Options: add, remove, view, exit")
        choice = input("What would you like to do? ").lower()
        if choice == 'add':
            ticker = input("Enter the stock ticker symbol: ").upper()
            shares = int(input("Enter the number of shares: "))
            portfolio.add_stock(ticker, shares)
        elif choice == 'remove':
            ticker = input("Enter the stock ticker symbol: ").upper()
            shares = int(input("Enter the number of shares: "))
            portfolio.remove_stock(ticker, shares)
        elif choice == 'view':
            portfolio.display_portfolio()
        elif choice == 'exit':
            print("Exiting the portfolio tracker.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
