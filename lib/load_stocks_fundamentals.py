import pandas as pd
from lib.get_avanza_fundamentals import get_avanza_fundamentals
from lib.get_yahoo_fundamentals import get_yahoo_fundamentals


def load_stocks_fundamentals():
    """Load stocks fundamentals.

    Avanza
    Yahoo
    """
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

    # Load fundamentals from Avanza
    avanza_stocks = ['ABB.ST',
                     'ATCO-B.ST',
                     'AXFO.ST',
                     'BOL.ST',
                     'CAST.ST',
                     'DIOS.ST',
                     'ESSITY-B.ST',
                     'FABG.ST',
                     'HEMF.ST',
                     'HUFV-A.ST',
                     'HOLM-B.ST',
                     'ICA.ST',
                     'INVE-B.ST',
                     'INDU-C.ST',
                     'KINV-B.ST',
                     'LUND.ST',
                     'LATO-B.ST',
                     'WALL-B.ST',
                     'SCA-B.ST',
                     'SEB-C.ST',
                     'SHB-B.ST',
                     'SKA-B.ST',
                     'SWED-A.ST',
                     'HM-B.ST',
                     'NP3.ST',
                     'TIETO.HE']
    for stock in avanza_stocks:
        stock_df = get_avanza_fundamentals(stock)
        df = df.append(stock_df, ignore_index=True, sort=False)

    # Load fundamentals from Yahoo
    yahoo_stocks = ['AAPL',
                    'KO',
                    'T',
                    'MCD',
                    'PEP',
                    'GOOG',
                    'AMZN',
                    'GS',
                    'JPM',
                    'INTC',
                    'O']

    for stock in yahoo_stocks:
        stock_df = get_yahoo_fundamentals(stock)
        df = df.append(stock_df, ignore_index=True, sort=False)

    return df


if __name__ == '__main__':
    df_test = load_stocks_fundamentals()
    print(df_test.head(20))
