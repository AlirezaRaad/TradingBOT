import streamlit as st
from WebApp_Home import Home as web_home

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
        ["Home", "About Strategies", "Run The Bot", "Connect To Telegram"],
    )

    st.header("***Version ?***", help="Current Version : 1.0.0")


# Define different pages
def Home():
    web_home()


def About_Strategies():
    pass


def Telegram_Connection():
    pass


def RunTheBot():
    pass


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
