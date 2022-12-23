import streamlit as st
import pandas as pd

feedings = pd.read_parquet('/Users/admin/Documents/GitHub/keeprising/data/feedings.parquet')

st.title('Keep Rising')

st.write(feedings)