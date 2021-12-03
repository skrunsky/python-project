import streamlit as st
import data_retriever as dr

# Retrieve currencies and make a list
currencies = dr.retrieve_currencies()
currency_list = list(currencies.values())

# Header content for the webpage
st.header("Amazing Python Project")
st.subheader("Created by amazing people")

# Introduction to the product and how to use it


# Adding currency selector to sidebar
with st.sidebar:
    st.title("Options")
    st.selectbox("Select a cryptocurrency", currency_list)
    st.number_input("Enter amount of runs", 1, 1000)

# Footer content for the webpage
st.markdown(
    "Created by Sigurd Koldste, Vera Mendes, Gianluca Pecoraro & Enrique Fabio Ferrari-Pedruzzi, as part of a project at [Nova School of Business and Economics](https://novasbe.pt/). "
)
st.markdown(
    "*Find the full source code [on GitHub](https://github.com/skrunsky/python-project).*")
