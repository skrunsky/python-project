import streamlit as st

# Header content for the webpage
st.header("Amazing Python Project")
st.subheader("Created by amazing peopl")

# Introduction to the product and how to use it


# Adding currency selector to sidebar
with st.sidebar:
    st.title("Options")
    st.selectbox("Select a cryptocurrency", ["test", "two"])
    st.number_input("Enter amount of runs", 1, 1000)

# Footer content for the webpage
st.markdown(
    "Created by Sigurd Koldste, Vera Mendes, Gianluca Pecoraro & Enrique Fabio Ferrari-Pedruzzi, as part of a project at [Nova School of Business and Economics](https://novasbe.pt/). "
)
st.markdown(
    "*Find the full source code [on GitHub](https://github.com/skrunsky/python-project).*")
