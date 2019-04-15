import numpy as np
import pandas as pd
# from pandas_datareader import data, web
import fix_yahoo_finance as yf
import datetime
from dateutil.relativedelta import relativedelta


def load_stocks_trace(list_stocks=0, time_years=1):
    """Import traces for stocks."""
    stocks = ['AAPL',
              'ABB.ST',
              'AMZN',
              'ATCO-B.ST',
              'AXFO.ST',
              'BOL.ST',
              'BRK-B',
              'CAST.ST',
              'DIOS.ST',
              'ERIC-B.ST',
              'ESSITY-B.ST',
              'FABG.ST',
              'GOOG',
              'GS',
              'HEMF.ST',
              'HUFV-A.ST',
              'HOLM-B.ST',
              'HM-B.ST',
              'ICA.ST',
              'INVE-B.ST',
              'JPM',
              'KINV-B.ST',
              'LATO-B.ST',
              'LUND-B.ST',
              'PAT.V',
              'SCA-B.ST',
              'SHB-B.ST',
              'SEB-C.ST',
              'SKA-B.ST',
              'SWED-A.ST',
              'WALL-B.ST']
    # stocks = ['BOL.ST']
    # Dates
    start = datetime.datetime.now() - relativedelta(years=time_years)
    end = datetime.datetime.now()

    # Get data
    data = yf.download(stocks, start=start, end=end)
    # print(data.head())
    data = data['Close']  # Just closing price
    # print(data.keys())
    return data


if __name__ == '__main__':
    print("test")
    df = load_stocks_trace()
    print(df.head())
