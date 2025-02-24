import streamlit as st
import MetaTrader5 as mt5


def Tr_hist():
    st.header("""Trading History""", divider="rainbow")
    st.info("NOTE that this is the history for orders which has been place via BOT. ")
    st.dataframe(st.session_state.tb.AllPlacedOrders())
