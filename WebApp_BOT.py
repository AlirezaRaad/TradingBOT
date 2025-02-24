import streamlit as st
import sqlite3 as sql
from TradinBot import TradingBot


def TheBot():

    st.header("Raad Algoritmic TradingBot", divider="rainbow")
    # Initialize session state for step tracking
    if "step" not in st.session_state:
        st.session_state.step = 1

    if "changed_flag" not in st.session_state:
        st.session_state.changed_flag = None

    if "start_trading" not in st.session_state:
        st.session_state.start_trading = (
            False  # Controls whether to start the bot or no.
        )

    if "allUserTypedData" not in st.session_state:
        st.session_state.allUserTypedData = {}
        # Makes a Dictionary to store information of user to give to the bot

    if "lock_inputs" not in st.session_state:
        st.session_state.lock_inputs = False
        # Controls whether inputs are locked or not. Further I only add the changes to allUserTypedData dict if only this is false.
        # I used not statement to make it True and then add to the dict. If this get true no other changes can happen to the dict.
        # Maybe User can change something but in the backend It wont change.

    # Function to go forward
    def next_step():
        st.session_state.step += 1

    # Function to go backward
    def prev_step():
        st.session_state.step -= 1

    def confirm_change():
        """
        In step 6 I implement a way to go to the desire step and change the info. This function will return the user back to step 6.
        """
        st.session_state.update(step=3)
        st.session_state.changed_flag = False

    def confirm_and_lock():
        """Locks all input fields once the user confirms their credentials."""
        st.session_state.lock_inputs = True

    # Display different content based on the current step

    # -------------------START | SELECT INSTRUMENT-----------------------------#
    if st.session_state.step == 1:

        st.header("SELECT INSTRUMENT")

        user_symbol = st.selectbox(
            "Pick a INSTRUMENT:",
            list(sorted(st.session_state.tb.available_symbols)),
            index=list(sorted(st.session_state.tb.available_symbols)).index("EURUSD"),
            disabled=st.session_state.lock_inputs,
        )

        # if lock_input is False, add the symbol to the dict.
        if not st.session_state.lock_inputs:
            st.session_state.allUserTypedData["symbol"] = user_symbol

        col1, col2 = st.columns(2)
        with col1:
            st.button("Previous Step", on_click=prev_step)
        with col2:
            st.button("Next Step", on_click=next_step)

        if st.session_state.changed_flag is True:
            st.button("Confirm Change", on_click=confirm_change)
            # this button only shows itself when in the last step user comes to this step.
    # -------------------END | SELECT INSTRUMENT-----------------------------#

    # -------------------START | SELECT STRATEGY-----------------------------#
    elif st.session_state.step == 2:

        st.header("SELECT STRATEGY AND ITS KIND")

        options = {"MA Models": ["SMA", "EMA", "WMA", "VWMA"]}

        # First dropdown: Select Strategy
        category = st.selectbox(
            "Select a category:",
            list(options.keys()),
            disabled=st.session_state.lock_inputs,
        )

        # Second dropdown: Depends on first selection
        sub_item = st.selectbox(
            "Select an Calculation Strategy:",
            options[category],
            disabled=st.session_state.lock_inputs,
        )

        st.markdown(
            f"""<b><p style="font-size:22px">You selected: <font color='blue'>{category}</font> with <font color='crimson'>{sub_item}</font> as its calculation method.</p></b>
                
                """,
            unsafe_allow_html=True,
        )

        # if lock_input is False, add the strategy and kind to the dict.
        if not st.session_state.lock_inputs:
            st.session_state.allUserTypedData["strategy"] = {
                "tool": category,
                "kind": sub_item,
            }

        col1, col2 = st.columns(2)
        with col1:
            st.button("Previous Step", on_click=prev_step)
        with col2:
            st.button("Next Step", on_click=next_step)

        if st.session_state.changed_flag is True:
            st.button("Confirm Change", on_click=confirm_change)
            # this button only shows itself when in the last step user comes to this step.
    # -------------------END | SELECT STRATEGY-----------------------------#

    elif st.session_state.step == 3:

        st.header("Confirmation")

        st.markdown(
            f"""<b><p style="font-size:22px">
        1. Instrument : {st.session_state.allUserTypedData["symbol"]}</br>
        2. Strategy : {st.session_state.allUserTypedData['strategy']["tool"]} with {st.session_state.allUserTypedData['strategy']["kind"]}</br>
        </br></p></b>""",
            unsafe_allow_html=True,
        )

        # Initialize session state for checkboxes
        if "yes_checked" not in st.session_state:
            st.session_state.yes_checked = False
        if "no_checked" not in st.session_state:
            st.session_state.no_checked = False

        # Function to update checkbox state
        def update_yes():
            st.session_state.yes_checked = not st.session_state.yes_checked
            if st.session_state.yes_checked:
                st.session_state.no_checked = False  # Uncheck "No"

        def update_no():
            st.session_state.no_checked = not st.session_state.no_checked
            if st.session_state.no_checked:
                st.session_state.yes_checked = False  # Uncheck "Yes"

        # UserLastQuestion : Keeps Track on What checkbox user ticked.
        UserLastQuestion = (
            "Yes"
            if st.session_state.yes_checked
            else "No" if st.session_state.no_checked else "None"
        )

        st.markdown(
            f"""<font color='hotpink'><b><p style="font-size:22px">Do you want to proceed or you want to change things? </p></b></font>""",
            unsafe_allow_html=True,
        )

        # Create yes/no checkboxes.
        yes = st.checkbox(
            "Yes", value=st.session_state.yes_checked, on_change=update_yes
        )
        no = st.checkbox("No", value=st.session_state.no_checked, on_change=update_no)

        if UserLastQuestion == "Yes":
            confirm_and_lock()  # immediately disable inputs
            st.session_state.start_trading = True  # start the robot process.

        elif UserLastQuestion == "No":

            st.markdown(
                f"""<b><p style="font-size:22px">Do you want to proceed and Run the bot with your information or you want to change things? </p></b>""",
                unsafe_allow_html=True,
            )

            allTheStepsdict = {
                "Selecting INSTRUMENT": 1,
                "Selecting STRATEGY and its KIND": 2,
            }

            st.markdown(
                f"""<font color='crismon'><b><p style="font-size:22px">Select a step to return to :</p></b></font>""",
                unsafe_allow_html=True,
            )
            user_step_to_return = st.selectbox("", options=list(allTheStepsdict.keys()))

            st.markdown(
                f"""<font color='crismon'><b><p style="font-size:22px">Click button bellow to go to your desired step.</p></b></font>""",
                unsafe_allow_html=True,
            )

            if st.button("Click"):
                st.session_state.step = allTheStepsdict[user_step_to_return]

                st.session_state.changed_flag = True
                # Gets User Back to desired step.

    if st.session_state.start_trading:

        st.header("Bot", divider="rainbow")
        # TODO: : REMEMBER TO IMPLEMENT GETTING VOLUME FROM USER OUTSIDE OF THE IFS TO NOT CONSTANTLY GET THE COLUMN IN EVERY IF.

        # Instantiate The bot to start Trading.
        if st.session_state.allUserTypedData["strategy"]["tool"] == "MA Models":

            if "bot_input" not in st.session_state:
                st.session_state.bot_input = False
            # For locking the timeFrame/atrMultiplier/RR if user clicked a button. + Price Calculation and short/long periods.

            col_price_cal_meth = st.selectbox(
                "Select Price Calculation Method:",
                list(
                    {
                        "close",
                        "open",
                        "high",
                        "low",
                        "median",
                        "typical",
                        "weighted",
                    }
                ),
                disabled=st.session_state.bot_input,
            )

            spCol, lpCol = st.columns(2)  # Short Period, LongPeriod

            increase_value_of_slider = st.checkbox(
                "Check Me if you want to increase max value of Shorter and Longer period to 99999"
            )
            with spCol:
                shorterPeriodBar = st.slider(
                    "Chose the shorter period For Moving Average",
                    min_value=1,
                    max_value=99999 if increase_value_of_slider else 50,
                    disabled=st.session_state.bot_input,
                )
            with lpCol:
                longererPeriodBar = st.slider(
                    "Chose the Longer period For Moving Average",
                    min_value=shorterPeriodBar + 1,
                    max_value=99999 if increase_value_of_slider else 200,
                    disabled=st.session_state.bot_input,
                )
            # Ask User For the DesireTime Frame.
            from MovingAverage import MovingAverage as mv

            timeFrames = mv.alltimeframes()

            user_time_frame = st.selectbox(
                "Select Your TimeFrame:",
                timeFrames,
                disabled=st.session_state.bot_input,
            )
            try:
                bot_check_box = False
                coll_atr_period, col_atr, col_rr = st.columns(3)

                with coll_atr_period:
                    user_atr_period = st.number_input(
                        "Enter your ATR period:",
                        min_value=shorterPeriodBar,
                        max_value=longererPeriodBar,
                        disabled=st.session_state.bot_input,
                    )

                with col_atr:
                    user_atr = st.number_input(
                        "Enter your ATR multiplier:",
                        disabled=st.session_state.bot_input,
                    )
                with col_rr:
                    user_rr = st.number_input(
                        "Enter your desired R/R :",
                        disabled=st.session_state.bot_input,
                    )
                if user_atr_period == 0 or user_rr == 0 or user_atr == 0:
                    raise ValueError
            except:
                st.info(
                    "The ATR PERIOD SHOULD NOT BE LESSER THAT MV SHORTER PERIOD AND LARGER THAT MV LONGER PERIOD."
                )
                st.info("The ATR Multiplier and R/R Should not be ZERO!")

            try:
                iteration_order = int(
                    st.number_input(
                        "Please Enter The Number of trades that you want The bot to make!",
                        disabled=st.session_state.bot_input,
                    )
                )

                user_trade_volume = st.number_input(
                    f"Please enter the volume lats that you want to trade in :"
                )

                bot_check_box = st.checkbox("Confirm and Start The Bot")
            except:
                st.info("Please Enter an integer Number")

            if bot_check_box and (
                longererPeriodBar
                and shorterPeriodBar
                and user_time_frame
                and col_price_cal_meth
                and user_atr
                and user_rr
            ):
                st.session_state.bot_input = True
                st.success("Bot is running")

                for num_trade in range(1, iteration_order + 1):

                    ordr_places_buy_bot = st.session_state.tb.MovingAverage(
                        symbol=st.session_state.allUserTypedData["symbol"],
                        nLongCandle=longererPeriodBar,
                        nShortCandle=shorterPeriodBar,
                        timeFrame=user_time_frame,
                        kind=st.session_state.allUserTypedData["strategy"]["kind"],
                        applyWhere=col_price_cal_meth,
                        atrMultiplier=user_atr,
                        RR=user_rr,
                        atrWindow=user_atr_period,
                        volume=user_trade_volume,
                    )

                    if ordr_places_buy_bot == 1:
                        st.success(f"✅ {num_trade} : BUY Order Placed!")

                    elif ordr_places_buy_bot == -1:
                        st.success(f"✅ {num_trade} : SELL Order Placed!")

            else:
                st.error("PLEASE ENTER VALID VALUES THEN CHECK THE BOX")
