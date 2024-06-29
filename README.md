# Multi-Currency Arbitrage Calculator

## Table of Contents
1. [Overview](#overview)
2. [Forex Basics](#forex-basics)
3. [Understanding Arbitrage](#understanding-arbitrage)
4. [Our Approach](#our-approach)
5. [Features](#features)
6. [Prerequisites](#prerequisites)
7. [Installation](#installation)
8. [Usage](#usage)
9. [How It Works](#how-it-works)
10. [Strengths and Limitations](#strengths-and-limitations)
11. [Disclaimer](#disclaimer)

## Overview

This Python script calculates potential arbitrage opportunities across multiple currencies in the Forex market. It considers combinations of 3 to 5 currencies, identifying and ranking potential profitable trades based on current exchange rates.

## Forex Basics

Forex, short for Foreign Exchange, is the global marketplace for trading national currencies. It's the largest and most liquid financial market in the world, with an average daily trading volume exceeding $6 trillion.

Key concepts:
- Currency Pairs: Currencies are always quoted in pairs (e.g., USD/EUR), representing the exchange rate between two currencies.
- Base/Quote Currency: In USD/EUR, USD is the base currency, and EUR is the quote currency.
- Bid/Ask Spread: The difference between the buying (ask) and selling (bid) price of a currency pair.

## Understanding Arbitrage

Arbitrage is the simultaneous buying and selling of an asset in different markets to profit from tiny differences in the asset's listed price. In Forex, this often involves exploiting price discrepancies between different currency pairs.

Types of Forex arbitrage our script considers:
1. Triangular Arbitrage: Involves three different currencies.
2. Four-way Arbitrage: Involves four different currencies.
3. Five-way Arbitrage: Involves five different currencies.

Example of triangular arbitrage:
1. Convert USD to EUR
2. Convert EUR to GBP
3. Convert GBP back to USD

If the final amount of USD is greater than the initial amount, an arbitrage opportunity exists.

## Our Approach

Our script automates the process of identifying potential arbitrage opportunities:

1. We fetch real-time exchange rates for 10 major currencies.
2. We calculate all possible 3-way, 4-way, and 5-way currency combinations.
3. For each combination, we compute the potential profit if a trader were to execute the series of exchanges.
4. We rank these opportunities based on potential profitability.

## Features

- Fetches real-time exchange rates for 10 major currencies
- Calculates arbitrage opportunities for 3-way, 4-way, and 5-way currency combinations
- Ranks opportunities by potential profitability
- Displays top 10 overall opportunities and top 5 for each combination type

## Prerequisites

- Python 3.6+
- yfinance library

## Installation

1. Clone this repository or download the script.
2. Install the required library:
```pip install yfinance```


## Usage

Run the script from the command line:
```python arbitrage_calculator.py```

The script will fetch current exchange rates, calculate arbitrage opportunities, and display the results.

## How It Works

1. **Data Fetching**: The `get_exchange_rates()` function uses the yfinance library to fetch the most recent exchange rates for all combinations of the 10 specified currencies.

2. **Arbitrage Calculation**: The `calculate_arbitrage()` function computes the potential profit for a given sequence of currency exchanges.

3. **Opportunity Finding**: The `find_arbitrage_opportunities()` function generates all possible 3 to 5 currency combinations and calculates the potential profit for each.

4. **Result Ranking**: The opportunities are sorted by profitability in descending order.

5. **Output**: The main function displays the top 10 overall opportunities and the top 5 opportunities for each category (3, 4, and 5-currency combinations).

## Strengths and Limitations

### Strengths:
1. Comprehensive Analysis: Our approach considers a wide range of currency combinations, potentially identifying opportunities that might be missed by simpler systems.
2. Real-time Data: By using current exchange rates, the script provides timely information.
3. Ranking System: Sorting opportunities by profitability helps users focus on the most promising trades.
4. Flexibility: The script can be easily modified to include different currencies or adjust the number of currencies in each combination.

### Limitations:
1. Transaction Costs: Our calculations don't account for spreads, fees, or other transaction costs, which can significantly impact profitability.
2. Execution Speed: By the time a user could act on the information, market conditions may have changed, eliminating the arbitrage opportunity.
3. Data Reliability: The free tier of Yahoo Finance may not provide data that's as reliable or up-to-date as professional Forex data feeds.
4. Simplistic Profit Calculation: Our profit calculation doesn't consider the amount of capital required or potential risks involved in each trade.
5. API Limitations: Frequent requests to Yahoo Finance might lead to rate limiting or IP blocking.
6. Market Depth: The script doesn't consider the volume available at each exchange rate, which is crucial for executing large trades.
7. Regulatory and Practical Constraints: The script doesn't account for regulatory restrictions or practical limitations that might prevent certain trades.

## Disclaimer

This script is for educational purposes only. Arbitrage trading carries significant risks and may not be legal or permissible in all jurisdictions. Always consult with financial and legal professionals before engaging in any trading activities.