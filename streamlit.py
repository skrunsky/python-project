import streamlit as st

import datetime
import time
import data_retriever as dr

# Retrieve currencies and make a list
currencies = dr.retrieve_currencies()
currency_list = list(currencies.values())

st.set_page_config(
    page_title="This is a cool app",
    page_icon="💡",
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

    st.title("Options")
    st.selectbox("Select a cryptocurrency", currency_list)
    st.number_input("Enter amount of runs", 1, 1000)

    st.title("Filters")
    "\n"

    # Cryptocurrency selection 
    st.multiselect('Select the cryptocurrencies you want to analyse', ['test', 'two'])
    "\n"

    # Defining the period interval
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    start_date = st.date_input('Start date', today)
    end_date = st.date_input('End date', tomorrow)
    if start_date < end_date:
        pass
    else:
        st.error('Error: The End date must come after the Start date.')
    "\n"

    # Defining the number of runs
    st.slider('How many times do you want to run the model?', 1, 1000)
    st.caption('Note: The more times you run the model, the more accurate the results are.')
    "\n"
    st.button('Next')

# Progress status
with st.spinner('Loading...'):
    time.sleep(1)

# Footer content for the webpage
st.markdown(
    "Created by Enrique Fabio Ferrari-Pedruzzi, Gianluca Pecoraro, Sigurd Koldste & Vera Mendes as part of an Introduction to Programming project at [Nova School of Business and Economics](https://novasbe.pt/).")
st.markdown(
    "*Find the full source code [on GitHub](https://github.com/skrunsky/python-project).*")
