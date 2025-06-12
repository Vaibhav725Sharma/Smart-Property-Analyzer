import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Gurgaon Real Estate Analytics App",
    page_icon="🏡",
    layout="wide"
)

# Custom styling
st.markdown(
    """
    <style>
        .main-title {
            font-size: 40px;
            font-weight: bold;
            color: #2E86C1;
            text-align: center;
        }
        .sub-title {
            font-size: 20px;
            color: #566573;
            text-align: center;
        }
        .sidebar-text {
            font-size: 18px;
            font-weight: bold;
            color: #154360;
        }
        .stApp {
            background: url('https://source.unsplash.com/1600x900/?real-estate,city') no-repeat center center fixed;
            background-size: cover;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Page title
st.markdown("<p class='main-title'>Welcome to Gurgaon Real Estate Analytics App 🏡</p>", unsafe_allow_html=True)



st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmk0d3pwbGk2eTZwbHlhaWR0MHZ0c3JieTduaG5nbHRhNXptczg3eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Sb6ttkJpJ1uU2XqC6J/giphy.gif" width="400">
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align: center; font-size: 20px; font-weight: bold; color: #566573;">
        Smart Choices, Better Prices – Your Guide to Real Estate Success!
    </div>
    """, 
    unsafe_allow_html=True
)


st.markdown(
    """
    <div style="text-align: center; font-size: 18px; font-weight: bold; color: #34495E;">
        🚀 Created by <b>Vaibhav Sharma, Priyansh, Kaushal, and Vaibhav Gangwar</b>
    </div>
    """, 
    unsafe_allow_html=True
)


# Sidebar success message with custom style
st.sidebar.markdown("<p class='sidebar-text'>Select a demo above to get started 🚀</p>", unsafe_allow_html=True)
