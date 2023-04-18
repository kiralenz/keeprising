# Libraries
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import json
import base64

# getting variables from config.json
with open('config/config.json') as f:
    keys = json.load(f)
PATH = keys['path']

# Functions
# better read functions from utils, but not yet working
def add_bg():
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(https://gist.githubusercontent.com/kiralenz/8fa216a5ab87e92944129da83d84dd5b/raw/806c89b90ee9c6eaf75f833eb9482c9cbca7dec1/bread_loaf.svg);
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
    
def add_logo(height):
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url(https://gist.githubusercontent.com/kiralenz/16203a45856cfb596741f24f85e82fbe/raw/c9d93e3336730e77132d40df4eb8d758471bcfd8/keeprising_logo.svg);
                background-repeat: no-repeat;
                padding-top: {height - 40}px;
                background-position: 20px 20px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# leftover dough calculation for action display
def leftover_action(df):
    total_dough = []
    cumsum = 0
    for index, row in df.iterrows():
        if row['recycling_happened'] == False:
            cumsum = cumsum + row['delta_starter'] 
            total_dough.append(cumsum)
        else:
            cumsum = 0
            total_dough.append(cumsum)
    df['total_dough'] = total_dough


    if df.iloc[-1, 1] > 200:
        action = ('Time to get creative! You have ' + str(df.iloc[-1, 1]) + 'g of starter leftover.')
    else:
        action = ('You have ' + str(df.iloc[-1, 1]) + 'g of starter leftover.')
    
    return action


# Loading data
feedings = pd.read_parquet(PATH + 'feedings.parquet')
feedings_processed = pd.read_parquet(PATH + 'feedings_processed.parquet')
baked_bread = pd.read_parquet(PATH + 'baked_bread.parquet')
left_over = pd.read_parquet(PATH + 'left_over.parquet')


# streamlit page
st.set_page_config(page_title="Keeprising")
st.set_page_config(layout="wide")
add_bg()
add_logo()
st.title('Keep Rising - Monitoring')


# KPIs
st.header('KPIs')
# calculation of the activity
action = leftover_action(df=left_over)

col1, col2, col3, col4= st.columns(4)
with col1:
    st.subheader('Your bread rating')
    st.write(baked_bread.sort_values(by='bread_rating', ascending=False)['bread_name'].head(3))
with col2:
    st.subheader('Your bread count')
    st.write(len(baked_bread))
with col3:
    st.subheader('Microbe composition')
    st.write(feedings_processed['bacteria_composition'].tail(1).values)
with col4:
    st.subheader('Starter volume status')
    st.write(action)


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
