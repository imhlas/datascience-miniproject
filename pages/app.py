import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Load the CSV data
data = pd.read_csv('data/clusters/freq_education_clusters.csv')

# Get unique values from the columns for dropdowns
age = data['age'].unique()
geo = data['geo'].unique()
edu = data['isced11'].unique()
sex = data['sex'].unique()

# Streamlit app layout
st.title("Dropdown Selection from CSV")

# Dropdowns for each column
selected_age = st.selectbox("Select Age:", age)
selected_sex = st.selectbox("Select Sex:", sex)
selected_edu = st.selectbox("Select Education:", edu)

filtered_df = data[
    (data['age'] == selected_age) &
    (data['sex'] == selected_sex) &
    (data['isced11'] == selected_edu)
]

country_clusters = filtered_df[['geo', 'clusters']]

# Load the European countries shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Filter for Europe
europe = world[(world['continent'] == 'Europe')]

europe = europe.merge(country_clusters, how='left', left_on='name', right_on='geo')

# Create a Folium map centered in Europe
m = folium.Map(location=[54, 15], zoom_start=4)

# Function to color the countries based on clusters
def color_clusters(cluster):
    if pd.isna(cluster):
        return 'lightgrey'
    cluster_colors = {
        1: 'pink',   
        2: 'blue',  
        0: 'red',  
    }
    return cluster_colors.get(cluster, 'lightgrey')

# Add countries to the map with color based on their cluster
for _, row in europe.iterrows():
    # Get country boundaries
    if row['geometry'] is not None:
        # Simplify geometry to speed up rendering
        geo_json = row['geometry'].simplify(0.01)
        # Define country style
        style = {'fillColor': color_clusters(row['clusters']),
                 'color': 'black', 'weight': 1.5, 'fillOpacity': 0.6}
        # Add to the folium map
        folium.GeoJson(geo_json, style_function=lambda x, style=style: style, 
                       tooltip=row['name']).add_to(m)

# Display the map in Streamlit
st_folium(m, width=700, height=500)