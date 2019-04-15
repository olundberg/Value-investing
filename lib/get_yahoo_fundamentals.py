"""Function to get fundamentals from Avanza."""
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import numpy as np
pd.set_option('display.max_columns', 50)


def find_keyword_value(soup, keyword):
    """Find value based on keyword from Yahoo."""
    pass
    return value


def map_yahoo_stock_to_url(stock_tic):
    """Return URL to Avanza."""
    stock = {}
    stock['AAPL'] = "https://finance.yahoo.com/quote/AAPL/"
    stock['KO'] = "https://finance.yahoo.com/quote/KO/"
    stock['T'] = "https://finance.yahoo.com/quote/T/"
    stock['MCD'] = "https://finance.yahoo.com/quote/MCD/"
    stock['PEP'] = "https://finance.yahoo.com/quote/PEP/"
    stock['GOOG'] = "https://finance.yahoo.com/quote/GOOG/"
    stock['AMZN'] = "https://finance.yahoo.com/quote/AMZN/"
    stock['INTC'] = "https://finance.yahoo.com/quote/INTC/"
    stock['GS'] = "https://finance.yahoo.com/quote/GS/"
    stock['JPM'] = "https://finance.yahoo.com/quote/JPM/"
    stock['O'] = "https://finance.yahoo.com/quote/O/"
    return stock[stock_tic]


def get_yahoo_fundamentals(stock_tic, type='html'):
    """HTML parser to get stock fundamentals from Yahoo.

    type = 'html' or 'API'
    """
    if type == 'html':
        # Parse HTML
        stock_url = map_yahoo_stock_to_url(stock_tic)
        r = requests.get(stock_url)
        soup = BeautifulSoup(r.content, 'html.parser')



        # Get values from html
        dividend_yield = soup.findAll(
            'td',
            {"data-test": "DIVIDEND_AND_YIELD-value"})[0].string
        try:
            dividend_yield = float(
                re.findall(r"\d+\.\d+", dividend_yield)[1])*0.01
        except:
            dividend_yield = np.nan

        antal_aktier = np.nan

        pe_ratio = soup.findAll(
            'td',
            {"data-test": "PE_RATIO-value"})[0].string
        pe_ratio = float(pe_ratio)

        eps = soup.findAll(
            'td',
            {"data-test": "EPS_RATIO-value"})[0].string
        eps = float(eps)

        market_cap = soup.findAll(
            'td',
            {"data-test": "MARKET_CAP-value"})[0].string
        market_cap = market_cap

        try:
            # Test to find payout ratio
            ans = re.findall(r"payoutRatio\":{\"raw\":\d+.\d+", str(soup))
            ans = re.findall(r"\d+.\d+", ans[0])
            dividend_earnings = float(ans[0])
        except:
            print("Could not find payout ratio for {}".format(stock_tic))
            dividend_earnings = np.nan

        ncavps = np.nan

        net_cash_ps = np.nan

        price_book = np.nan

        # Add to dataframe
        d = {'kortnamn': stock_tic,
             'dividend_yield': dividend_yield,
             'antal_aktier': antal_aktier,
             'pe_ratio': pe_ratio,
             'eps': eps,
             'market_cap': market_cap,
             'dividend/earnings': dividend_earnings,
             'ncavps': ncavps,
             'net_cash_ps': net_cash_ps,
             'price_book': price_book}

        df = pd.DataFrame(data=d, index=[0])
    elif type == 'API':
        pass

    return df


if __name__ == '__main__':
    columns = ['kortnamn',
               'dividend_yield',
               'pe_ratio',
               'eps',
               'market_cap',
               'dividend/earnings',
               'ncavps',
               'net_cash_ps',
               'price_book']
    df = pd.DataFrame(columns=columns)
    yahoo_stocks = ['AAPL',
                    'KO',
                    'T',
                    'MCD',
                    'PEP',
                    'GOOG',
                    'AMZN',
                    'INTC',
                    'JPM',
                    'GS',
                    'O']
    for stock in yahoo_stocks:
        stock_df = get_yahoo_fundamentals(stock)
        df = df.append(stock_df, ignore_index=True)

    print(df.head(30))
