#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('load_ext', 'blackcellmagic')


# In[2]:


import pandas as pd
import seaborn as sns
import numpy as np


# In[4]:


PATH = ('/Users/admin/Documents/GitHub/keeprising/data/')


# # Data

# ## Feeding data update

# ### Loading past feeding data

# In[21]:


feedings = pd.read_parquet(PATH + 'feedings.parquet')


# ### Adding new data

# In[8]:


date_today = '2022-12-20'


# In[10]:


temperature_today = 19


# In[11]:


feeding_time_today = 10


# In[12]:


initial_height_today = 2.9


# In[13]:


end_height_today = 7.9


# In[14]:


bubble_size_today = 0.3


# In[18]:


latest_feeding = pd.DataFrame(data={
    'feeding_date':date_today, 
    'temperature':temperature_today,
    'feeding_time':feeding_time_today,
    'initial_height':initial_height_today,
    'end_height':end_height_today,
    'bubble_size':bubble_size_today
}, index=[0])


# In[ ]:





# ### Df merging

# In[23]:


feedings = pd.concat([feedings, latest_feeding], ignore_index=True)


# In[24]:


feedings.to_parquet(PATH + 'feedings.parquet')


# In[ ]:





# ## Data processing

# ### Bacteria composition

# **TODO**
# * improve bacteria composition

# In[66]:


bacteria_composition = pd.DataFrame({
    'temperature':[20, 25,30, 35],
    'dominant_microbes':['none', 'lactic acid bacteria', 'Acetic acid bacteria', 'sourdough yeast']
})


# In[67]:


bacteria_composition


# In[ ]:





# In[68]:


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


# ### Growth rate

# In[69]:


feedings['growth_rate'] = feedings['end_height'] / feedings['initial_height']


# In[70]:


feedings['growth_rate_per_hour'] = feedings['end_height'] / feedings['initial_height'] / feedings['feeding_time']


# In[71]:


feedings.head()


# In[ ]:





# ## Utilization

# ### Baked breads

# #### Loading past bread data

# In[26]:


baked_bread = pd.read_parquet(PATH + 'baked_bread.parquet')


# #### Adding new data

# In[29]:


latest_bread = 'Paderborner Landbrot'


# In[30]:


latest_baking_date = '2022-12-14'


# In[31]:


latest_ranking = 3


# In[32]:


latest_starter_used = 30


# In[33]:


latest_bread = pd.DataFrame(data={
    'bread_name':latest_bread,
    'baking_date':latest_baking_date,
    'bread_rating':latest_ranking,
    'used_starter':latest_starter_used
}, index=[0])


# #### Df merging 

# In[39]:


baked_bread = pd.concat([baked_bread, latest_bread], ignore_index=True)


# In[40]:


baked_bread['baking_date'] = pd.to_datetime(baked_bread['baking_date'])


# In[42]:


baked_bread.to_parquet(PATH + 'baked_bread.parquet')


# In[ ]:





# ### Utilized sourdough starter

# #### For baking

# In[43]:


used_for_bread = baked_bread[['baking_date', 'used_starter']]


# In[44]:


used_for_bread.rename(columns={
    'baking_date':'date',
    'used_starter':'delta_starter'
}, inplace=True)


# In[45]:


used_for_bread['delta_starter'] = used_for_bread['delta_starter']*(-1)


# In[46]:


used_for_bread


# #### Leftover from feeding

# In[47]:


old_dough = feedings[['feeding_date']]


# In[48]:


old_dough.rename(columns={'feeding_date':'date'}, inplace=True)


# In[49]:


# assuming a use of 10g for the new starter and a loss of 10g
old_dough['delta_starter'] = 90


# #### Recycle utilizations

# In[51]:


recyled_dough = pd.read_parquet(PATH + 'recycled_dough.parquet')


# #### Total

# In[53]:


left_over = pd.concat([used_for_bread, old_dough, recyled_dough], ignore_index=True)


# In[54]:


left_over['date'] = pd.to_datetime(left_over['date'])


# In[55]:


left_over.sort_values(by='date', inplace=True)


# In[56]:


left_over['recycling_happened'] = left_over['recycling_happened'].fillna(False)


# In[57]:


left_over.reset_index(inplace=True, drop=True)


# In[58]:


total_dough = []
cumsum = 0
for index, row in left_over.iterrows():
    if row['recycling_happened'] == False:
        cumsum = cumsum + row['delta_starter'] 
        total_dough.append(cumsum)
    else:
        cumsum = 0
        total_dough.append(cumsum)


# In[59]:


left_over['total_dough'] = total_dough


# In[ ]:





# ### Bread experiments TODO

# **TODO**
# * Vorgehen + Modifikation + Resultat + Experimentbasis (Brot) 

# In[ ]:





# # KPIs

# ## Bread

# **Top 3 breads**

# In[62]:


baked_bread.sort_values(by='bread_rating', ascending=False)['bread_name'].head(3)


# In[ ]:





# **Baked breads**

# In[63]:


len(baked_bread)


# In[ ]:





# **Relevant factors**

# In[ ]:





# ## Sourdough

# **Current bacteria dominance**

# In[72]:


feedings['bacteria_composition'].tail(1)


# In[ ]:





# ## Leftovers

# **TODO**
# * turn into function

# In[73]:


if left_over.iloc[-1, 1] > 200:
    print('Time to get creative! You have ' + str(left_over.iloc[-1, 1]) + 'g of starter leftover.')
else:
    print('You have ' + str(left_over.iloc[-1, 1]) + 'g of starter leftover.')


# In[ ]:





# In[ ]:





# # Plots

# ## Bread

# In[86]:


sns.displot(
    data=baked_bread.groupby(pd.Grouper(key="baking_date", freq="M"))[
        "bread_rating"
    ].mean(),
    x="baking_date",
    height=5,
    aspect=2,
).set(title='Baked breads per month');


# In[149]:


sns.set(rc={'figure.figsize':(15,5)})
sns.lineplot(data=baked_bread, x='baking_date', y='bread_rating'
).set(title='Bread rating');


# ## Feeding

# In[143]:


sns.relplot(data=feedings, x="temperature", y="growth_rate_per_hour", kind="line", height=5, aspect=2).set(
    title="Growth dependence from temperature"
);


# In[144]:


sns.lmplot(data=feedings, x='temperature', y='growth_rate_per_hour', height=5, aspect=2).set(
    title="Growth dependence from temperature"
);


# In[146]:


sns.relplot(data=feedings, x='temperature', y='bubble_size', kind='line',  height=5, aspect=2).set(
    title="Bubble size dependence from temperature"
);


# In[148]:


sns.lmplot(data=feedings, x='temperature', y='bubble_size', height=5, aspect=2).set(
    title="Bubble size dependence from temperature"
);


# In[136]:


sns.catplot(data=feedings, x='bacteria_composition', y='growth_rate', kind='boxen');


# In[ ]:





# In[ ]:





# In[ ]:




