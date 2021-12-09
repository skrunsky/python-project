import streamlit as st

import datetime
import time
import matplotlib.pyplot as plt

# own functions
import data_retriever as dr
import data_treatment as dt


# Retrieve currencies and make a list
currencies = dr.retrieve_currencies()

#Page configuration
st.set_page_config(
    page_title="This is a cool app",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "# GARCH MODEL. This is an *extremely* cool app!"
    }
)

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
  
    


# Header content for the webpage
st.title("Crypto Asset Forecasting")
"\n"
st.subheader("Forecasting one month returns on crypto asset time-series using stochastic volatility models")
"\n"
"\n"

# Introduction to the product 
st.markdown("An approach to estimate volatilities on past data is used. To estimate the forecast probability density, a stochastic volatility model is chosen. A GARCH, ARCH or HARCH model to specify the equity index return process based can be used.") 
st.markdown("Below the annualized conditional **volatility** for the specified timeframe can be observed:")
"\n"
"\n"

returns = dr.get_market_data(selected_currency, str(start_date), str(end_date))

sigma, mu, result, return_list = dt.garch(returns)

dt.garch_volatility(
    result, selected_currency, str(start_date), str(end_date))
"\n"
"\n"
st.markdown("Based on the computed volatilities Engle and Rosenberg (2002) suggest an approach to estimate one month forecasted returns.")
st.markdown(f"Through a Monte Carlo simulation a number of returns ({n}) is simulated that yields a **return density function** as specified below.")
st.markdown("The forecast becomes more accurate the more iterations the user specifies.")
"\n"
"\n"
monte_carlo = dt.monte_carlo_simulation(
    return_list, mu, sigma, n, selected_currency)

dt.density_plot(monte_carlo, n, selected_currency)

st.markdown(f"The on average forecasted return of {selected_currency} over the next month is: ")
st.metric(label="Return", value=f"{mu} %") #CORRECT THIS
"\n"
"\n"
st.markdown("The average return out of the simulated sample resembles the on average most likely return for the next month. Using the density function the user can now get an understanding of the likelihood of the occurrence of a certain return.")
"\n"
"\n"
"\n"

st.balloons()

# Footer content for the webpage
st.markdown(
    "*Created by Enrique Fabio Ferrari-Pedruzzi, Gianluca Pecoraro, Sigurd Koldste & Vera Mendes as part of an Introduction to Programming project at [Nova School of Business and Economics](https://novasbe.pt/).*")
"\n"
st.markdown(
    "*Find the full source code [on GitHub](https://github.com/skrunsky/python-project).*")



