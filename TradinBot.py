import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import datetime as dt
from typing import Optional, Literal
from types import SimpleNamespace
from collections import deque


# TODO: DONT FORGET TO ADD SQL DATABASE.
class TradingBot:
    """
    This Bot Will Trade Based On Given Parameter and Strategies.


    --------------------------------------------------------
    Methods :

    connect ==> Connects to the Metatrader5 Platform with the given User credentials. Return True if logging was successful and False If not and Raises Value Error To Stop Further processing.

    --------------------------------------------------------
    availableStrategies ==> See What Strategies Is here. Then you can use the Strategy more in depth with its own method.

    --------------------------------------------------------
    MovingAverage ==>

    --------------------------------------------------------
    get_data ==>

    back test ==> can Implement ML

    kind of strategy ma | rsi ......


    """

    def __init__(self, username, password, server):
        self._user_name_ = username
        self._pass_word_ = password
        self._ser_ver_ = server
        if not self.connect():
            raise ValueError("Enter Correct Credentials")

    @property
    def username(self):
        return self._user_name_

    @property
    def password(self):
        return self._pass_word_

    @property
    def server(self):
        return self._ser_ver_

    def connect(self):
        if mt5.initialize() and mt5.login(self.username, self.password, self.server):
            return True
        else:
            return False

    @property
    def availableStrategies(self):
        print(
            f"Available Strategies:\n\tMA : Moving Average CrossOver\n\tBuy (Golden Cross) → When the shorter moving average crosses above the longer moving average.\n\t"
            + f"Sell (Death Cross) → When the shorter moving average crosses below the longer moving average.\n\t--------------------"
            + f"\n\tRSI : (Coming Soon)"
        )
        # return {"MA": "MA", "RSI": "RSI"}
        return {"MA": "MA"}

    def MovingAverage(
        self,
        symbol,
        nShortCandle: int,
        nLongCandle: int,
        kind: Literal["SMA", "EMA", "VWMA", "WMA"],
        timeFrame: Literal[
            "1 minute",
            "2 minutes",
            "3 minutes",
            "4 minutes",
            "5 minutes",
            "6 minutes",
            "10 minutes",
            "12 minutes",
            "15 minutes",
            "20 minutes",
            "30 minutes",
            "1 hour",
            "2 hours",
            "3 hours",
            "4 hours",
            "6 hours",
            "8 hours",
            "12 hours",
            "1 day",
            "1 week",
            "1 month",
        ],
        applyWhere: Literal[
            "close",
            "open",
            "high",
            "low",
            "median",
            "typical",
            "weighted",
        ] = "median ",
    ):
        """
        timeFrame : MA Time Frame

        nShortCandle : Number Of Candles With You Selected in shorterTf.
        nLongCandle : Number Of Candles With You Selected in longerTf.

        example:
        \tnShortCandle = 50 & nLongCandle = 200 & timeFrame 10 minutes -> bring 50 of most recent 10min bars data for shorter MA and bring 200 of most recent 10min bars for the longer MA.
        ------------------------
        You Can Select You Short-Term and Long-term MA to trigger BUY/SELL orders.

        ------------------------

        """
        from MovingAverage import MovingAverage

        if kind not in MovingAverage.AllMAs():
            raise TypeError("Please Provide The CORRECT MA METHOD.")

        # Creating Shorter MovingAverage Class with its correct MA method.
        shorterMovingAverage = MovingAverage(
            kind=kind,
            symbol=symbol,
            period=nShortCandle,
            timeframe=timeFrame,
            calc_meth=applyWhere.lower(),
        )

        shorterMA = getattr(shorterMovingAverage, kind)

        # --------------------------------------------#
        longerMovingAverage = MovingAverage(
            kind=kind,
            symbol=symbol,
            period=nLongCandle,
            timeframe=timeFrame,
            calc_meth=applyWhere.lower(),
        )

        longerMA = getattr(longerMovingAverage, kind)

        # --------------------------------------------#

        # For the MA crossover strategy I need to have the previous MA and the current MA to see the if they crossed or no.
        # I have to remember that from the time of running the script the crossover maters.

        # Now It is Time To Implement Strategy.

        # I will create a loop with a dict and alway keep two element in the dict.

        # I dont Need to store values and constantly check if a new time has added or not.

        # We you fetch the last n bars it gives you the Last n bars up until that moment, it means if you fetch it
        # Constantly it will automatically update the last price.

        shorter_ma = deque(maxlen=2)
        longer_ma = deque(maxlen=2)

        # First-time initialization
        shorter_ma.append(shorterMA())
        longer_ma.append(longerMA())

        while True:
            # Calculate new values
            new_shorter = shorterMA()
            new_longer = longerMA()

            shorter_ma.append(new_shorter)
            longer_ma.append(new_longer)

            # Check for Golden Cross
            if (
                len(shorter_ma) == 2
                and shorter_ma[0] < longer_ma[0]
                and shorter_ma[1] > longer_ma[1]
            ):
                print("BUY signal detected!")

            # Check for Death Cross
            elif (
                len(shorter_ma) == 2
                and shorter_ma[0] > longer_ma[0]
                and shorter_ma[1] < longer_ma[1]
            ):
                print("SELL signal detected!")

    def SelectStrategy(self, strategy: Literal["MA", "RSI"]):
        """
        See availableStrategies() to Select Your Strategy.
        """
        if strategy.upper() not in self.availableStrategies:
            raise TypeError(
                "Please Select Your Strategy From TradingBot.availableStrategies"
            )

    def BackupTheData():
        pass

    def BuyOrder():
        pass

    def SellOrder():
        pass

    def __repr__(self):
        return f"TradingBot(username={self.username}, password={self.password}, server={self.server})"
