import os
import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Plotting Demo")

st.title('Analytics')

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the paths to the datasets
data_viz1_path = os.path.join(script_dir, '..', 'datasets', 'data_viz1.csv')
feature_text_path = os.path.join(script_dir, '..', 'datasets', 'feature_text.pkl')

# Load the datasets
new_df = pd.read_csv(data_viz1_path)
with open(feature_text_path, 'rb') as file:
    feature_text = pickle.load(file)

# Ensure numeric columns are clean
numeric_cols = ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']
new_df[numeric_cols] = new_df[numeric_cols].apply(pd.to_numeric, errors='coerce')
new_df.dropna(subset=numeric_cols, inplace=True)

# Group data
group_df = new_df.groupby('sector').mean(numeric_only=True)[numeric_cols]

st.header('Sector Price per Sqft Geomap')
fig = px.scatter_mapbox(
    group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
    color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
    mapbox_style="open-street-map", width=1200, height=700, hover_name=group_df.index
)

st.plotly_chart(fig, use_container_width=True)

st.header('Features Wordcloud')

# Truncate the feature_text if it's too large and limit the number of words
feature_text = ' '.join(feature_text.split()[:1000])  # Use first 1000 words

# Create a figure and axis explicitly for the wordcloud
fig, ax = plt.subplots(figsize=(8, 8), facecolor=None)

wordcloud = WordCloud(
    width=600, height=600,  # Reduced size
    background_color='black',
    stopwords=set(['s']), min_font_size=10,
    max_words=100  # Limit the number of words
).generate(feature_text)

# Display wordcloud on the axes
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
plt.tight_layout(pad=0)

# Display the figure in Streamlit
st.pyplot(fig)

st.header('Area Vs Price')

property_type = st.selectbox('Select Property Type', ['flat', 'house'])

if property_type == 'house':
    fig1 = px.scatter(
        new_df[new_df['property_type'] == 'house'], x="built_up_area", y="price",
        color="bedRoom", title="Area Vs Price"
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(
        new_df[new_df['property_type'] == 'flat'], x="built_up_area", y="price",
        color="bedRoom", title="Area Vs Price"
    )
    st.plotly_chart(fig1, use_container_width=True)

st.header('BHK Pie Chart')

sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0, 'overall')

selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':
    fig2 = px.pie(new_df, names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)
else:
    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)

st.header('Side by Side BHK price comparison')

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')
st.plotly_chart(fig3, use_container_width=True)

st.header('Side by Side Distplot for property type')

fig3 = plt.figure(figsize=(10, 4))
sns.histplot(new_df[new_df['property_type'] == 'house']['price'], label='house', kde=True)
sns.histplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat', kde=True)
plt.legend()
st.pyplot(fig3)
