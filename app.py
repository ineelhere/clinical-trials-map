import streamlit as st
from map_utils import *
from streamlit_folium import folium_static


st.title("Clinical Trials Locator 🌐")
condition = st.text_input("Enter a medical condition:", placeholder="Glioblastoma")
location = st.text_input("Enter a location:", placeholder="Kolkata")

if st.button("Find Clinical Trial Sites 🔍"):
    condition_input = condition.strip().lower() if condition else ""
    location_input = location.strip().lower() if location else ""
    
    if condition_input or location_input:
        map_ = myfunc(condition_input, location_input)
        if map_:
            folium_static(map_)
        else:
            st.error("No clinical trials found for the given condition and/or location.")
    else:
        st.error("Please provide at least a medical condition or a location.")
