import streamlit as st
from TradinBot import TradingBot

st.header("Raad Algoritmic TradingBot", divider="rainbow")

# -------------------START | CREATING SIDEBAR-------------------#
with st.sidebar:
    st.header("***About Making The App***")
    st.markdown(
        """Hello, I am <font color='lightgreen'><b>Raad</b></font>;<br><br>
        I made this app just to be familiar with the hardships of making a <font color='hotpink'><b>ALGORITHMIC TRADING BOT</b></font>.<br><br>
                Although in version 1.0.0 I implement just a simple moving average crossovers but learnt a lot and I can use this Experience and make better bots in the near future.

""",
        unsafe_allow_html=True,
    )
    st.header(
        "***What will be Added in Future Version?***", help="Current Version : 1.0.0"
    )
    st.markdown(
        """
        :red[NOTE]: these are not in any specific order<br><br>
        1. Machine Learning Based model will be deployed to see if the odds of current BUY/SELL signal profit/loss.If it was profitable place order otherwise do not execute order.<br><br>
        2. Will Add more classic indicators like RSI/MACD/... with their strategies.<br><br>
        

        """,
        unsafe_allow_html=True,
    )

# -------------------END | CREATING SIDEBAR-------------------#
st.markdown(
    """<p style="font-size:20px">
    This <font color='hotpink'><b>ALGORITHMIC TRADING BOT</b></font> will trade based on classic Indicator and their strategies.<br><br>
            In the Version 1.0.0 I just added Moving Average CrossOvers which you can see the details in Selecting Strategy option.<br><br>
            For Seeing what will be added with later updates, see sidebar <font color='red'>'What will be Added in Future Version?'</font> Section
        </p>
""",
    unsafe_allow_html=True,
)
st.header("How it will work", divider="rainbow")
st.markdown(
    """<b><p style="font-size:22px">
    1. You Need to <font color='aqua'>log in</font> into your MetaTrader5 account.<br>
    2. You Need to select the <font color='aqua'>instrument</font> which your broker also provides.<br>
    3. You need to select which <font color='aqua'>price calculation method</font> you want to use.<br>
    4. You Need to Select your <font color='aqua'>Strategies.</font><br>
    5. You Need To Select Which <font color='aqua'>Moving Average formula</font> you want to use.<br>
    6. You just need to select your <font color='aqua'>LONGER/SHORTER period</font> for you.<br>
    </p></b>

""",
    unsafe_allow_html=True,
)
# -------------------START | LOG IN-----------------------------#

st.header("Enter Your Credential.", divider="rainbow")
st.markdown(
    """<b><p style="font-size:22px">
    Enter you username/password and the server which you are connect with in mt5 app.</br>
    <font color='orange'>YOU can find your credentials under Tools -> Options -> Server</font>
    </p></b>

""",
    unsafe_allow_html=True,
)
# Create 2 column to get Username/Password and 1 for Server
usernameCol, passwordCol = st.columns(spec=2, vertical_alignment="center", gap="large")

with usernameCol:
    user_username = st.text_input(
        "Enter your username:",
        key="USER_username",
        type="default",
    )
with passwordCol:
    user_password = st.text_input(
        "Enter your password:", key="USER_password", type="password"
    )


user_server = st.text_input("Enter your server:", key="USER_server", type="default")

confirmedCredential = st.checkbox("Confirm and Lock Inputs")
if confirmedCredential:
    try:
        tb = TradingBot(
            username=int(user_username), password=user_password, server=user_server
        )
        tb.connect()
        confirmedCredential
    except:
        st.markdown(
            """<font color='yellow'><b><p style="font-size:22px">PLEASE ENTER CORRECT CREDENTIALS.</p></b></font>""",
            unsafe_allow_html=True,
        )
# -------------------END | LOG IN-----------------------------#

# -------------------START | SELECT INSTRUMENT-----------------------------#
st.header("SELECT INSTRUMENT", divider="rainbow")
st.selectbox(
    "Pick a fruit:", ["Apple", "Banana", "Cherry"], index=1  # Default to "Banana"
)
# -------------------END | SELECT INSTRUMENT-----------------------------#

# -------------------START | SELECT PRICE CALCULATION-----------------------------#
st.header("SELECT PRICE CALCULATION", divider="rainbow")
# -------------------END | SELECT PRICE CALCULATION-----------------------------#

# -------------------START | SELECT STRATEGY-----------------------------#
st.header("SELECT STRATEGY", divider="rainbow")
# -------------------END | SELECT STRATEGY-----------------------------#

# -------------------START | MOVING AVERAGE KIND-----------------------------#
st.header("MOVING AVERAGE KIND", divider="rainbow")
# -------------------END | MOVING AVERAGE KIND-----------------------------#

# -------------------START | SELECTING THE PERIOD OF MOVING AVERAGES--------------------------------------#
st.header("SELECTING THE PERIODS", divider="rainbow")
increase_value_of_slider = st.checkbox(
    "Check Me if you want to increase max value of Shorter and Longer period to 99999"
)
spCol, lpCol = st.columns(2)  # Short Period, LongPeriod

with spCol:
    st.slider(
        "Chose the shorter period For Moving Average",
        min_value=1,
        max_value=99999 if increase_value_of_slider else 50,
    )
with lpCol:
    st.slider(
        "Chose the Longer period For Moving Average",
        min_value=1,
        max_value=99999 if increase_value_of_slider else 200,
    )
# -------------------END | SELECTING THE PERIOD OF MOVING AVERAGES--------------------------------------#
