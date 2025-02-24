import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import datetime as dt
import sqlite3 as sql
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

    available_symbols = set()

    def __init__(self, username, password, server):
        self._user_name_ = username
        self._pass_word_ = password
        self._ser_ver_ = server
        if not self.connect():
            raise ValueError("Enter Correct Credentials")
        TradingBot.FetchAllAvailableSymbols()
        self.sql_db_name = f"BuySellHistory_{username}.db"
        self.SqlDbMaker()

    @classmethod
    def FetchAllAvailableSymbols(cls):
        """
        Fetch All symbols that the brokers has and pour the name of them into TradingBot.available_symbols
        """
        try:
            symbols = mt5.symbols_get()
            for i in range(len(symbols)):
                cls.available_symbols.add(symbols[i].name)
            return True
        except:
            return False

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
        kind: Literal["SMA", "EMA", "WMA", "VWMA"],
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
        atrMultiplier: float = 1.5,
        RR: float = 2.0,
    ):
        """
        timeFrame : MA Time Frame

        nShortCandle : Number Of Candles With You Selected in shorterTf.
        nLongCandle : Number Of Candles With You Selected in longerTf.

        example:
        \tnShortCandle = 50 & nLongCandle = 200 & timeFrame 10 minutes -> bring 50 of most recent 10min bars data for shorter MA and bring 200 of most recent 10min bars for the longer MA.
        ------------------------
        atrMultiplier -> The number that will be multiplied by ATR in order to set sl/tp. (atrMultiplier * atr)
        RR -> Risk/Reward ratio. Default Value is 2.0 which means (atrMultiplier * atr) * RR for the profits.

        ------------------------
        return 1 if BUY order executed and returns -1 When Sell Order executed.
        """
        from MovingAverage import MovingAverage

        if kind not in MovingAverage.AllMAs():
            raise TypeError("Please Provide The CORRECT MA METHOD.")
        if symbol not in TradingBot.available_symbols:
            raise TypeError("Please Provide The SYMBOL That your Broker has.")

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

        self.BuyOrder(
            obj=longerMovingAverage,
            symbol=symbol,
        )

        while True:

            # Calculate new values
            new_shorter = shorterMA()
            new_longer = longerMA()

            shorter_ma.append(new_shorter)
            longer_ma.append(new_longer)

            # Check for Golden Cross
            if len(shorter_ma) == 2:

                while True:
                    # If we have an open Position, do now check and go for another one. Prevent to open Two Positions.
                    if len(mt5.positions_get()) != 0:
                        break

                if shorter_ma[0] < longer_ma[0] and shorter_ma[1] > longer_ma[1]:
                    print("BUY signal detected!")
                    self.BuyOrder(
                        obj=longerMovingAverage,
                        symbol=symbol,
                        atrMult=atrMultiplier,
                        RR=RR,
                    )
                    print("BUY Order Executed!")
                    return 1

                # Check for Death Cross
                elif shorter_ma[0] > longer_ma[0] and shorter_ma[1] < longer_ma[1]:
                    print("SELL signal detected!")
                    self.SellOrder(
                        obj=longerMovingAverage,
                        symbol=symbol,
                        atrMult=atrMultiplier,
                        RR=RR,
                    )
                    print("SELL Order Executed!")
                    return -1

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

    @staticmethod
    def AtrForBuySell(obj, window=14):
        """
        Calculate ATR and return the ATR value.
        """

        df = obj.data.copy()
        df["high-low"] = df["high"] - df["low"]
        df["high-close"] = np.abs(df["high"] - df["close"].shift(1))
        df["low-close"] = np.abs(df["low"] - df["close"].shift(1))
        df["tr"] = df[["high-low", "high-close", "low-close"]].max(axis=1)
        atr = df["tr"].rolling(window).mean().iloc[-1]  # 14-period ATR

        return atr

    def BuyOrder(self, obj, symbol, atrWindow=14, atrMult: float = 1.5, RR: float = 2):
        price = mt5.symbol_info_tick(symbol).ask

        atr = TradingBot.AtrForBuySell(obj=obj, window=atrWindow)

        sl = price - atrMult * atr
        tp = price + atrMult * RR * atr

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": 0.01,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": sl,
            "tp": tp,
            "comment": "python script BUY",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        mt5.order_send(request)
        self.buysell_cursor.execute(
            f"""INSERT INTO orders (Time ,Symbol ,Price ,SL ,TP ,Volume, Type, Strategy)
                  VALUES (?,?,?,?,?,?,?,?)""",
            (
                str(dt.datetime.now()),
                symbol,
                price,
                tp,
                sl,
                0.01,
                "BUY",
                "MA CrossOver",
            ),
        )
        self.conn_to_buysell.commit()
        self.AllPlacedOrders()
        return f"BUY Order Set:\n\tSymbol : {symbol}\n\tPrice : {price} | TP : {tp} | SL : {sl} | Vol : {0.01}\n\tTime of execution {str(dt.datetime.now())} | Strategy : MA CrossOver"

    def SellOrder(self, obj, symbol, atrWindow=14, atrMult: float = 1.5, RR: float = 2):

        price = mt5.symbol_info_tick(symbol).bid

        atr = TradingBot.AtrForBuySell(obj=obj, window=atrWindow)

        sl = price + atrMult * atr
        tp = price - atrMult * RR * atr

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": 0.01,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": sl,
            "tp": tp,
            "comment": "python script SELL",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        mt5.order_send(request)
        self.buysell_cursor.execute(
            f"""INSERT INTO orders (Time ,Symbol ,Price ,SL ,TP ,Volume, Type, Strategy)
                  VALUES (?,?,?,?,?,?,?,?)""",
            (
                str(dt.datetime.now()),
                symbol,
                price,
                tp,
                sl,
                0.01,
                "SELL",
                "MA CrossOver",
            ),
        )
        self.conn_to_buysell.commit()
        self.AllPlacedOrders()
        return f"Sell Order Set:\n\tSymbol : {symbol}\n\tPrice : {price} | TP : {tp} | SL : {sl} | Vol : {0.01}\n\tTime of execution {str(dt.datetime.now())} | Strategy : MA CrossOver"

    def AllPlacedOrders(self) -> pd.DataFrame:
        """
        returns a pandas DataFrame of all placed Orders Using This Bot.
        if you Dont provide any variable, it just updates the list.
        """
        self.all_orders = pd.read_sql("SELECT * FROM orders", self.conn_to_buysell)
        return self.all_orders

    def SqlDbMaker(self):
        """
        Makes a sql database with sqlite and returns True.
        Returns Value Error with custom message if it Failed.
        """
        try:
            self.conn_to_buysell = sql.connect(
                self.sql_db_name, check_same_thread=False
            )
            self.buysell_cursor = self.conn_to_buysell.cursor()
            self.buysell_cursor.execute(
                """CREATE TABLE IF NOT EXISTS orders (
                            Time nvarchar(26) PRIMARY KEY,
                            Symbol nvarchar(10),
                            Price float,
                            SL float,
                            TP float,
                            Volume float,
                            Type char(4),
                            Strategy nvarchar(50))
            """
            )
            return True
        except:
            return ValueError("Sql database making has faces Errors.")

    def __repr__(self):
        return f"TradingBot(username={self.username}, password={self.password}, server={self.server})"
