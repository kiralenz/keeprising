import pandas as pd

# Streamlit styling
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


# adding a column with the microbial composition based on the feeding temperature
def bacteria_column(df, bac_compos):
    df['bacteria_composition'] = np.where(
        df["temperature"] <= 20,
        bac_compos.loc[
            bac_compos["temperature"] == 20, "dominant_microbes"
        ],
        np.where(
            ((df["temperature"] > 20) & (df["temperature"] <= 25)),
            bac_compos.loc[
                bac_compos["temperature"] == 25, "dominant_microbes"
            ],
            np.where(
                ((df["temperature"] > 25) & (df["temperature"] <= 30)),
                bac_compos.loc[
                    bac_compos["temperature"] == 30, "dominant_microbes"
                ],
                bac_compos.loc[
                    bac_compos["temperature"] == 35, "dominant_microbes"
                ],
            ),
        ),
    )
    return df


# adding two columns for growth rates, one time normalized
def growth_rate_cols(df):
    df['growth_rate'] = (
        df['end_height'] / df['initial_height']
    )

    df['growth_rate_per_hour'] = (
        df['end_height'] 
        / df['initial_height'] 
        / df['feeding_time']
    )
    
    return df
  
    
def addone(number):
    new_number = number + 1
    return new_number