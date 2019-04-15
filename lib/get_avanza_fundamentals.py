"""Function to get fundamentals from Avanza."""
from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np
import re


def map_avanza_stock_to_url(stock_tic, site='om-aktien.html'):
    """Return URL to Avanza.

    site = 'om-aktien.html' or 'om-bolaget.html'
    """
    stock = {}
    avanza_url = "https://www.avanza.se/aktier/" + site

    stock['ABB.ST'] = avanza_url + "/5447/abb-ltd"
    stock['ATCO-B.ST'] = avanza_url + "/5235/atlas-copco-b"
    stock['AXFO.ST'] = avanza_url + "/5465/axfood"
    stock['BOL.ST'] = avanza_url + "/5564/boliden"
    stock['CAST.ST'] = avanza_url + "/5353/castellum"
    stock['DIOS.ST'] = avanza_url + "/43267/dios-fastigheter"
    stock['ESSITY-B.ST'] = avanza_url + "/764241/essity-b"
    stock['FABG.ST'] = avanza_url + "/5300/fabege"
    stock['HUFV-A.ST'] = avanza_url + "/5287/hufvudstaden-a"
    stock['HM-B.ST'] = avanza_url + "/5364/hennes---mauritz-b"
    stock['HOLM-B.ST'] = avanza_url + "/5251/holmen-b"
    stock['HEMF.ST'] = avanza_url + "/470196/hemfosa-fastigheter"
    stock['ICA.ST'] = avanza_url + "/31607/ica-gruppen"
    stock['INVE-B.ST'] = avanza_url + "/5247/investor-b"
    stock['INDU-C.ST'] = avanza_url + "/5245/industrivarden-c"
    stock['KINV-B.ST'] = avanza_url + "/5369/kinnevik-b"
    stock['LUND.ST'] = avanza_url + "/5375/lundbergforetagen-b"
    stock['LATO-B.ST'] = avanza_url + "/5321/latour-b"
    stock['NP3.ST'] = avanza_url + "/522855/np3-fastigheter"
    stock['SCA-B.ST'] = avanza_url + "/5263/sca-b"
    stock['SEB-C.ST'] = avanza_url + "/5256/seb-c"
    stock['SHB-B.ST'] = avanza_url + "/5265/handelsbanken-b"
    stock['SKA-B.ST'] = avanza_url + "/5257/skanska-b"
    stock['SWED-A.ST'] = avanza_url + "/5241/swedbank-a"
    stock['TIETO.HE'] = avanza_url + "/5455/tieto-oyj"
    stock['WALL-B.ST'] = avanza_url + "/5344/wallenstam-b"
    return stock[stock_tic]


def get_avanza_fundamentals(stock_tic):
    """HTML parser to get stock fundamentals from Avanza."""
    # Parse "om-aktien.html"
    stock_url = map_avanza_stock_to_url(stock_tic, site='om-aktien.html')
    r = requests.get(stock_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    kort_namn = soup.find(
        'dt', string='Kortnamn').find_next_sibling('dd').string
    # Dividend_yield
    dividend_yield = soup.find(
        'dt', string='Direktavkastning %').find_next_sibling('dd').string
    dividend_yield = float(dividend_yield.replace(',', '.'))*0.01
    # PE-ratio
    pe_ratio = soup.find(
            'dt', string='P/E-tal').find_next_sibling('dd').string
    pe_ratio = float(pe_ratio.replace(',', '.'))
    # Price/Book, Kurs/Eget kapital
    price_book = soup.find(
            'dt', string='Kurs/eget kapital ').find_next_sibling('dd').string
    price_book = float(price_book.replace(',', '.'))
    # EPS
    eps_sek = soup.find(
            'dt', string='Vinst/aktie SEK').find_next_sibling('dd').string
    eps_sek = float(eps_sek.replace(',', '.'))
    # Börsvärde (market cap)
    market_cap = soup.find(
            'dt', string=re.compile('Börsvärde')).find_next_sibling('dd').string
    market_cap = market_cap.replace(',', '.')
    market_cap = market_cap.replace("\xa0", "")
    market_cap = float(market_cap)
    # Antal aktier
    antal_aktier = soup.find(
        'dt', string='Antal aktier').find_next_sibling('dd').string
    antal_aktier = float(market_cap)

    # Get info from "om-bolaget.html"
    stock_url = map_avanza_stock_to_url(stock_tic, site='om-bolaget.html')
    r = requests.get(stock_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    # dividend/earnings
    dividend_earnings = soup.find(
        'dt', string='Andel utdelad vinst %').find_next_sibling('dd').string
    try:
        dividend_earnings = float(dividend_earnings.replace(',', '.'))*0.01
    except Exception:
        dividend_earnings = np.nan

    # Långfristiga skulder
    long_liabilities = soup.find(
        'td', string='Långfristiga skulder').find_next_sibling('td').string
    long_liabilities = float(long_liabilities.replace(u'\xa0', ''))
    # Kortfristiga skulder
    short_liabilities = soup.find(
        'td', string='Kortfristiga skulder').find_next_sibling('td').string
    short_liabilities = float(short_liabilities.replace(u'\xa0', ''))
    # Omsättningstillgångar
    current_assets = soup.find(
        'td', string='Summa omsättningstillgångar').find_next_sibling('td').string
    current_assets = float(current_assets.replace(u'\xa0', ''))
    # Kassa och bank
    cash_assets = soup.find(
        'td', string='Kassa och bank').find_next_sibling('td').string
    cash_assets = float(cash_assets.replace(u'\xa0', ''))
    # NCAVPS net current assets value per share
    ncavps = (current_assets-(long_liabilities+short_liabilities))/antal_aktier
    # net cash
    net_cash_ps = (cash_assets-(long_liabilities+short_liabilities))/antal_aktier

    # Add to dataframe
    d = {'kortnamn': stock_tic,
         'dividend_yield': dividend_yield,
         'antal_aktier': antal_aktier,
         'pe_ratio': pe_ratio,
         'eps': eps_sek,
         'market_cap': market_cap,
         'dividend/earnings': dividend_earnings,
         'ncavps': ncavps,
         'net_cash_ps': net_cash_ps,
         'price_book': price_book}

    df = pd.DataFrame(data=d, index=[0])

    return df


if __name__ == '__main__':
    data = get_avanza_fundamentals('BOL.ST')
    print(data.head())
