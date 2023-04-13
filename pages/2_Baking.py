# Libraries
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import json
# import openai
import base64

# getting variables from config.json
with open('config/config.json') as f:
    keys = json.load(f)
PATH = keys['path']


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
feedings = pd.read_parquet(PATH + 'feedings.parquet')
baked_bread = pd.read_parquet(PATH + 'baked_bread.parquet')
recycled_dough = pd.read_parquet(PATH + 'recycled_dough.parquet')


# streamlit page
st.set_page_config(page_title="Keeprising") 
add_bg('bread_loaf.png')  
st.title('Keep Rising - Your baking')
st.header('How was your baking?')


# Adding new baking data - user input
latest_baking_date = st.date_input('Baking date')
latest_bread = st.text_input('Bread name')
latest_rating = st.number_input('Rating - 0 to 10')
starter_used = st.number_input('Starter used in g')

# storing new data in a dataframe
latest_bread = pd.DataFrame(data={
    'bread_name':latest_bread,
    'baking_date':latest_baking_date,
    'bread_rating':latest_rating,
    'used_starter':starter_used
}, index=[0])

# merging the new data to historic data
baked_bread = add_latest_activity(
    df_hist=baked_bread, 
    df_new=latest_bread, 
    date_column='baking_date')

# Saving data
baked_bread.to_parquet(PATH + 'baked_bread.parquet')
st.dataframe(baked_bread.tail(3))


# Starter recycling
st.header('Did you recycle?')
recycling_bool = st.checkbox(label="Select here if you used leftover starter.", value=False)

if recycling_bool:
    latest_recycling_date = st.date_input('Recycling date')
    
    # storing new data in a dataframe
    latest_recycling = pd.DataFrame(data={
        'date':latest_recycling_date,
        'recycling_happened':True
    }, index=[0])
    
    # merging new to historic data
    recycled_dough = add_latest_activity(
    df_hist=recycled_dough, 
    df_new=latest_recycling, 
    date_column='date')


# Processing
# TODO: functionalize
# Utilized sourdough starter
used_for_bread = baked_bread[['baking_date', 'used_starter']]
used_for_bread.rename(columns={
    'baking_date':'date',
    'used_starter':'delta_starter'
}, inplace=True)
used_for_bread['delta_starter'] = used_for_bread['delta_starter']*(-1)

leftover_starter = feedings[['feeding_date']]
leftover_starter.rename(columns={'feeding_date':'date'}, inplace=True)
# assuming a use of 40g for the new starter and a loss of 10g
leftover_starter['delta_starter'] = 55

# TODO: functionalize
# Leftover calculation
left_over = pd.concat([used_for_bread, leftover_starter, recycled_dough], ignore_index=True)
left_over['date'] = pd.to_datetime(left_over['date'])
left_over.sort_values(by='date', inplace=True)
left_over['recycling_happened'] = left_over['recycling_happened'].fillna(False)
left_over.reset_index(inplace=True, drop=True)

# leftover dough calculation
total_dough = []
cumsum = 0
for index, row in left_over.iterrows():
    if row['recycling_happened'] == False:
        cumsum = cumsum + row['delta_starter'] 
        total_dough.append(cumsum)
    else:
        cumsum = 0
        total_dough.append(cumsum)
left_over['total_dough'] = total_dough


if left_over.iloc[-1, 1] > 200:
    action = ('Time to get creative! You have ' + str(left_over.iloc[-1, 1]) + 'g of starter leftover.')
else:
    action = ('You have ' + str(left_over.iloc[-1, 1]) + 'g of starter leftover.')

# Actions
st.header("Your starter status")
st.write(action)
