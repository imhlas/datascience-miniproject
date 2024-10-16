import streamlit as st
from visualizer import DataVisualizer

# navigation bar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a dataset", ["Education", "Income", "Urbanisation"])

# logic for changing page and dataset
if page == "Education":
    visualizer = DataVisualizer('../data/clusters/freq_education_clusters.csv', "Education dataset")
    visualizer.load_data()
    visualizer.show_visualizations()
elif page == "Income":
    visualizer = DataVisualizer('../data/clusters/freq_income_clusters.csv', "Income dataset")
    visualizer.load_data()
    visualizer.show_visualizations()
elif page == "Urbanisation":
    visualizer = DataVisualizer('../data/clusters/freq_urbanisation_clusters.csv', "Urbanisation dataset")
    visualizer.load_data()
    visualizer.show_visualizations()

