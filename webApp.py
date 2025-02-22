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

st.header("Now Lets make our Bot", divider="rainbow")

# Initialize session state for step tracking
if "step" not in st.session_state:
    st.session_state.step = 1


if "changed_flag" not in st.session_state:
    st.session_state.changed_flag = None

if "start_trading" not in st.session_state:
    st.session_state.start_trading = False  # Controls whether to start the bot or no.

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
    st.session_state.update(step=6)
    st.session_state.changed_flag = False


def confirm_and_lock():
    """Locks all input fields once the user confirms their credentials."""
    st.session_state.lock_inputs = True


# Display different content based on the current step

# -------------------START | LOG IN-----------------------------#
if st.session_state.step == 1:

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
            disabled=st.session_state.lock_inputs,
        )
    with passwordCol:
        user_password = st.text_input(
            "Enter your password:",
            key="USER_password",
            type="password",
            disabled=st.session_state.lock_inputs,
        )

    user_server = st.text_input(
        "Enter your server:",
        key="USER_server",
        type="default",
        disabled=st.session_state.lock_inputs,
    )

    confirmedCredential = st.checkbox("Confirm and Lock Inputs to see next Step.")

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

            st.button("Next", on_click=next_step)

        except:
            st.markdown(
                """<font color='yellow'><b><p style="font-size:22px">PLEASE ENTER CORRECT CREDENTIALS.</p></b></font>""",
                unsafe_allow_html=True,
            )

# -------------------END | LOG IN-----------------------------#

# -------------------START | SELECT INSTRUMENT-----------------------------#
elif st.session_state.step == 2:

    st.header("SELECT INSTRUMENT")

    user_symbol = st.selectbox(
        "Pick a INSTRUMENT:",
        list(st.session_state.tb.available_symbols),
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

# -------------------START | SELECT PRICE CALCULATION-----------------------------#
elif st.session_state.step == 3:

    st.header("SELECT HOW YOU WANT TO CALCULATE PRICE THAT WITH USE IN MOVING AVERAGES")

    user_calc_method = st.selectbox(
        "Pick a INSTRUMENT:",
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
        disabled=st.session_state.lock_inputs,
    )
    # disabled=st.session_state.lock_inputs=False in the first implementation, but if lock_inputs get True Value in step 6,
    # you cannot change this.

    # if lock_input is False, add the calculation method to the dict.
    if not st.session_state.lock_inputs:
        st.session_state.allUserTypedData["calc_meth"] = user_calc_method

    col1, col2 = st.columns(2)
    with col1:
        st.button("Previous Step", on_click=prev_step)
    with col2:
        st.button("Next Step", on_click=next_step)
    if st.session_state.changed_flag is True:
        st.button("Confirm Change", on_click=confirm_change)
        # this button only shows itself when in the last step user comes to this step.
# -------------------END | SELECT PRICE CALCULATION-----------------------------#

# -------------------START | SELECT STRATEGY-----------------------------#
elif st.session_state.step == 4:

    st.header("SELECT STRATEGY AND ITS KIND")

    options = {"MA CrossOvers": ["SMA", "EMA", "WMA", "VWMA"]}

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

# -------------------START | SELECTING THE PERIOD OF MOVING AVERAGES--------------------------------------#
elif st.session_state.step == 5:

    st.header("SELECTING THE PERIODS")
    increase_value_of_slider = st.checkbox(
        "Check Me if you want to increase max value of Shorter and Longer period to 99999"
    )
    spCol, lpCol = st.columns(2)  # Short Period, LongPeriod

    with spCol:
        shorterPeriodBar = st.slider(
            "Chose the shorter period For Moving Average",
            min_value=1,
            max_value=99999 if increase_value_of_slider else 50,
            disabled=st.session_state.lock_inputs,
        )
    with lpCol:
        longererPeriodBar = st.slider(
            "Chose the Longer period For Moving Average",
            min_value=shorterPeriodBar + 1,
            max_value=99999 if increase_value_of_slider else 200,
            disabled=st.session_state.lock_inputs,
        )

    # if lock_input is False, add the shorter and longer period to the dict.
    if not st.session_state.lock_inputs:
        st.session_state.allUserTypedData["periods"] = {
            "long": longererPeriodBar,
            "short": shorterPeriodBar,
        }

    col1, col2 = st.columns(2)
    with col1:
        st.button("Previous Step", on_click=prev_step)
    with col2:
        st.button("Next Step", on_click=next_step)

    if st.session_state.changed_flag is True:
        st.button("Confirm Change", on_click=confirm_change)
        # this button only shows itself when in the last step user comes to this step.

# -------------------END | SELECTING THE PERIOD OF MOVING AVERAGES--------------------------------------#

elif st.session_state.step == 6:

    st.header("Confirmation")

    st.markdown(
        f"""<b><p style="font-size:22px">
    1. Instrument : {st.session_state.allUserTypedData["symbol"]}</br>
    2. Price Calculation method : {st.session_state.allUserTypedData["calc_meth"]}</br>
    3. Strategy : {st.session_state.allUserTypedData['strategy']["tool"]} with {st.session_state.allUserTypedData['strategy']["kind"]}</br>
    4. Periods : Short = {st.session_state.allUserTypedData["periods"]["short"]}, Long = {st.session_state.allUserTypedData["periods"]["long"]}</br></p></b>""",
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
        f"""<font color='hotpink'><b><p style="font-size:22px">Do you want to proceed and Run the bot with your information or you want to change things? </p></b></font>""",
        unsafe_allow_html=True,
    )

    # Create yes/no checkboxes.
    yes = st.checkbox("Yes", value=st.session_state.yes_checked, on_change=update_yes)
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
            "Selecting INSTRUMENT": 2,
            "Selecting how to CALCULATE PRICE": 3,
            "Selecting STRATEGY and its KIND": 4,
            "Selecting the PERIODS": 5,
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

    st.header("Running The Bot", divider="rainbow")

    st.session_state.allUserTypedData

    if st.session_state.allUserTypedData["strategy"]["tool"] == "MA CrossOvers":
        st.session_state.tb.MovingAverage(
            symbol=st.session_state.allUserTypedData["symbol"],
            nLongCandle=st.session_state.allUserTypedData["period"]["long"],
            nShortCandle=st.session_state.allUserTypedData["period"]["short"],
            timeFrame="1 minute",
            kind=["strategy"]["kind"],
            applyWhere=st.session_state.allUserTypedData["calc_meth"],
            atrMultiplier=1.5,
            RR=2,
        )

    st.markdown(
        f"""<b><p style="font-size:25px">Bot is running!!""",
        unsafe_allow_html=True,
    )
