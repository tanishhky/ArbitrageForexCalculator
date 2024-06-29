import yfinance as yf
import itertools
from collections import defaultdict

BROKER_FEE_PERCENTAGE = 0.000  # 0.02% fee per transaction
MINIMUM_PROFIT_THRESHOLD = 0.001  # 0.1% minimum profit after fees

def get_exchange_rates():
    currencies = ['USD', 'EUR', 'JPY', 'GBP', 'CHF', 'CAD', 'AUD', 'NZD', 'CNY', 'INR']
    rates = {}
    for base in currencies:
        for quote in currencies:
            if base != quote:
                pair = f"{base}{quote}=X"
                try:
                    ticker = yf.Ticker(pair)
                    bid = ticker.info['bid']
                    ask = ticker.info['ask']
                    if bid and ask:
                        spread = (ask - bid) / ((ask + bid) / 2)
                        rates[f"{base}/{quote}"] = {
                            'bid': bid,
                            'ask': ask,
                            'spread': spread
                        }
                        print(f"Fetched rate for {base}/{quote}: Bid {bid:.6f}, Ask {ask:.6f}, Spread {spread:.4%}")
                    else:
                        print(f"No bid/ask data available for {pair}")
                except Exception as e:
                    print(f"Error fetching data for {pair}: {e}")
    return rates

def calculate_arbitrage(rates, path, initial_amount=100000):
    amount = initial_amount
    for i in range(len(path) - 1):
        pair = f"{path[i]}/{path[i+1]}"
        if pair in rates:
            amount *= rates[pair]['bid'] * (1 - BROKER_FEE_PERCENTAGE)
        else:
            amount /= rates[f"{path[i+1]}/{path[i]}"]['ask'] * (1 + BROKER_FEE_PERCENTAGE)
    return (amount / initial_amount) - 1  # Return profit percentage

def find_arbitrage_opportunities(rates, initial_amount=100000):
    currencies = ['USD', 'EUR', 'JPY', 'GBP', 'CHF', 'CAD', 'AUD', 'NZD', 'CNY', 'INR']
    opportunities = []

    for length in range(3, 6):  # 3 to 5 currency combinations
        for path in itertools.permutations(currencies, length):
            path = list(path) + [path[0]]  # Complete the cycle
            profit = calculate_arbitrage(rates, path, initial_amount)
            if profit > MINIMUM_PROFIT_THRESHOLD:
                opportunities.append((path, profit, profit * initial_amount))

    return sorted(opportunities, key=lambda x: x[1], reverse=True)

def main():
    print("Fetching exchange rates...")
    rates = get_exchange_rates()
    
    if not rates:
        print("No exchange rate data available. Exiting.")
        return

    print("Calculating arbitrage opportunities...")
    initial_amount = 100000  # USD
    opportunities = find_arbitrage_opportunities(rates, initial_amount)

    if not opportunities:
        print("No profitable arbitrage opportunities found.")
    else:
        print(f"\nTop 10 Most Profitable Arbitrage Opportunities (Initial Amount: ${initial_amount}):")
        for i, (path, profit_percentage, profit_amount) in enumerate(opportunities[:10], 1):
            print(f"{i}. Path: {' -> '.join(path)}")
            print(f"   Potential profit: {profit_percentage:.4%} (${profit_amount:.2f})")
            print(f"   Total return: ${initial_amount + profit_amount:.2f}")

    print(f"\nNote: These calculations include actual spreads from current bid/ask prices and a broker fee of {BROKER_FEE_PERCENTAGE:.4%} per transaction.")
    print(f"Only opportunities with a profit above {MINIMUM_PROFIT_THRESHOLD:.4%} are shown.")
    print("Remember that forex rates change rapidly, and these opportunities may no longer be available.")

if __name__ == "__main__":
    main()