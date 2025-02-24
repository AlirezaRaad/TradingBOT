""""
This Bot is in sync with the other bot when is active and sends notification into telegram bot or channel if you make it admin.
This Bot automatically READ sql database to see if any new order is added or no. if a new order is added, send it through Telegram.
"""

import sqlite3 as sql
import telebot
import os
import datetime as dt
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from infos import TelAPI


bot = telebot.TeleBot(TelAPI)

userID = 11008730
user_sql_database_path = os.path.join(os.getcwd(), "BuySellHistory", f"{userID}.db")
user_sql_conn = sql.connect(user_sql_database_path, check_same_thread=False)
user_sql_cursor = user_sql_conn.cursor()


# --------------------------------------------------#
user_sql_cursor.execute("SELECT Time FROM orders ORDER BY Time DESC LIMIT 1")
last_trade = user_sql_cursor.fetchone()[
    0
]  # Gets the date of last trade and I tested that it only be executed 1 time.
last_trade_date = dt.datetime.strptime(last_trade, "%Y-%m-%d %H:%M:%S.%f")


def CheckTheDB():
    global last_trade_date, msg_id
    while True:
        user_sql_cursor.execute("SELECT Time FROM orders ORDER BY Time DESC LIMIT 1")
        last_trade_2 = user_sql_cursor.fetchone()[0]
        last_trade_date_2 = dt.datetime.strptime(last_trade_2, "%Y-%m-%d %H:%M:%S.%f")
        if last_trade_date_2 > last_trade_date:
            last_trade_date = last_trade_date_2
            bot.send_message(
                msg_id,
                "ORDER HAS BEEN EXECUTED.",
            )


# --------------------------------------------------#


def start_custom_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)  # Resize to fit smaller screens
    markup.row(KeyboardButton("/description"))

    return markup


@bot.message_handler(commands=["start"])
def send_start(message):
    bot.send_message(
        message.chat.id,
        "Welcome to @RaadRsume bot. RaadLearn.com.",
        reply_markup=start_custom_keyboard(),
    )
    global msg_id
    msg_id = message.chat.id


@bot.message_handler(commands=["description"])
def send_start(message):
    bot.send_message(
        message.chat.id,
        f"This Bot will Sends You message when a order has been set., {user_sql_database_path}",
    )
    CheckTheDB()


bot.polling()
