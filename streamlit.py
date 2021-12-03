import streamlit as st

import datetime
import time
import matplotlib.pyplot as plt

# own functions
import data_retriever as dr
import data_treatment as dt


# Retrieve currencies and make a list
currencies = dr.retrieve_currencies()

st.set_page_config(
    page_title="This is a cool app",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Header content for the webpage
st.header("Amazing Python Project")
st.subheader("Created by amazing people")

# Introduction to the product and how to use it

# Sidebar configuration
with st.sidebar:

    st.title("Filters")
    "\n"

    # Cryptocurrency selection
    selected_currency = st.selectbox("Select a cryptocurrency", currencies)
    "\n"

    # Defining the period interval
    today = datetime.date.today()
    last_month = today - datetime.timedelta(days=31)
    start_date = st.date_input('Start date', last_month)
    end_date = st.date_input('End date', today)

    if start_date < end_date:
        pass
    else:
        st.error('Error: The End date must come after the Start date.')
        "\n"

    # Defining the number of runs
    n = st.slider('How many times do you want to run the model?', 10, 1000)
    st.caption(
        'Note: The more times you run the model, the more accurate the results are.')
    "\n"

# Progress status
with st.spinner('Loading...'):
    time.sleep(1)

returns = dr.get_market_data(selected_currency, str(start_date), str(end_date))

sigma, mu, result, return_list = dt.garch(returns)

dt.garch_volatility(
    result, selected_currency, str(start_date), str(end_date))

monte_carlo = dt.monte_carlo_simulation(
    return_list, mu, sigma, n, selected_currency)

dt.density_plot(monte_carlo, n, selected_currency)

# Footer content for the webpage
st.markdown(
    "Created by Enrique Fabio Ferrari-Pedruzzi, Gianluca Pecoraro, Sigurd Koldste & Vera Mendes as part of an Introduction to Programming project at [Nova School of Business and Economics](https://novasbe.pt/).")
st.markdown(
    "*Find the full source code [on GitHub](https://github.com/skrunsky/python-project).*")
