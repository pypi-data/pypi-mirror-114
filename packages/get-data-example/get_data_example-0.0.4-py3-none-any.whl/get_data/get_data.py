"""
Module provide method for get data from yfinance library and save it into csv file
"""

import os
import datetime as dt
from argparse import ArgumentParser
import yfinance as yf




def get_hour_data(tick_name: str, date: str) -> None:
    """
    Downloads data for specific date and hour for specific tick (company)
    :param tick_name: stocj name of company
    :param date: string dae representation in format %Y-%m-%d-%H
    :return: None
    """
    date = dt.datetime.strptime(date, "%Y-%m-%d-%H")
    ticker = yf.Ticker(tick_name)
    date = date - dt.timedelta(hours=1)
    hist_df = ticker.history(period="1h", interval='1m', end=date)
    hour = str(date.hour)
    str_date = date.strftime("%Y-%m-%d")
    path = os.path.abspath('./data/original/' + tick_name + '/' + str_date)
    if not os.path.exists(path):
        os.makedirs(path)
        print("Directory ", path, " Created ")
    hist_df.to_csv(path + '/' + hour + '.csv')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--tick_name', type=str, default='AAPL')
    parser.add_argument('--date', type=str, default=dt.datetime.now().strftime("%Y-%m-%d-%H"))
    args = parser.parse_args()

    get_hour_data(**vars(args))
