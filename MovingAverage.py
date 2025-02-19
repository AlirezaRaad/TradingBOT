from TradinBot import TradingBot
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import datetime as dt
from typing import Optional, Literal


# class MovingAverage(TradingBot):
class MovingAverage:
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
        self._sym_bol_ = symbol
        self.short = short
        self.long = long
        self.shortTf = shortTf
        self.longTf = longTf
        self.applyWhere = applyWhere

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
        self.WhereToApply = {
            "close",
            "open",
            "high",
            "low",
            "median",
            "typical",
            "weighted",
        }
        self.GetData()

    @property
    def symbol(self):
        return self._sym_bol_

    def GetData(self):
        dfShort = pd.DataFrame(
            mt5.copy_rates_from_pos(
                self._sym_bol_, self.timeframes[self.shortTf], 0, self.short
            )
        ).add_prefix("S_")
        dfShort["S_time"] = pd.to_datetime(dfShort["S_time"], unit="s")
        dfShort.index = dfShort["S_time"]
        dfShort.drop(columns=["S_time", "S_real_volume"], inplace=True)
        dfShort.index.rename("time", inplace=True)

        dfLong = pd.DataFrame(
            mt5.copy_rates_from_pos(
                self._sym_bol_, self.timeframes[self.longTf], 0, self.long
            )
        ).add_prefix("L_")
        dfLong["L_time"] = pd.to_datetime(dfLong["L_time"], unit="s")
        dfLong.index = dfLong["L_time"]
        dfLong.drop(columns=["L_time", "L_real_volume"], inplace=True)
        dfLong.index.rename("time", inplace=True)

        if dfShort.empty or dfLong.empty:
            return ValueError("One or both DataFrames are empty!")

        self.shorter_data, self.longer_data = dfShort, dfLong

    def Calculate(self):
        """
        This Method Calculates the Corresponding Moving Average Based On MovingAverage.applyWhere
        """
        if self.applyWhere == "median":
            self.shorter_data["S_median_MA"] = (
                self.shorter_data.S_high + self.shorter_data.S_low
            ) / 2

            self.longer_data["L_median_MA"] = (
                self.longer_data.L_high + self.longer_data.L_low
            ) / 2

        elif self.applyWhere == "typical":
            self.shorter_data["S_typical_MA"] = (
                self.shorter_data.S_high
                + self.shorter_data.S_low
                + self.shorter_data.S_close
            ) / 3

            self.longer_data["L_typical_MA"] = (
                self.longer_data.L_high
                + self.longer_data.L_low
                + self.longer_data.L_close
            ) / 3

        elif self.applyWhere == "weighted":
            self.shorter_data["S_weighted_MA"] = (
                self.shorter_data.S_high
                + self.shorter_data.S_low
                + 2 * self.shorter_data.S_close
            ) / 4

            self.longer_data["L_weighted_MA"] = (
                self.longer_data.L_high
                + self.longer_data.L_low
                + 2 * self.longer_data.L_close
            ) / 4

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
        if self.applyWhere.lower() not in self.WhereToApply:
            raise ValueError("Enter Correct price input to calculate SMA. ")

        self.longerMA = self.longer_data[f"L_{self.applyWhere}_MA"].mean()
        self.shorterMA = self.shorter_data[f"S_{self.applyWhere}_MA"].mean()

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
        if self.applyWhere.lower() not in self.WhereToApply:
            raise ValueError("Enter Correct price input to calculate EMA.")

        self.SMA()
        # EMA is kind of a Recursive FUnction So I have To make a recursive Function in order to calculate the EMA.
        # OR We can use pandas.dataFrame.ewm method to easily do the job.

        self.shorterEMA = (
            self.shorter_data[f"S_{self.applyWhere}_MA"]
            .ewm(span=self.short, adjust=False)
            .mean()
            .iloc[-1]
        )
        self.longerEMA = (
            self.shorter_data[f"S_{self.applyWhere}_MA"]
            .ewm(span=self.long, adjust=False)
            .mean()
            .iloc[-1]
        )

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
