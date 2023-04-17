# Libraries
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import json
import openai
import base64

# getting keys
with open('config/config.json') as f:
    keys = json.load(f)
PATH = keys['path']
openai_organization = keys['openai_organization']
openai.organization = openai_organization
openai_api_key = keys['openai_api_key']
openai.api_key = openai_api_key
openai.Model.list()


# Functions
# better read functions from utils, but not yet working
def add_bg(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
    
# merging historical activities with latest activity data
def add_latest_activity(df_hist, df_new, date_column):
    
    # Fixing dtypes
    df_hist[date_column] = df_hist[date_column].astype(str)
    df_new[date_column] = df_new[date_column].astype(str)
    
    # Df merging of historical feedings and latest feeding
    df = pd.concat([df_hist, df_new], ignore_index=True)
    df[date_column] = pd.to_datetime(df[date_column])
    df[date_column] = df[date_column].dt.strftime('%Y-%m-%d')
    
    return df


# Loading data
notes_history = pd.read_parquet(PATH + 'notes_history.parquet')
    
    
# streamlit page
st.set_page_config(page_title="Keeprising")
add_bg('bread_loaf.png')  
st.title('Keeprising - Here to help you')


# Notes
st.header("Your observations - Misstakes are there to learn")
latest_note = st.text_input('Type your observation here')
latest_date = st.date_input('Date')

latest_note = pd.DataFrame(data={
    'date':latest_date, 
    'notes':latest_note,
}, index=[0])

notes_history = add_latest_activity(df_hist=notes_history, df_new=latest_note, date_column='date')
notes_history = notes_history.set_index('date')

st.dataframe(notes_history)


# Help area
st.header("Ask for help")
question = st.text_input('Ask your question here')
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a bakery educator."},
        {"role": "user", "content": question},
    ]
)
answer = response['choices'][0]['message']['content']

st.write(answer)
