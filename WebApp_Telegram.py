import streamlit as st
import threading
from TelegramBot import start_telegram_bot


def Telegram_bot():
    def run_the_bot():
        if "telegramBOT" not in st.session_state:
            st.session_state.telegramBOT = threading.Thread(
                target=start_telegram_bot, daemon=True
            ).start()

    st.header("Telegram Bot Implementation", divider="rainbow")

    if st.button("🚀 Start Telegram Bot"):
        run_the_bot()
        st.success("Bot started successfully!")

    if st.button("⛔ Stop Telegram Bot"):
        st.warning("Stopping the bot requires restarting the app.")
