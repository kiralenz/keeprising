import streamlit as st

st.set_page_config(
    page_title="Hello",
)

st.write("# Welcome to keeprising!")

st.sidebar.success("Select")

st.markdown(
    """
    keeprising is a sourdough monitoring tool.
    You can select an activity or the dashboard mode in the sidebar. 
    In the help page you can find the possibility to ask ChatGPT for
    bread support or find maybe FAQs in the future. 
"""
)