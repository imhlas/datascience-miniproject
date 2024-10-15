import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff

# Load the CSV data
data = pd.read_csv('data/clusters/freq_education_clusters.csv')

# Streamlit app layout
st.title("Education dataset")

# Drinking distributions
# Create distplot with custom bin_size

fig_drinking = make_subplots(rows=1, cols=3, subplot_titles=("Frequent drinkers", "Occasional drinkers", "Non-drinkers"))

fig_frequent_drinkers = ff.create_distplot(
        [data[data['clusters'] == 0].loc[:, 'Frequent drinkers'], 
         data[data['clusters'] == 1].loc[:, 'Frequent drinkers'],
         data[data['clusters'] == 2].loc[:, 'Frequent drinkers']],
        ['Cluster 1', 'Cluster 2', 'Cluster 3'],
        bin_size=[.1, .25, .5])

fig_occasional_drinkers = ff.create_distplot(
        [data[data['clusters'] == 0].loc[:, 'Occasional drinkers'], 
         data[data['clusters'] == 1].loc[:, 'Occasional drinkers'],
         data[data['clusters'] == 2].loc[:, 'Occasional drinkers']],
        ['Cluster 1', 'Cluster 2', 'Cluster 3'],
        bin_size=[.1, .25, .5])

fig_non_drinkers = ff.create_distplot(
        [data[data['clusters'] == 0].loc[:, 'Non-drinkers'], 
         data[data['clusters'] == 1].loc[:, 'Non-drinkers'],
         data[data['clusters'] == 2].loc[:, 'Non-drinkers']],
        ['Cluster 1', 'Cluster 2', 'Cluster 3'],
        bin_size=[.1, .25, .5])

# Extract traces from each distplot and add to the subplot figure
for trace in fig_frequent_drinkers['data']:
    fig_drinking.add_trace(trace, row=1, col=1)

for trace in fig_occasional_drinkers['data']:
    fig_drinking.add_trace(trace, row=1, col=2)

for trace in fig_non_drinkers['data']:
    fig_drinking.add_trace(trace, row=1, col=3)

# Update layout
fig_drinking.update_layout(showlegend=True,
                           title_text="Drinking Behavior by Cluster",
                           height=500,
                           width=1200)


def get_static_count(cluster_data):
    geo_count = cluster_data['geo'].value_counts()
    sex_count = cluster_data['sex'].value_counts()
    age_count = cluster_data['age'].value_counts()
    edu_count = cluster_data['isced11'].value_counts()

    return geo_count, sex_count, age_count, edu_count


clust_0_geo, clust_0_sex, clust_0_age, clust_edu_0 = get_static_count(data[data['clusters'] == 0])
clust_1_geo, clust_1_sex, clust_1_age, clust_edu_1 = get_static_count(data[data['clusters'] == 1])
clust_2_geo, clust_2_sex, clust_2_age, clust_edu_2 = get_static_count(data[data['clusters'] == 2])

# Subplot for country information
fig_country = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])

# Add pie charts to each subplot
fig_country.add_trace(go.Pie(labels=clust_0_geo.index, values=clust_0_geo.values, title="Cluster 1"), 1, 1)
fig_country.add_trace(go.Pie(labels=clust_1_geo.index, values=clust_1_geo.values, title="Cluster 2"), 1, 2)
fig_country.add_trace(go.Pie(labels=clust_1_geo.index, values=clust_2_geo.values, title="Cluster 3"), 1, 3)

# Update layout to show only one legend
fig_country.update_layout(
    title_text="Country distribution in each cluster ",
    showlegend=True, 
    width=1200,
    height=500
)

#Subplot for sex information
fig_sex = make_subplots(rows=1,
                        cols=3,
                        specs=[[{'type':'domain'},{'type':'domain'},{'type':'domain'}]])

# Pie charts to each subplot
fig_sex.add_trace(go.Pie(labels=clust_0_sex.index, values=clust_0_sex.values, title="Cluster 1"), 1, 1)
fig_sex.add_trace(go.Pie(labels=clust_1_sex.index, values=clust_1_sex.values, title="Cluster 2"), 1, 2)
fig_sex.add_trace(go.Pie(labels=clust_1_sex.index, values=clust_2_sex.values, title="Cluster 3"), 1, 3)

# Layout
fig_sex.update_layout(
    title_text="Sex distribution in clusters",
    showlegend=True, 
    width=1200, 
    height=500
)

# Combined barchart with age information
# Create the bar chart
fig_age = go.Figure()

# Add bars for each dataset (Chart 1, Chart 2, Chart 3)
fig_age.add_trace(go.Bar(x=clust_0_age.index, y=clust_0_age.values, name='Cluster 1'))
fig_age.add_trace(go.Bar(x=clust_1_age.index, y=clust_1_age.values, name='Cluster 2'))
fig_age.add_trace(go.Bar(x=clust_2_age.index, y=clust_2_age.values, name='Cluster 3'))

# The layout for age groups
fig_age.update_layout(
    title='Age group occurances in clusters',
    xaxis_title='Age groups',
    yaxis_title='Number of occurances',
    barmode='group',  # Group bars by category
    width=1200,  # Set figure width
    height=500  # Set figure height
)

# Education
# Create traces for each cluster
trace1 = go.Bar(
    x=clust_edu_0.index,
    y=clust_edu_0.values,
    name='Cluster 1',
    marker_color='blue'
)

trace2 = go.Bar(
    x=clust_edu_1.index,
    y=clust_edu_1.values,
    name='Cluster 2',
    marker_color='green'
)

trace3 = go.Bar(
    x=clust_edu_2.index,
    y=clust_edu_1.values,
    name='Cluster 3',
    marker_color='red'
)

# Create the figure with stacked bars
fig_edu = go.Figure(data=[trace1, trace2, trace3])

# The layout for stacked bars
fig_edu.update_layout(
    barmode='stack',
    title='Education levels in clusters',
    xaxis=dict(title='Education levels'),
    yaxis=dict(title='Number occurances'),
    height=500,
    width=1200
)

# Display the map in Streamlit
st.plotly_chart(fig_drinking)
st.plotly_chart(fig_country)
st.plotly_chart(fig_sex)
st.plotly_chart(fig_age)
st.plotly_chart(fig_edu)


