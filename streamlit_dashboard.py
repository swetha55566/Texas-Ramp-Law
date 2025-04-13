import streamlit as st
import pandas as pd

data = pd.DataFrame({
    'Permit ID': ['001', '002'],
    'Violation': ['Slope too steep', 'Width too narrow'],
    'Latitude': [33.215, 33.234],
    'Longitude': [-97.133, -97.145]
})

st.title(" Ramp Law Compliance Dashboard")
st.map(data.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'}))
st.write(" Violation Details:")
st.dataframe(data)