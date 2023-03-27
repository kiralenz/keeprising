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
openai_api_key = keys['openai_api_key']
openai_organization = keys['openai_organization']
openai.organization = openai_organization
openai.api_key = openai_api_key
openai.Model.list()

# Variables
PATH = ('/Users/kiralenz/Documents/keeprising/data/')

# Loading data
feedings = pd.read_parquet(PATH + 'feedings.parquet')
baked_bread = pd.read_parquet(PATH + 'baked_bread.parquet')
recyled_dough = pd.read_parquet(PATH + 'recycled_dough.parquet')
feedings_processed = pd.read_parquet(PATH + 'feedings_processed.parquet')

# Functions
# better read functions from utils, but not yet working
def add_bg_from_local(image_file):
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

# streamlit page
st.set_page_config(page_title="Keeprising") 
add_bg_from_local('bread_loaf.png')  
st.title('Keep Rising - Your baking')
st.header('How was your baking?')

# Baked breads
# Adding new data
latest_baking_date = st.date_input('Baking date')
latest_bread = st.text_input('Bread name')
latest_rating = st.number_input('Rating - 0 to 10')
starter_used = st.number_input('Starter used in g')


latest_bread = pd.DataFrame(data={
    'bread_name':latest_bread,
    'baking_date':latest_baking_date,
    'bread_rating':latest_rating,
    'used_starter':starter_used
}, index=[0])

baked_bread['baking_date'] = baked_bread['baking_date'].astype(str)
latest_bread['baking_date'] = latest_bread['baking_date'].astype(str)

# Df merging 
baked_bread = pd.concat([baked_bread, latest_bread], ignore_index=True)
baked_bread['baking_date'] = pd.to_datetime(baked_bread['baking_date'])
baked_bread['baking_date'] = baked_bread['baking_date'].dt.strftime('%Y-%m-%d')

# Saving data
baked_bread.to_parquet(PATH + 'baked_bread.parquet')
st.dataframe(baked_bread.tail(3))


# Processing
# TODO: functionalize
# Utilized sourdough starter
used_for_bread = baked_bread[['baking_date', 'used_starter']]
used_for_bread.rename(columns={
    'baking_date':'date',
    'used_starter':'delta_starter'
}, inplace=True)
used_for_bread['delta_starter'] = used_for_bread['delta_starter']*(-1)

old_dough = feedings[['feeding_date']]
old_dough.rename(columns={'feeding_date':'date'}, inplace=True)
# assuming a use of 40g for the new starter and a loss of 10g
old_dough['delta_starter'] = 55


# TODO: functionalize
# Leftover calculation
left_over = pd.concat([used_for_bread, old_dough, recyled_dough], ignore_index=True)
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
