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
add_bg_from_local('bread_loaf.png')  
st.title('Keep Rising - Dashboards')

st.header('Another feeding')

# TODO: Add field for input
# Adding new feeding data
st.write('How was your last feeding?')
date_today = st.date_input('Feeding date')
# date_today = '2022-12-20'
temperature_today = st.number_input('Temperature')
# temperature_today = 19
feeding_time_today = st.number_input('Feeding duration')
# feeding_time_today = 10
initial_height_today = st.number_input('Intial height')
# initial_height_today = 2.9
end_height_today = st.number_input('End height')
# end_height_today = 7.9
bubble_size_today = st.number_input('Bubble size')
# bubble_size_today = 0.3

st.write(date_today)
st.write(temperature_today)
st.write(feeding_time_today)
st.write(end_height_today)
st.write(bubble_size_today)

# latest_feeding = pd.DataFrame(data={
#     'feeding_date':date_today, 
#     'temperature':temperature_today,
#     'feeding_time':feeding_time_today,
#     'initial_height':initial_height_today,
#     'end_height':end_height_today,
#     'bubble_size':bubble_size_today
# }, index=[0])


# # Df merging
# feedings = pd.concat([feedings, latest_feeding], ignore_index=True)
# feedings.to_parquet(PATH + 'feedings.parquet')

# Data processing
# Bacteria composition
bacteria_composition = pd.DataFrame({
    'temperature':[20, 25,30, 35],
    'dominant_microbes':['none', 'lactic acid bacteria', 'Acetic acid bacteria', 'sourdough yeast']
})


feedings["bacteria_composition"] = np.where(
    feedings["temperature"] <= 20,
    bacteria_composition.loc[
        bacteria_composition["temperature"] == 20, "dominant_microbes"
    ],
    np.where(
        ((feedings["temperature"] > 20) & (feedings["temperature"] <= 25)),
        bacteria_composition.loc[
            bacteria_composition["temperature"] == 25, "dominant_microbes"
        ],
        np.where(
            ((feedings["temperature"] > 25) & (feedings["temperature"] <= 30)),
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
feedings['growth_rate'] = feedings['end_height'] / feedings['initial_height']
feedings['growth_rate_per_hour'] = feedings['end_height'] / feedings['initial_height'] / feedings['feeding_time']


# Utilization
# Baked breads
# Adding new data

st.header('Latest bread')
latest_bread = 'Paderborner Landbrot'
latest_baking_date = '2022-12-14'
latest_ranking = 3
latest_starter_used = 30

st.write(latest_bread)
st.write(latest_baking_date)
st.write(latest_ranking)
st.write(latest_starter_used)

# latest_bread = pd.DataFrame(data={
#     'bread_name':latest_bread,
#     'baking_date':latest_baking_date,
#     'bread_rating':latest_ranking,
#     'used_starter':latest_starter_used
# }, index=[0])

# # Df merging 
# baked_bread = pd.concat([baked_bread, latest_bread], ignore_index=True)
# baked_bread['baking_date'] = pd.to_datetime(baked_bread['baking_date'])
# baked_bread.to_parquet(PATH + 'baked_bread.parquet')

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
# assuming a use of 10g for the new starter and a loss of 10g
old_dough['delta_starter'] = 90

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


# KPIs

st.header('KPIs')
st.subheader('Your bread rating')
st.write(baked_bread.sort_values(by='bread_rating', ascending=False)['bread_name'].head(3))
st.subheader('Your bread count')
st.write('You baked ' + str(len(baked_bread)) + ' breads.')
st.subheader('Your starter')
st.write('Your starter contains mainly microbes of type' + str(feedings['bacteria_composition'].tail(1).values))

if left_over.iloc[-1, 1] > 200:
    action = ('Time to get creative! You have ' + str(left_over.iloc[-1, 1]) + 'g of starter leftover.')
else:
    action = ('You have ' + str(left_over.iloc[-1, 1]) + 'g of starter leftover.')

# Actions
st.write(action)


# Plots
# 1) Bread
st.header("Plots")
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
growth_dependence_from_temperature2 = sns.lmplot(data=feedings, x='temperature', y='growth_rate_per_hour', height=5, aspect=2).set(
    title="Growth dependence from temperature"
);
st.pyplot(growth_dependence_from_temperature2)


# bubblesize_dependence_from_temperature = sns.relplot(data=feedings, x='temperature', y='bubble_size', kind='line',  height=5, aspect=2).set(
#     title="Bubble size dependence from temperature"
# );
# st.pyplot(bubblesize_dependence_from_temperature)


bubblesize_dependence_from_temperature2 = sns.lmplot(data=feedings, x='temperature', y='bubble_size', height=5, aspect=2).set(
    title="Bubble size dependence from temperature"
);
st.pyplot(bubblesize_dependence_from_temperature2)


# bacteria_composition_plot = sns.catplot(data=feedings, x='bacteria_composition', y='growth_rate', kind='boxen');
# st.pyplot(bacteria_composition_plot)



# Help area
st.header("Help")
question = st.text_input('Ask your question here')
# response = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#         {"role": "system", "content": "You are a bakery educator."},
#         {"role": "user", "content": question},
#     ]
# )
# answer = response['choices'][0]['message']['content']
# helper code which is not necessary anymore
response = 'Answer to question: ' + question
answer=response

st.write(answer)
