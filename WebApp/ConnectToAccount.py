import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from bot.TradinBot import TradingBot


def ConnectToMT5():
    if "lock_inputs_acc" not in st.session_state:
        st.session_state.lock_inputs_acc = False

    # Makes a Dictionary to store information of user to give to the bot
    if "allUserTypedData" not in st.session_state:
        st.session_state.allUserTypedData = {}

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
        except Exception as e:
            print(e)
            st.error("PLEASE ENTER CORRECT CREDENTIALS.")

        else:
            st.success("CONNECTION SUCCESSFUL. NOW YOU CAN USE OTHER FEATURES.")
            st.session_state.lock_inputs_acc = True
