import streamlit as st

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
            For Seeing what will be added with later updates, see sidebar :red['What will be Added in Future Version?'] Section
        </p>
""",
    unsafe_allow_html=True,
)
st.header("How it will work", divider="rainbow")
st.markdown(
    """<p style="font-size:20px">
    1. You Need to log in into your MetaTrader5 account.<br>
    2. You Need to select the instrument which your broker also provides.<br>
    3. You Need to Select your Strategies.<br>
    4. You need to select which price calculation method you want to use.<br>
    5.You Need To Select Which Moving Average formula you want to use.<br>
    6. You just need to select your LONGER/SHORTER period for you.<br>
    </p>

""",
    unsafe_allow_html=True,
)
# -------------------START | LOG IN-----------------------------#


# -------------------END | LOG IN-----------------------------#

# -------------------START | SELECTING THE PERIOD OF MOVING AVERAGES--------------------------------------#
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
