import streamlit as st
from visualizer import DataVisualizer
import sys
sys.path.append('../')


# navigation bar

st.set_page_config(layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a dataset", ["Education", "Income", "Urbanisation"])

# logic for changing page and dataset
if page == "Education":
    visualizer = DataVisualizer('data/clusters/education_clusters.csv', "Alcohol consumption frequency clusters in Europe\nEducation dataset")
    visualizer.load_data()
    visualizer.show_visualizations()
elif page == "Income":
    visualizer = DataVisualizer('data/clusters/income_clusters.csv', "Alcohol consumption frequency clusters in Europe\nIncome dataset")
    visualizer.load_data()
    visualizer.show_visualizations()
elif page == "Urbanisation":
    visualizer = DataVisualizer('data/clusters/urbanisation_clusters.csv', "Alcohol consumption frequency clusters in Europe\nUrbanisation dataset")
    visualizer.load_data()
    visualizer.show_visualizations()