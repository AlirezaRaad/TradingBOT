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
            "High Price",
            "Low Price",
            "Median Price",
            "Typical Price",
            "Weighted Close",
        ] = "Median Price",
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


class MovingAverage(TradingBot):
    """
    This class provides methods to calculate different types of Moving Averages.

    Methods:
    --------
    SMA(prices: list, period: int) -> float
        Calculates the Simple Moving Average (SMA).

        Formula:
        SMA = (P1 + P2 + ... + Pn) / N

        Where:
        - Pn = Price at period n
        - N  = Number of periods

    EMA(prices: list, period: int) -> float
        Calculates the Exponential Moving Average (EMA).

        Formula:
        EMA_t = α * P_t + (1 - α) * EMA_{t-1}

        Where:
        - P_t = Current price
        - α = 2 / (N + 1) (Smoothing factor)
        - N  = Number of periods
        - EMA_{t-1} = Previous EMA value

    SMMA(prices: list, period: int) -> float
        Calculates the Smoothed Moving Average (SMMA).

        Formula:
        SMMA_t = (SMMA_{t-1} * (N - 1) + P_t) / N

        Where:
        - P_t = Current price
        - N  = Number of periods
        - SMMA_{t-1} = Previous SMMA value

    WMA(prices: list, period: int) -> float
        Calculates the Weighted Moving Average (WMA).

        Formula:
        WMA = (P1 * W1 + P2 * W2 + ... + Pn * Wn) / (W1 + W2 + ... + Wn)

        Where:
        - Pn = Price at period n
        - Wn = Weight at period n (typically Wn = n for recent price emphasis)
        - N  = Number of periods

    """

    def __init__(self, kind, symbol, short, long, shortTf, longTf, applyWhere):
        self.kind = kind
        self.symbol = symbol
        self.short = short
        self.long = long
        self.shortTf = shortTf
        self.longTf = longTf
        self.applyWhere = applyWhere
        self.WhereToApply = {
            "close",
            "open",
            "high price",
            "low price",
            "median price",
            "typical price",
            "weighted close",
        }

        self.timeframes = {
            "1 minute": mt5.TIMEFRAME_M1,
            "2 minutes": mt5.TIMEFRAME_M2,
            "3 minutes": mt5.TIMEFRAME_M3,
            "4 minutes": mt5.TIMEFRAME_M4,
            "5 minutes": mt5.TIMEFRAME_M5,
            "6 minutes": mt5.TIMEFRAME_M6,
            "10 minutes": mt5.TIMEFRAME_M10,
            "12 minutes": mt5.TIMEFRAME_M12,
            "15 minutes": mt5.TIMEFRAME_M15,
            "20 minutes": mt5.TIMEFRAME_M20,
            "30 minutes": mt5.TIMEFRAME_M30,
            "1 hour": mt5.TIMEFRAME_H1,
            "2 hour": mt5.TIMEFRAME_H2,
            "3 hours": mt5.TIMEFRAME_H3,
            "4 hours": mt5.TIMEFRAME_H4,
            "6 hours": mt5.TIMEFRAME_H6,
            "8 hours": mt5.TIMEFRAME_H8,
            "12 hours": mt5.TIMEFRAME_H12,
            "1 day": mt5.TIMEFRAME_D1,
            "1 week": mt5.TIMEFRAME_W1,
            "1 month": mt5.TIMEFRAME_MN1,
        }

    def GetData(self):
        dfShort = pd.DataFrame(
            mt5.copy_rates_from_pos(
                self.symbol, self.timeframes[self.shortTf], 0, self.long
            )
        ).add_prefix("S_")
        dfShort.index = dfShort["S_time"]
        dfShort.drop(columns=["S_time", "S_real_volume"], inplace=True)

        dfLong = pd.DataFrame(
            mt5.copy_rates_from_pos(
                self.symbol, self.timeframes[self.longTf], 0, self.long
            )
        ).add_prefix("L_")
        dfLong.index = dfLong["L_time"]
        dfLong.drop(columns=["L_time", "L_real_volume"], inplace=True)
        if dfShort.empty or dfLong.empty:
            return ValueError("One or both DataFrames are empty!")

        kh = pd.DataFrame(pd.concat([dfShort, dfLong], axis=1))

        return kh

    def SMA(self):
        """
        SMA(prices: list, period: int) -> float
        Calculates the Simple Moving Average (SMA).

        Formula:
        SMA = (P1 + P2 + ... + Pn) / N

        Where:
        - Pn = Price at period n
        - N  = Number of periods
        """
        if self.applyWhere.lower() in self.WhereToApply:
            print(self.applyWhere.lower())

        df = self.GetData()

    def CalculateSMA(self):
        pass

    def EMA(self):
        """
        EMA(prices: list, period: int) -> float
        Calculates the Exponential Moving Average (EMA).

        Formula:
        EMA_t = α * P_t + (1 - α) * EMA_{t-1}

        Where:
        - P_t = Current price
        - α = 2 / (N + 1) (Smoothing factor)
        - N  = Number of periods
        - EMA_{t-1} = Previous EMA value
        """
        pass

    def SMMA(self):
        """
        SMMA(prices: list, period: int) -> float
        Calculates the Smoothed Moving Average (SMMA).

        Formula:
        SMMA_t = (SMMA_{t-1} * (N - 1) + P_t) / N

        Where:
        - P_t = Current price
        - N  = Number of periods
        - SMMA_{t-1} = Previous SMMA value
        """
        pass

    def WMA(self):
        """
        WMA(prices: list, period: int) -> float
        Calculates the Weighted Moving Average (WMA).

        Formula:
        WMA = (P1 * W1 + P2 * W2 + ... + Pn * Wn) / (W1 + W2 + ... + Wn)

        Where:
        - Pn = Price at period n
        - Wn = Weight at period n (typically Wn = n for recent price emphasis)
        - N  = Number of periods
        """
        pass
