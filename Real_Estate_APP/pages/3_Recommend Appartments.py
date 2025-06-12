import os
import joblib
import pickle
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="Recommend Apartments")

# Dynamically locate the project root directory
current_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))  # Two levels up
datasets_dir = os.path.join(project_root, 'Real_Estate_APP', 'datasets')

# File paths
location_distance_path = os.path.join(datasets_dir, 'location_distance.pkl')
cosine_sim1_path = os.path.join(datasets_dir, 'cosine_sim1.pkl')
cosine_sim2_path = os.path.join(datasets_dir, 'cosine_sim2.pkl')
cosine_sim3_path = os.path.join(datasets_dir, 'cosine_sim3.pkl')

# Check if the dataset file exists
if not os.path.exists(location_distance_path):
    st.error(f"Dataset file not found: {location_distance_path}")
    st.stop()

# Try to load the location_distance.pkl file
try:
    with open(location_distance_path, 'rb') as file:
        location_data = joblib.load(file)

    # Print debug info
    print(f"Loaded data type: {type(location_data)}")

    # Convert to DataFrame if needed
    if isinstance(location_data, pd.DataFrame):
        location_df = location_data
    elif isinstance(location_data, dict):
        location_df = pd.DataFrame(location_data)
    elif isinstance(location_data, list):
        location_df = pd.DataFrame(location_data)
    else:
        st.error(f"Unsupported data type: {type(location_data)}")
        st.stop()

except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# Check if the cosine similarity files exist
for cosine_sim_path in [cosine_sim1_path, cosine_sim2_path, cosine_sim3_path]:
    if not os.path.exists(cosine_sim_path):
        st.error(f"Cosine similarity file not found: {cosine_sim_path}")
        st.stop()

# Load cosine similarity matrices
try:
    with open(cosine_sim1_path, 'rb') as file:
        cosine_sim1 = pickle.load(file)
    with open(cosine_sim2_path, 'rb') as file:
        cosine_sim2 = pickle.load(file)
    with open(cosine_sim3_path, 'rb') as file:
        cosine_sim3 = pickle.load(file)
except FileNotFoundError as e:
    st.error(f"File not found: {e.filename}")
    st.stop()
except Exception as e:
    st.error(f"Error loading cosine similarity files: {e}")
    st.stop()

# Recommendation function
def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3

    if property_name not in location_df.index:
        st.error("Selected property not found in dataset.")
        return pd.DataFrame()

    idx = location_df.index.get_loc(property_name)
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    top_properties = location_df.index[top_indices].tolist()

    return pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

# Streamlit UI: Radius-based filter
st.title('Select Location and Radius')
selected_location = st.selectbox('Location', sorted(location_df.columns.to_list()))
radius = st.number_input('Radius in Kms', min_value=0.0)

if st.button('Search'):
    if selected_location in location_df.columns:
        result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()
        for key, value in result_ser.items():
            st.text(f"{key} - {round(value / 1000)} kms")
    else:
        st.error("Selected location not found in columns.")

# Streamlit UI: Recommendation system
st.title('Recommend Apartments')
selected_apartment = st.selectbox('Select an apartment', sorted(location_df.index.to_list()))

if st.button('Recommend'):
    recommendation_df = recommend_properties_with_scores(selected_apartment)
    if not recommendation_df.empty:
        st.dataframe(recommendation_df)
