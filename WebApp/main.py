import streamlit as st
from Home import Home as web_home
from AboutStrategies import AboutStrat
from MainBOT import TheBot
from TradeHistory import Tr_hist
from ConnectToAccount import ConnectToMT5
from Telegram import Telegram_bot

# -------------------START | CREATING SIDEBAR-------------------#
with st.sidebar:
    st.header("***About Making The App***")
    st.markdown(
        """Hello, I am <font color='lightgreen'><b>Raad</b></font>;<br><br>
        I made this app just to be familiar with the hardships of making a <font color='hotpink'><b>ALGORITHMIC TRADING BOT</b></font>.<br><br>
""",
        unsafe_allow_html=True,
    )

    # Sidebar for navigation
    page = st.sidebar.radio(
        "Navigation to",
        [
            "Home",
            "About Strategies",
            "Connect To MT5",
            "Connect To Telegram",
            "Run The Bot",
            "Trading History",
        ],
    )

    st.header("***Version ?***", help="Current Version : 1.0.0")


# Define different pages
def Home():
    web_home()


def About_Strategies():
    AboutStrat()


def Telegram_Connection():
    Telegram_bot()


def RunTheBot():
    try:
        TheBot()
    except AttributeError:
        st.error("First Connect To Your MT5 Account!")


def TradeHistory():
    try:
        Tr_hist()

    except AttributeError:
        st.error("First Connect To Your MT5 Account!")


def ConnectMT5():
    ConnectToMT5()


# -------------------END | CREATING SIDEBAR-------------------#


# Display the selected page
if page == "Home":
    Home()
elif page == "About Strategies":
    About_Strategies()
elif page == "Run The Bot":
    RunTheBot()
elif page == "Connect To Telegram":
    Telegram_Connection()
elif page == "Trading History":
    TradeHistory()
elif page == "Connect To MT5":
    ConnectMT5()
