import streamlit as st
import threading
import subprocess
from TelegramBot import start_telegram_bot


def Telegram_bot():
    def run_the_bot():
        if "telegramBOT" not in st.session_state:
            st.session_state.telegramBOT = threading.Thread(
                target=start_telegram_bot, daemon=True
            ).start()

    st.header("Telegram Bot Implementation", divider="rainbow")


# st.session_state.USER_username
tel_api = st.text_input("Enter your Telegram Bot API Token:", type="password")

# Start Bot Button
if st.button("Start Telegram Bot"):
    if tel_api:
        subprocess.Popen(["python", "TelegramBot.py", tel_api, user_id])
        st.success("Bot started successfully!")
    else:
        st.error("Please enter a valid API Token and numeric User ID.")
