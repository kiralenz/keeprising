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

# getting keys
# with open('config/config.json') as f:
#     keys = json.load(f)
# openai_api_key = keys['openai_api_key']
# openai_organization = keys['openai_organization']
# openai.organization = openai_organization
# openai.api_key = openai_api_key
# openai.Model.list()

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
feedings_processed = pd.read_parquet(PATH + 'feedings_processed.parquet')
baked_bread = pd.read_parquet(PATH + 'baked_bread.parquet')

# streamlit page
st.set_page_config(page_title="Keeprising")
add_bg('bread_loaf.png')  
st.title('Keep Rising - Dashboards')


# KPIs
st.header('KPIs')
st.subheader('Your bread rating')
st.write(baked_bread.sort_values(by='bread_rating', ascending=False)['bread_name'].head(3))
st.subheader('Your bread count')
st.write('You baked ' + str(len(baked_bread)) + ' breads.')
st.subheader('Your starter')
st.write('Your starter contains mainly microbes of type' + str(feedings_processed['bacteria_composition'].tail(1).values))



# Plots
# 1) Bread
st.header("Plots")
baked_bread['baking_date'] = pd.to_datetime(baked_bread['baking_date'])
plot_baked_bread = baked_bread.groupby(pd.Grouper(key="baking_date", freq="M"))[
        "bread_rating"
    ].mean().to_frame('avg_bread_rating')
fig, ax = plt.subplots(figsize=(6, 5))
plot_baked_bread.plot(kind='bar', ylabel='Average bread rating', legend=False, ax=ax)
# Adapt the x tick labels
ticklabels = plot_baked_bread.index
ticklabels = [item.strftime('%m-%Y') for item in plot_baked_bread.index]
ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
plt.gcf().autofmt_xdate()
# plot in streamlit
st.pyplot(fig)


# 2) Feeding
growth_dependence_from_temperature2 = sns.lmplot(data=feedings_processed, x='temperature', y='growth_rate_per_hour', height=5, aspect=2).set(
    title="Growth dependence from temperature"
);
st.pyplot(growth_dependence_from_temperature2)


bubblesize_dependence_from_temperature2 = sns.lmplot(data=feedings, x='temperature', y='bubble_size', height=5, aspect=2).set(
    title="Bubble size dependence from temperature"
);
st.pyplot(bubblesize_dependence_from_temperature2)


# bacteria_composition = sns.boxenplot(x="bacteria_composition", y="growth_rate", data=feedings_processed) #.set(title="Growth Rate by Bacteria Composition")
# st.pyplot(bacteria_composition)
