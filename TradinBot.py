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
            f"Available Strategies:\n\tMA : Moving Average(Fully customizable at TradingBot.MovingAverage())\n\tRSI : "
        )
        return {"MA": "MA", "RSI": "RSI"}

    def MovingAverage(
        self,
        symbol,
        shorterMA: int,
        longerMA: int,
        formulas: Literal["SMA", "EMA", "SMMA", "WMA"],
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
            "Close",
            "Open",
            "High",
            "Low",
            "Median",
            "Typical",
            "Weighted",
        ] = "Median ",
    ):
        """
        shorterMA : Shorter-term MA
        longerMA : Longer-term MA

        shorterTf : Shorter-term MA Time Frame
        longerTf : Longer-term MA Time Frame. Dont Give Value To Use Shorter-term MA Time Frame
        ------------------------
        You Can Select You Short-Term and Long-term MA to trigger BUY/SELL orders.

        ------------------------

        """
        if longerTf is None:
            longerTf = shorterTf
        match formulas.upper():
            case "SMA":
                sma = MovingAverage(
                    kind="SMA",
                    symbol=symbol,
                    short=shorterMA,
                    long=longerMA,
                    shortTf=shorterTf,
                    longTf=longerTf,
                    applyWhere=applyWhere,
                )
                return sma.SMA()
            case "EMA":
                pass
            case "SMMA":
                pass
            case "WMA":
                pass
            case _:
                raise TypeError("Please SElect Correct Formula.")

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
