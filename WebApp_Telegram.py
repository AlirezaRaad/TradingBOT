import streamlit as st
import subprocess
import os

st.header("Telegram Bot Implementation", divider="rainbow")


def Telegram_bot():
    if "telegram_bot" not in st.session_state:
        st.session_state.telegram_bot = None

    if "lock_telegram_api_input" not in st.session_state:
        st.session_state.lock_telegram_api_input = False
    try:
        # Fetching UserId to open the user database
        user_id = st.session_state.tb.username

        tel_api = st.text_input(
            "Enter your Telegram Bot API Token:",
            type="password",
            disabled=st.session_state.lock_telegram_api_input,
        )

        # Start Bot Button
        if st.button("Start Telegram Bot"):
            if tel_api:

                # Kill any previous Bot if its running.
                if st.session_state.telegram_bot:
                    st.session_state.telegram_bot.kill()

                # Make a new instance of bot and run it
                venv_python = os.path.join(r"simpleTS\Scripts\python.exe")
                try:
                    st.session_state.telegram_bot = subprocess.run(
                        [
                            venv_python,
                            "TelegramBot.py",
                            tel_api,
                            str(user_id),
                        ],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    # st.session_state.telegram_bot.run()
                    st.success("Bot started successfully!")
                    st.session_state.lock_telegram_api_input = True
                except:
                    st.error("Please Enter Valid TOKEN")

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
