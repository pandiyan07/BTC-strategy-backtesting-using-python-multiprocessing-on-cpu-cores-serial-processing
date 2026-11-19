# Project Title

**Multiprocessing Trading Strategy Backtester with EMA, ATR &
Performance Analytics**

## Table of Contents

-   [About The Project](#about-the-project)
-   [Built With](#built-with)
-   [Key Features](#key-features)
-   [Getting Started](#getting-started)
-   [Technologies Used
    (Prerequisites)](#technologies-used-prerequisites)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Project Structure](#project-structure)
-   [How It Works](#how-it-works)
-   [Main Python Functions](#main-python-functions)
-   [Output Report](#output-report)
-   [Performance Notes](#performance-notes)
-   [License Description](#license-description)
-   [Disclaimer](#disclaimer)

## About The Project

This project is a parameter-optimization backtesting engine for
rule-based trading strategies. It loads Binance's Bicoin historical OHLC data stored offline, computes
EMA and ATR indicators, evaluates thousands of parameter combinations in
parallel using multiprocessing, simulates long and short trades,
measures profitability, winning percentage, trade statistics, ATR
filters, and exports a ranked Excel report containing the
best-performing parameter sets.

### Built With

-   Python 3
-   pandas
-   NumPy
-   pandas-ta
-   multiprocessing
-   datetime

### Key Features

-   EMA (5 & 34) calculation
-   ATR-based volatility filter
-   Long & short trade simulation
-   Parameter grid optimization
-   Multiprocessing execution
-   Winning percentage calculation
-   Top 5 profitable trades
-   Least profitable trades
-   Net/Gross P&L calculation
-   Excel report generation

## Getting Started

### Technologies Used (Prerequisites)

-   Python 3.10+
-   pip
-   pandas
-   numpy
-   pandas-ta
-   openpyxl

### Installation

``` bash
git clone https://github.com/yourusername/trading-backtester.git
cd trading-backtester
pip install pandas numpy pandas-ta openpyxl
python backtester_final_with_winning_percentage_top_five_trades_atr_and_tsl.py
```

## Usage

Configure the CSV input path, parameter ranges and output Excel
location, then execute the script. The program evaluates all parameter
combinations and generates a ranked optimization report.

## Project Structure

``` text
backtester_final_with_winning_percentage_top_five_trades_atr_and_tsl.py
│
├── EMA_CALCULATOR()          # Calculates EMA values
├── ATR_CALCULATOR()          # Calculates ATR values
├── TRADE_EXIT_WORK()         # Updates trade statistics
├── TRADING_BOT()            # Executes parameterized backtests
└── Main Program             # Loads data, launches workers, exports report
```

## How It Works

1.  Load historical OHLC data from CSV.
2.  Calculate EMA and ATR indicators.
3.  Generate parameter combinations.
4.  Split workload across CPU cores.
5.  Simulate long and short trades.
6.  Apply EMA and ATR entry filters.
7.  Exit trades using EMA-gap logic.
8.  Calculate profit, loss and win rate.
9.  Rank parameter combinations.
10. Export the final Excel report.

## Main Python Functions

  -----------------------------------------------------------------------
  Function                            Description
  ----------------------------------- -----------------------------------
  `EMA_CALCULATOR()`                  Computes Exponential Moving Average
                                      values.

  `ATR_CALCULATOR()`                  Computes Average True Range values.

  `TRADE_EXIT_WORK()`                 Updates cumulative profit, loss and
                                      winning-trade statistics.

  `TRADING_BOT()`                     Runs the complete backtest and
                                      parameter optimization workflow.
  -----------------------------------------------------------------------

## Output Report

The generated Excel report includes: - Net Profit - Total Profit - Total
Loss - Winning Percentage - Number of Trades - Long Trades - Short
Trades - Top 5 Profitable Trades - Least Profitable Trades - EMA
Parameters - ATR Values - Strategy Parameters

## Performance Notes

-   Uses multiprocessing to distribute parameter ranges across CPU
    cores.
-   Supports large-scale optimization over thousands of parameter
    combinations.
-   Produces a sortable report for identifying high-performing
    strategies.

## License Description

Recommended License: MIT License.

Permission is granted to use, modify, distribute and commercialize the
software while retaining the original copyright notice.

## Disclaimer

This project is intended for educational, research and
strategy-development purposes only. Past performance does not guarantee
future results. Validate all strategies before using them in live
trading.
