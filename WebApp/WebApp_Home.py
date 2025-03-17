import streamlit as st


def Home():
    st.header("Raad Algoritmic TradingBot", divider="rainbow")

    st.markdown(
        f"""<p style="font-size:25px"> Hello, This Is <a href="https://raadlearn.com/">Raad's</a> Algorithmic Trading WorkShop.<br>
        I will pour my programming knowledge into this application to created a good algorithmic BOTs with different strategies, 
        from the basic Moving Average strategies to <b><font color='crimson'>ADVANCE MACHINE LEARNING Models</font></b> for Time Series Analysis. </p>
                """,
        unsafe_allow_html=True,
    )

    st.header("Non-ML Strategies", divider="rainbow")
    st.markdown(
        f"""<p style="font-size:25px">
        1. Moving Average Crossover (Golden Cross, Death Cross)<br>
        2. Bollinger Bands (BB)<br>
        3. Relative Strength Index (RSI)<br>
        4. Momentum Indicator (MOM)<br>
        5. Volume Weighted Average Price (VWAP)<br>
        6. Chaikin Money Flow (CMF)<br></p>""",
        unsafe_allow_html=True,
    )

    st.header("ML Based Models", divider="rainbow")
    st.markdown(
        f"""<p style="font-size:25px">
        1. ARIMA<br>
        2. ARIMAX <br>
        3. ARIMA + ML Hybrid Models <br>
        4. ARIMA + XGBoost Hybrid <br>
        5. LSTM + CNN Hybrid Models<br>
        6. Facebook Prophet + XGBoost Hybrid<br></p>""",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    Home()
