import streamlit as st

import datetime


# own functions
import data_retriever as dr
import data_treatment as dt
import graph_creator as gc

# variables
API_KEY = st.secrets['API_KEY']

# Create objects
data_retriever = dr.DataRetriever(API_KEY)

# Retrieve currencies and make a list
currencies = data_retriever.retrieve_currencies()

# Page configuration
st.set_page_config(
    page_title="Crypto Asset Forecasting",
    page_icon="icon.png",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "Based on Engle and Rosenberg (2002) an approach to estimate one month forecasted returns based on volatilities is applied on Cryptocurrencies. Usually, models that exhibit time-varying volatility and volatility clustering are employed in modelling return time series. To estimate the forecast probability density, a stochastic volatility model, in this case a GARCH, ARCH or HARCH model to specify the equity index return process, can be chosen. *This web app was built using* `streamlit`, `pandas`, `matplotlib`, `numpy`, `stqdm`, `scikit-learn` *&* `arch` *libraries.*"
    }
)

# Sidebar configuration
with st.sidebar:
    col1, col2, col3 = st.columns([0.3, 1, 0.3])
    col2.image("logo.png", use_column_width=True)
    "\n"

    st.title("Options")

    # Cryptocurrency and model selection
    selected_currency = st.selectbox("Select a cryptocurrency", currencies)
    model = st.selectbox("Select a model", ['GARCH', 'ARCH', 'HARCH'])
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

# Initialize the DataTreatment object
data_treatment = dt.DataTreatment(
    data_retriever, model, n, selected_currency, str(start_date), str(end_date))
data_treatment.set_variables()

# Initialize the GraphCreator object
graph_creator = gc.GraphCreator(
    data_treatment, selected_currency, str(start_date), str(end_date))

# Header content for the webpage
st.header("Crypto Asset Forecasting")
st.subheader(
    "Forecasting one month returns on crypto asset time-series using stochastic volatility models")

# Defining columns to use for the layout
col1, col2 = st.columns([1, 3])

with col1:
    graph_creator.show_forecasted_return()

    st.markdown(f"Here, the distribution of possible returns, as **histogram** and as **smoothed density function**, can be observed. Applying a Monte Carlo simulation, {n} possible one-month returns are simulated and plotted.")
    st.markdown("A left-skewed probability distribution would indicate a higher probability for negative one-month expected returns, while a right-skewed distribution would indicate more positive return expectations over the next month.")
    st.markdown("The average of all simulated returns corresponds to the on average most likely to be expected return over the next month.")

with col2:
    graph_creator.density_plot()

st.markdown("---")

col3, col4 = st.columns([3, 1])

with col3:
    graph_creator.volatility_plot()

with col4:
    st.markdown(f"This figure shows the {selected_currency} annualized conditional **volatility** computed with the {model} model. The period from {start_date} to {end_date} is used to forecast volatilities of the next period.") 
    st.markdown("Typically, very high levels of volatility correspond to corrections in the underlying asset. Based on the assumption of volatility clustering, all else held equal, more recent volatilities have a stronger influence on predicted future volatility levels.")

st.markdown("---")

st.markdown(
    "*Created by Enrique Fabio Ferrari-Pedruzzi, Gianluca Pecoraro, Sigurd Koldste & Vera Mendes as part of an Introduction to Programming project at [Nova School of Business and Economics](https://novasbe.pt/).*")
st.markdown("This site does not give financial advice, nor is it an investment advisor. It is just a tool to help you understand the volatility of crypto assets, and is meant for educational and demonstration purposes only.")
st.markdown("For further insights check the **About** item in the menu.")
st.markdown(
    "*Find the full source code [on GitHub](https://github.com/skrunsky/python-project).*")
