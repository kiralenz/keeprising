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


# Loading data
feedings = pd.read_parquet(PATH + 'feedings.parquet')
baked_bread = pd.read_parquet(PATH + 'baked_bread.parquet')
recyled_dough = pd.read_parquet(PATH + 'recycled_dough.parquet')


# streamlit page
st.set_page_config(page_title="Keeprising")
add_bg('bread_loaf.png')  
st.title('Keeprising - Your Feeding')
st.header('How was your feeding?')

# Adding new feeding data
st.write('How was your last feeding?')
date_today = st.date_input('Feeding date')
temperature_today = st.number_input('Temperature')
feeding_time_today = st.number_input('Feeding duration')
initial_height_today = st.number_input('Intial height')
end_height_today = st.number_input('End height')
bubble_size_today = st.number_input('Bubble size')

latest_feeding = pd.DataFrame(data={
    'feeding_date':date_today, 
    'temperature':temperature_today,
    'feeding_time':feeding_time_today,
    'initial_height':initial_height_today,
    'end_height':end_height_today,
    'bubble_size':bubble_size_today
}, index=[0])

# Fixing dtypes
feedings['feeding_date'] = feedings['feeding_date'].astype(str)
latest_feeding['feeding_date'] = latest_feeding['feeding_date'].astype(str)


# Df merging
feedings = pd.concat([feedings, latest_feeding], ignore_index=True)
feedings['feeding_date'] = pd.to_datetime(feedings['feeding_date'])
feedings['feeding_date'] = feedings['feeding_date'].dt.strftime('%Y-%m-%d')

# saving df
feedings.to_parquet(PATH + 'feedings.parquet')

# application display
st.dataframe(feedings.tail())
st.write("Nice job! Well done!")


# Data processing
# Bacteria composition
bacteria_composition = pd.read_parquet(PATH + 'bacteria_composition.parquet')
feedings_processed = feedings.copy()
feedings_processed["bacteria_composition"] = np.where(
    feedings_processed["temperature"] <= 20,
    bacteria_composition.loc[
        bacteria_composition["temperature"] == 20, "dominant_microbes"
    ],
    np.where(
        ((feedings_processed["temperature"] > 20) & (feedings_processed["temperature"] <= 25)),
        bacteria_composition.loc[
            bacteria_composition["temperature"] == 25, "dominant_microbes"
        ],
        np.where(
            ((feedings_processed["temperature"] > 25) & (feedings_processed["temperature"] <= 30)),
            bacteria_composition.loc[
                bacteria_composition["temperature"] == 30, "dominant_microbes"
            ],
            bacteria_composition.loc[
                bacteria_composition["temperature"] == 35, "dominant_microbes"
            ],
        ),
    ),
)


# Growth rate
feedings_processed['growth_rate'] = feedings_processed['end_height'] / feedings_processed['initial_height']
feedings_processed['growth_rate_per_hour'] = (
    feedings_processed['end_height'] 
    / feedings_processed['initial_height'] 
    / feedings['feeding_time']
)

# Storing data
feedings_processed.to_parquet(PATH + 'feedings_processed.parquet')
