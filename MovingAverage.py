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

    def __init__(self, kind, symbol, period, timeframe, calc_meth):
        self.kind = kind
        self.period = period
        self._sym_bol_ = symbol
        self.timeframe = timeframe

        if calc_meth not in self.whereToApply:
            raise TypeError(
                "calc_meth should be in self.whereToApply. See self.whereToApply."
            )
        self.calc_meth = calc_meth

    @property
    def symbol(self):
        return self._sym_bol_

    @property
    def alltimeframes(self):
        return {
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

    @property
    def whereToApply(self):
        return {
            "close",
            "open",
            "high",
            "low",
            "median",
            "typical",
            "weighted",
        }

    def GetData(self):
        df = pd.DataFrame(
            mt5.copy_rates_from_pos(
                self._sym_bol_, self.alltimeframes[self.timeframe], 0, self.period
            )
        )
        df["time"] = pd.to_datetime(df["time"], unit="s", utc=True)
        df.index = df["time"]
        df.drop(columns=["time", "real_volume"], inplace=True)
        df.index.rename("time", inplace=True)

        if df.empty:
            return ValueError("DataFrames are empty!")

        self.data = df

    def Calculate(self):
        """
        This Method Calculates the Corresponding Moving Average Based On MovingAverage.applyWhere
        """
        self.GetData()

        if self.calc_meth in ["close", "open", "high", "low"]:
            self.data["Calc_Price"] = self.data[self.calc_meth]
            return True

        elif self.calc_meth == "median":

            self.data["Calc_Price"] = (self.data.high + self.data.low) / 2
            return True

        elif self.calc_meth == "typical":

            self.data["Calc_Price"] = (
                self.data.high + self.data.low + self.data.close
            ) / 3
            return True

        elif self.calc_meth == "weighted":
            self.data["Calc_Price"] = (
                self.data.high + self.data.low + 2 * self.data.close
            ) / 4
            return True
        else:
            return False

    def SMA(self) -> bool:
        """
        SMA(prices: list, period: int) -> bool
        Calculates the Simple Moving Average (SMA).

        Formula:
        SMA = (P1 + P2 + ... + Pn) / N

        Where:
        - Pn = Price at period n
        - N  = Number of periods
        """
        try:
            if not self.Calculate():
                raise ValueError("Calculation Failed!")

            if self.calc_meth.lower() not in self.whereToApply:
                raise ValueError("Enter Correct calculator method to calculate SMA. ")

            self.SMA_ = self.data["Calc_Price"].mean()
            return self.SMA_
        except Exception as e:
            print(e)
            return False

    def EMA(self) -> bool:
        """
        EMA(prices: list, period: int) -> bool
        Calculates the Exponential Moving Average (EMA).

        Formula:
        EMA_t = α * P_t + (1 - α) * EMA_{t-1}

        Where:
        - P_t = Current price
        - α = 2 / (N + 1) (Smoothing factor)
        - N  = Number of periods
        - EMA_{t-1} = Previous EMA value
        """
        try:
            if not self.Calculate():
                raise ValueError("Calculation Failed!")

            if self.calc_meth.lower() not in self.whereToApply:
                raise ValueError("Enter Correct price input to calculate EMA.")

            # EMA is kind of a Recursive FUnction So I have To make a recursive Function in order to calculate the EMA.
            # OR We can use pandas.dataFrame.ewm method to easily do the job.

            self.EMA_ = (
                self.data[f"Calc_Price"]
                .ewm(span=self.period, adjust=False)
                .mean()
                .iloc[-1]
            )

            return self.EMA_
        except Exception as e:
            print(e)
            return False

    def WMA(self) -> bool:
        """
        WMA(prices: list, period: int) -> bool
        Calculates the Weighted Moving Average (WMA).

        Formula:
        WMA = (P1 * W1 + P2 * W2 + ... + Pn * Wn) / (W1 + W2 + ... + Wn)

        Where:
        - Pn = Price at period n
        - Wn = Weight at period n (Wn = n for recent price emphasis)
        - N  = Number of periods
        """
        try:
            if not self.Calculate():
                raise ValueError("Calculation Failed!")

            if self.calc_meth.lower() not in self.whereToApply:
                raise ValueError("Enter Correct calculator method to calculate EMA. ")

            # Calculate WMA for the shorter Data
            tmp_short = dict()
            counter = self.period

            for i in range(self.period - 1, 0, -1):
                tmp_short[counter] = self.data[f"Calc_Price"].iloc[i] * counter
                counter -= 1

            self.WMA_ = (
                np.array(list(tmp_short.values())).sum()
                + self.data[f"Calc_Price"].iloc[0]
            ) / (np.array(list(tmp_short.keys())).sum() + 1)

            return self.WMA_
        except Exception as e:
            print(e)
            return False

    def VWMA(self) -> bool:
        try:
            if not self.Calculate():
                raise ValueError("Calculation Failed!")

            if self.calc_meth.lower() not in self.whereToApply:
                raise ValueError("Enter Correct calculator method to calculate EMA. ")

            # Calculate WMA for the shorter Data
            tmp_short = dict()

            for i in range(self.period - 1, 0, -1):

                tmp_short[self.data[f"tick_volume"].iloc[i]] = (
                    self.data[f"Calc_Price"].iloc[i] * self.data[f"tick_volume"].iloc[i]
                )

            self.VWMA_ = (
                np.array(list(tmp_short.values())).sum()
                + self.data[f"Calc_Price"].iloc[0] * self.data[f"tick_volume"].iloc[0]
            ) / (np.array(list(tmp_short.keys())).sum() + 1)

            return self.VWMA_
        except Exception as e:
            print(e)
            return False
