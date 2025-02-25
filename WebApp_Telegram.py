import streamlit as st
import subprocess
import os

st.header("Telegram Bot Implementation", divider="rainbow")


def Telegram_bot():
    if "telegram_bot" not in st.session_state:
        st.session_state.telegram_bot = None

    try:
        # Fetching UserId to open the user database
        user_id = st.session_state.tb.username

        tel_api = st.text_input("Enter your Telegram Bot API Token:", type="password")

        # Start Bot Button
        if st.button("Start Telegram Bot"):
            if tel_api:

                # Kill any previous Bot if its running.
                if st.session_state.telegram_bot:
                    st.session_state.telegram_bot.kill()

                # Make a new instance of bot and run it
                venv_python = os.path.join(r"simpleTS\Scripts\python.exe")
                st.session_state.telegram_bot = subprocess.Popen(
                    [venv_python, "TelegramBot.py", tel_api, str(user_id)]
                )
                st.success("Bot started successfully!")

        if (
            st.session_state.telegram_bot
            and st.session_state.telegram_bot.poll() is None
        ):
            if st.button("Kill The Telegram Bot"):
                st.session_state.telegram_bot.kill()
                st.session_state.telegram_bot = None
                st.success("Bot stopped successfully!")
    except AttributeError:
        st.error("First log in into your Mt5 Account.")
    # except:
    #     st.error("Please Enter Valid Telegram Bot Api Token.")
    st.write(st.session_state.telegram_bot.poll())
    st.write(user_id, tel_api)
