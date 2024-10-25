import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import re

class DataVisualizer:
    def __init__(self, dataset_path, title):
        self.dataset_path = dataset_path
        self.title = title
        self.data = None
        self.cluster_num = None
        self.cluster_names = None
        self.dataset_exists = True
        self.specs = None

    def load_data(self):
        try:
            self.data = pd.read_csv(self.dataset_path, delimiter=';')
        except FileNotFoundError:
            self.dataset_exists = False

    def _get_clusters(self):
        self.cluster_num = len(self.data['clusters'].unique())
        self.cluster_names = [f'Cluster {i}' for i in range(0, self.cluster_num)]
        self.specs = [[{'type': 'domain'} for _ in range(self.cluster_num)]]
        
    def _get_drinking_habit_lists(self):
        frequent_drinkers, occasional_drinkers, non_drinkers = [], [], []

        for cluster in range(0, self.cluster_num):
            cluster_data = self.data[self.data['clusters'] == cluster]
            frequent_drinkers.append(cluster_data.loc[:, 'Frequent drinkers'])
            occasional_drinkers.append(cluster_data.loc[:, 'Occasional drinkers'])
            non_drinkers.append(cluster_data.loc[:, 'Non-drinkers'])

        return frequent_drinkers, occasional_drinkers, non_drinkers

    def _show_dist_plot(self):
        frequent_drinkers, occasional_drinkers, non_drinkers = self._get_drinking_habit_lists()

        # Create a combined distplot with subplots
        fig_drinking = make_subplots(
            rows=1, 
            cols=3, 
            subplot_titles=("Frequent drinkers", "Occasional drinkers", "Non-drinkers"),
            shared_yaxes=True  # Shared y-axis to have one legend
        )

        # Maintain the same bin size for all clusters
        bin_sizes = [.1, .25, .5, .75]
        fig_frequent_drinkers = ff.create_distplot(frequent_drinkers, self.cluster_names, bin_size=bin_sizes)
        fig_occasional_drinkers = ff.create_distplot(occasional_drinkers, self.cluster_names, bin_size=bin_sizes)
        fig_non_drinkers = ff.create_distplot(non_drinkers, self.cluster_names, bin_size=bin_sizes)

        # Extract traces and ensure the legend is added only once
        for idx, trace in enumerate(fig_frequent_drinkers['data']):
            trace.showlegend = True if idx < self.cluster_num else False 
            fig_drinking.add_trace(trace, row=1, col=1)

        for trace in fig_occasional_drinkers['data']:
            trace.showlegend = False  
            fig_drinking.add_trace(trace, row=1, col=2)

        for trace in fig_non_drinkers['data']:
            trace.showlegend = False 
            fig_drinking.add_trace(trace, row=1, col=3)

        # Manually set the y-axis range (choose a suitable max value)
        fig_drinking.update_yaxes(range=[0, 1.1])

        # Update layout to show one unified legend
        fig_drinking.update_layout(
            showlegend=True,  # Show one legend for the entire figure
            title_text="Drinking Behavior by Cluster",
            height=500,
            width=1200,
            margin=dict(l=50, r=50, t=50, b=50),
            font=dict(size=14)
        )

        return fig_drinking

    def _show_country_dist(self):
        fig_country = make_subplots(
            rows=1, 
            cols=self.cluster_num,
            specs=self.specs
        )

        for cluster in range(0, self.cluster_num):
            cluster_data = self.data[self.data['clusters'] == cluster]
            geo_count = cluster_data['geo'].value_counts()

            # Select top 10 countries
            top_10_countries = geo_count.nlargest(10)
            top_10_sum = top_10_countries.sum()

            # Add 'Others' as the rest of the countries
            others_value = geo_count.sum() - top_10_sum
            labels = top_10_countries.index.tolist() + ['Others']
            values = top_10_countries.tolist() + [others_value]

            # Create the pie chart for this cluster
            fig_country.add_trace(go.Pie(labels=labels,
                                        values=values,
                                        title=f"Cluster {cluster}"), 
                                        1, cluster + 1)

        # Update layout to show only one legend
        fig_country.update_layout(
            title_text="Country distribution (Top 10 + Others) in each cluster",
            showlegend=True, 
            width=1200,
            height=500,
            font=dict(size=14)
        )
        
        return fig_country

    
    def _show_sex(self):
        
        #Subplot for sex information
        fig_sex = make_subplots(rows=1,
                                cols=self.cluster_num,
                                specs=self.specs)

        # Pie charts to each subplot
        for cluster in range(0, self.cluster_num):
            cluster_data = self.data[self.data['clusters'] == cluster]
            sex_count = cluster_data['sex'].value_counts()
            fig_sex.add_trace(go.Pie(labels=sex_count.index,
                                    values=sex_count.values,
                                    title=f"Cluster {cluster}"), 1, cluster + 1)

        # Layout
        fig_sex.update_layout(
            title_text="Sex distribution in clusters",
            showlegend=True, 
            width=1200, 
            height=500,
            font=dict(size=14)
        )

        return fig_sex
    

    def _show_age(self):
        fig_age = go.Figure()

        # Helper function to extract the starting age as an integer
        def extract_starting_age(age_group):
            match = re.search(r'(\d+)', age_group)
            if match:
                return int(match.group(1)) 
            else:
                return float('inf') 

        # Add bars for each dataset
        for cluster in range(0, self.cluster_num):
            cluster_data = self.data[self.data['clusters'] == cluster]
            age_count = cluster_data['age'].value_counts()

            # Sort age groups by the starting age extracted
            sorted_age_count = age_count.sort_index(key=lambda x: x.map(extract_starting_age))

            # Add trace for the sorted data
            fig_age.add_trace(go.Bar(x=sorted_age_count.index, y=sorted_age_count.values, name=f'Cluster {cluster}'))

        # The layout for age groups
        fig_age.update_layout(
            title='Age group occurrences in clusters',
            yaxis_title='Number of occurrences',
            barmode='group',
            width=1200, 
            height=500  
        )

        return fig_age

    
    def _show_edu(self):
        # Define the full names and corresponding shorter names for display
        education_levels_order = [
            "Less than primary, primary and lower secondary education (levels 0-2)",
            "Upper secondary and post-secondary non-tertiary education (levels 3 and 4)",
            "Tertiary education (levels 5-8)"
        ]

        education_levels_short = [
            "Primary/Lower Sec (levels 0-2)",
            "Upper Sec/Post-sec (levels 3-4)",
            "Tertiary (levels 5-8)"
        ]

        # Create subplots
        fig_edu = make_subplots(
            rows=1, cols=self.cluster_num,
            subplot_titles=[f"Cluster {i}" for i in range(self.cluster_num)]
        )

        colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow',
                'cyan', 'magenta', 'black', 'white']

        # Add a bar chart for each cluster in a separate subplot
        for cluster in range(0, self.cluster_num):
            cluster_data = self.data[self.data['clusters'] == cluster]
            edu_count = cluster_data['isced11'].value_counts()

            # Reindex edu_count to ensure all categories are present
            edu_count = edu_count.reindex(education_levels_order, fill_value=0)

            # Add trace to the specific subplot for this cluster
            fig_edu.add_trace(go.Bar(
                x=edu_count.index,
                y=edu_count.values,
                marker_color=colors[cluster],
                name=f'Cluster {cluster}'
            ), row=1, col=cluster + 1)

        # Update layout for the figure
        fig_edu.update_layout(
            title='Education levels by cluster',
            yaxis_title='Number of occurrences',
            showlegend=False, 
            height=500,
            width=1200
        )

        # Lock the x-axis categories in the specified order and rotate the labels
        for i in range(1, self.cluster_num + 1):
            fig_edu.update_xaxes(
                categoryorder='array', 
                categoryarray=education_levels_order,
                tickvals=education_levels_order,  # Use full names as values
                ticktext=education_levels_short,  # Show shortened names
                tickangle=-45,  # Rotate the labels by 45 degrees
                row=1, col=i
            )

        return fig_edu



    def show_visualizations(self):
        # Streamlit app layout
        st.title(self.title)

        # show error if dataset was not found
        if not self.dataset_exists:
            st.error("Dataset not found")
            return

        self._get_clusters()

        fig_drinking = self._show_dist_plot()
        fig_country = self._show_country_dist()
        fig_sex = self._show_sex()
        fig_age = self._show_age()
        
        st.plotly_chart(fig_drinking)
        st.plotly_chart(fig_country)
        st.plotly_chart(fig_sex)
        st.plotly_chart(fig_age)
        
        if self.title == 'Education dataset':
            fig_edu = self._show_edu()
            st.plotly_chart(fig_edu)
