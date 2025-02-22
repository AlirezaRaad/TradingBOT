import streamlit as st


def AboutStrat():
    st.header(
        "***Moving Average Crossover (Golden Cross, Death Cross)***", divider="rainbow"
    )
    st.markdown(
        f"""<p style="font-size:25px">Lets See Moving Average Parameters:<br>
        1. <font color='FFA500'>Instrument</font> : The instrument that your Broker does provides and you want to use the BOT on.<br>
        2. <font color='FFA500'>Price Calculation Method</font> : Whit this you will decide how to calculate you price in order to put this price into Moving Averages formulas.<br>
        3. <font color='FFA500'>MA Models</font> : How to calculate the value of Moving Average with the given price.<br>
        4. <font color='FFA500'>Periods</font> : Select the periods for longer and shorter Moving Average.<br>
        5. <font color='FFA500'>Time Frames</font> : Select your desired time frame to trade on.
        6. <font color='FFA500'>ATR</font> : Select the multiplier for ATR to calculate Stop Loss point.
        7. <font color='FFA500'>R/R</font> : Select yor R/R to multiply this number by SL distance to make a Take Profit point.</p>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""<p style="font-size:25px">Lets assume these parameters are selected :<br>
        EURUSD | mean | SMA | 1 minute |short = 50, long = 200 | 1.5 | 2<br><br>
        It mean that the program will select 'EURUSD' as the instrument to TRADE ON.<br>
        It will use mean formula (high + low)/2 to create NEW PRICES.<br>
        First it selects 1 minute as time frame Then it put new prices into SMA formula with short SMA that has 50 period and a long SMA that has 200.<br><br>
        NOW, the BOT will be ready for the Golden Cross, Death Cross signals to trade.<br><br>
        When <font color='FFD700'>Golden Cross</font> Signal generates | SL = price - (atr * multiplier) | TP : price + 2 * (atr * multiplier)<br>
        When <font color='red'>Death Cross</font> Signal generates | SL = price + (atr * multiplier) | TP : price - 2 * (atr * multiplier)</p>""",
        unsafe_allow_html=True,
    )
    st.divider()


if __name__ == "__main__":
    AboutStrat()
