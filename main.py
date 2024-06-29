import yfinance as yf
import itertools
from collections import defaultdict

def get_exchange_rates():
    currencies = ['USD', 'EUR', 'JPY', 'GBP', 'CHF', 'CAD', 'AUD', 'NZD', 'CNY', 'INR']
    rates = {}
    for base in currencies:
        for quote in currencies:
            if base != quote:
                pair = f"{base}{quote}=X"
                try:
                    data = yf.Ticker(pair).history(period="1d")
                    if not data.empty:
                        rates[f"{base}/{quote}"] = data['Close'].iloc[-1]
                        print(f"Fetched rate for {base}/{quote}: {rates[f'{base}/{quote}']}")
                    else:
                        print(f"No data available for {pair}")
                except Exception as e:
                    print(f"Error fetching data for {pair}: {e}")
    return rates

def calculate_arbitrage(rates, path):
    total_rate = 1
    for i in range(len(path) - 1):
        pair = f"{path[i]}/{path[i+1]}"
        if pair in rates:
            total_rate *= rates[pair]
        else:
            total_rate *= 1 / rates[f"{path[i+1]}/{path[i]}"]
    return total_rate - 1  # Return profit percentage

def find_arbitrage_opportunities(rates):
    currencies = ['USD', 'EUR', 'JPY', 'GBP', 'CHF', 'CAD', 'AUD', 'NZD', 'CNY', 'INR']
    opportunities = []

    for length in range(3, 6):  # 3 to 5 currency combinations
        for path in itertools.permutations(currencies, length):
            path = list(path) + [path[0]]  # Complete the cycle
            profit = calculate_arbitrage(rates, path)
            if profit > 0:
                opportunities.append((path, profit))

    return sorted(opportunities, key=lambda x: x[1], reverse=True)

def main():
    print("Fetching exchange rates...")
    rates = get_exchange_rates()
    
    if not rates:
        print("No exchange rate data available. Exiting.")
        return

    print("Calculating arbitrage opportunities...")
    opportunities = find_arbitrage_opportunities(rates)

    if not opportunities:
        print("No profitable arbitrage opportunities found.")
    else:
        print("\nTop 10 Most Profitable Arbitrage Opportunities:")
        for i, (path, profit) in enumerate(opportunities[:10], 1):
            print(f"{i}. Path: {' -> '.join(path)}")
            print(f"   Potential profit: {profit:.4%}")

    print("\nArbitrage opportunities by number of currencies involved:")
    opportunities_by_length = defaultdict(list)
    for path, profit in opportunities:
        opportunities_by_length[len(path) - 1].append((path, profit))

    for length in range(3, 6):
        top_opportunities = sorted(opportunities_by_length[length], key=lambda x: x[1], reverse=True)[:5]
        print(f"\nTop 5 {length}-currency arbitrage opportunities:")
        for i, (path, profit) in enumerate(top_opportunities, 1):
            print(f"{i}. Path: {' -> '.join(path)}")
            print(f"   Potential profit: {profit:.4%}")

if __name__ == "__main__":
    main()