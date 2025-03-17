import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from bot.TradinBot import TradingBot

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.getcwd()), ".env"))

if os.environ["MT5_USERNAME"]:
    user_username = os.environ.get("MT5_USERNAME")
if os.environ["MT5_PASSWORD"]:
    user_password = os.environ.get("MT5_PASSWORD")
if os.environ["MT5_SERVER"]:
    user_server = os.environ.get("MT5_SERVER")


def ConnectToMT5():
    if "lock_inputs_acc" not in st.session_state:
        st.session_state.lock_inputs_acc = False

    st.header("""Connect To Your MT5 Account!""", divider="rainbow")

    st.header("Enter Your Credential.")
    st.markdown(
        """<b><p style="font-size:22px">
        Enter you username/password and the server which you are connect with in mt5 app.</br>
        <font color='orange'>YOU can find your credentials under Tools -> Options -> Server</font>
        </p></b>

    """,
        unsafe_allow_html=True,
    )

    # Create 2 column to get Username/Password and 1 for Server in a separate boc
    usernameCol, passwordCol = st.columns(
        spec=2, vertical_alignment="center", gap="large"
    )

    with usernameCol:
        user_username = st.text_input(
            "Enter your username:",
            key="USER_username",
            type="default",
            disabled=st.session_state.lock_inputs_acc,
        )
    with passwordCol:
        user_password = st.text_input(
            "Enter your password:",
            key="USER_password",
            type="password",
            disabled=st.session_state.lock_inputs_acc,
        )

    user_server = st.text_input(
        "Enter your server:",
        key="USER_server",
        type="default",
        disabled=st.session_state.lock_inputs_acc,
    )

    confirmedCredential = st.checkbox("Confirm and Lock Inputs.")

    # If the program was able to login to mt5 using the credentials, it will go to the next step.
    if confirmedCredential:
        try:
            st.session_state.tb = TradingBot(
                username=int(user_username),
                password=user_password,
                server=user_server,
            )
            st.session_state.tb.connect()

            st.session_state.allUserTypedData["credentials"] = {
                "username": user_username,
                "password": user_password,
                "server": user_server,
            }

            st.markdown(
                """<font color='aqua'><b><p style="font-size:22px">CONNECTION SUCCESSFUL. NOW YOU CAN USE OTHER FEATURES.</p></b></font>""",
                unsafe_allow_html=True,
            )
            st.session_state.lock_inputs_acc = True
        except:
            st.markdown(
                """<font color='yellow'><b><p style="font-size:22px">PLEASE ENTER CORRECT CREDENTIALS.</p></b></font>""",
                unsafe_allow_html=True,
            )
