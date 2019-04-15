import numpy as np
import pandas as pd
# from pandas_datareader import data, web
import fix_yahoo_finance as yf
import datetime
from dateutil.relativedelta import relativedelta


def load_index_trace(list_index=0, time_years=1):
    """Load index traces for indices.

    ^OMX =OMXS30
    Consider to add Six30RX
    """
    # Which indexes to load ^IXIC (nasdaq), ^GSPC (sp500) ^OMXS30,
    indices = ['^OMX', '^IXIC', '^GSPC', '^OMXS30']

    # Between which dates
    start = datetime.datetime.now() - relativedelta(years=time_years)
    end = datetime.datetime.now()

    df = pd.DataFrame()

    for index in indices:
        data = yf.download(index, start=start, end=end)

        df[index] = data['Close']
        df[index + '_MA50'] = data['Close'].rolling(50).mean()
        df[index + '_MA200'] = data['Close'].rolling(200).mean()
    return df, indices


if __name__ == '__main__':
    """Test."""
    print("test")
    df, idx = load_index_trace()
    print(idx)
    print(df.head())
    df.plot()
