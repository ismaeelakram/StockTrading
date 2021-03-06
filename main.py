from dotenv import load_dotenv
load_dotenv()
import robin_stocks as robinhood
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chalk
import time

from stock import Stock
from helpers import get_active_stocks, get_cheapest_stock, buy_stock, get_stocks, sell_stock

# Login to Robinhood
# print(chalk.green("Logging into Robinhood..."))
# account = robinhood.login(os.getenv('ROBINHOOD_USER'), os.getenv('ROBINHOOD_PASS'))

# Setup selenium browser
chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=chrome_options)

# Get active stocks
stocks = get_active_stocks(browser)

# Get cheapest stock
cheapest_stock = get_cheapest_stock(stocks)
print(chalk.green("Cheapest stock is: ") + f"{cheapest_stock.symbol} ({cheapest_stock.name}) (${cheapest_stock.price})")

# Check if you already own cheapest stock
current_stocks = get_stocks()
stock_found = False
for stock in current_stocks:
    # [(symbol, name, shares, initial_price)]
    if(stock[0] == cheapest_stock.symbol):
        stock_found = True
if not stock_found:
    buy_stock(cheapest_stock, 4)

print(chalk.blue("Beginning stock price listening..."))
while True:
    print(chalk.blue("Checking stocks again..."))
    for stock in get_stocks():
        # [(symbol, name, shares, initial_price)]
        
        browser.get(f'https://finance.yahoo.com/quote/{stock[0]}')
        new_price = float(browser.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[4]/div/div/div/div[3]/div[1]/div/span[1]').text)

        if(stock[3] > new_price):
            print(chalk.green(f"{stock[0]} stock price has gone up! Selling to earn {new_price - stock[3]}..."))
            sell_stock(stock[0], stock[2], stock[2])
        else:
            print(chalk.blue(f"{stock[0]} price has either gone down or is the same. Ignoring..."))
    time.sleep(60)