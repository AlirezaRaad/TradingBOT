import streamlit as st
from WebApp_Home import Home as web_home
from WebApp_AboutStrategies import AboutStrat
from WebApp_BOT import TheBot
from WebApp_TradeHistory import Tr_hist
from WebApp_ConnectToAccount import ConnectToMT5

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
    pass


def RunTheBot():
    TheBot()


def TradeHistory():
    Tr_hist()


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
