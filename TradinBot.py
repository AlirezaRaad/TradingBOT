import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import datetime as dt
from typing import Optional, Literal


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
        shorterTf: Literal[
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
        longerTf: Optional[
            Literal[
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
            ]
        ] = None,
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
        shorterTf : Shorter-term MA Time Frame
        longerTf : Longer-term MA Time Frame. Dont Give Value To Use Shorter-term MA Time Frame

        If you dont provide a TimeFrame For longerTf, it will get shorterTf value.

        nShortCandle : Number Of Candles With You Selected in shorterTf.
        nLongCandle : Number Of Candles With You Selected in longerTf.

        example:
        \tnShortCandle = 50 & nLongCandle = 200 & shorterTf 10 minutes -> bring 50 of most recent 10min bars data. BECAUSE we did not provide longerTf, it will bring 200 of most recent 10min bars data.
        ------------------------
        You Can Select You Short-Term and Long-term MA to trigger BUY/SELL orders.

        ------------------------

        """
        from MovingAverage import MovingAverage

        if longerTf is None:
            longerTf = shorterTf

        theMA = {"shortMA": dict(), "longMA": dict()}

        # Stores the value of current Moving average based on the given parameters to later compare the most recent Ma number with last one
        # To see if they Crossed Or Not.

        shorter_MA = MovingAverage(
            kind=kind,
            symbol=symbol,
            period=nShortCandle,
            timeframe=shorterTf,
            calc_meth=applyWhere.lower(),
        )

        longerTf_MA = MovingAverage(
            kind=kind,
            symbol=symbol,
            period=nLongCandle,
            timeframe=longerTf,
            calc_meth=applyWhere.lower(),
        )

        # Now It is Time To Implement Strategy.

    def SelectStrategy(self, strategy: Literal["MA", "RSI"]):
        """
        See availableStrategies() to Select Your Strategy.
        """
        if strategy.upper() not in self.availableStrategies:
            raise TypeError(
                "Please Select Your Strategy From TradingBot.availableStrategies"
            )

    def __repr__(self):
        return f"TradingBot(username={self.username}, password={self.password}, server={self.server})"
