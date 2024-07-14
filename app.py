import streamlit as st
from map_utils import *
from streamlit_folium import folium_static

st.title("Clinical Trials Locator 🌐")

# Create columns for inputs
col1, col2, col3 = st.columns([1, 1, 1])

# Input fields
with col1:
    condition = st.text_input("Enter a medical condition:", placeholder=" Glioblastoma")

with col2:
    location = st.text_input("Enter a location:", placeholder=" Kolkata")

with col3:
    pagesize = st.number_input("Number of pages of results to display:", value=10, step=1)

# Button to trigger search
if st.button("Find Clinical Trial Sites 🔍"):
    condition_input = condition.strip().lower() if condition else ""
    location_input = location.strip().lower() if location else ""
    
    if condition_input or location_input:
        # Call your function to get the map
        map_ = myfunc(condition_input, location_input, pagesize)
        
        if map_:
            folium_static(map_)
        else:
            st.error("No clinical trials found for the given condition and/or location.")
    else:
        st.error("Please provide at least a medical condition or a location.")
