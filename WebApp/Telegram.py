import streamlit as st
import subprocess
import os
import threading
from dotenv import load_dotenv

load_dotenv()


def Telegram_bot():
    st.header("Telegram Bot Implementation", divider="rainbow")

    if "telegram_bot" not in st.session_state:
        st.session_state.telegram_bot = None

    # Set a flag to lock the input.
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
            # Kill any previous Bot if its running.
            if st.session_state.telegram_bot:
                st.session_state.telegram_bot = None
            try:
                threading.Thread(
                    target=start_bot, args=(tel_api, user_id), daemon=True
                ).start()
                st.session_state.telegram_bot = True
                st.session_state.lock_telegram_api_input = True
                st.success("Bot started successfully!")
                st.session_state.lock_telegram_api_input = True

            except subprocess.CalledProcessError as e:
                st.write("STDERR:", e.stderr)

                st.error("Please Enter Valid TOKEN")

    # except AttributeError:
    #     st.error("First Log in into your MT5 account")

    except Exception as e:
        st.error("Unexpected ERROR has occurred.")
        st.error(e)


def start_bot(tel_api, user_id):
    venv_python = os.environ["PYTHON_VENV_PATH"]

    subprocess.run(
        [
            venv_python,
            os.path.join("bot", "TelegramBot.py"),
            tel_api,
            str(user_id),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
