import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

class DataVisualizer:
    def __init__(self, dataset_path, title):
        self.dataset_path = dataset_path
        self.title = title
        self.data = None
        self.cluster_num = None
        self.cluster_names = None
        self.dataset_exists = True

    def load_data(self):
        try:
            self.data = pd.read_csv(self.dataset_path)
        except FileNotFoundError:
            self.dataset_exists = False

    def _get_clusters(self):
        self.cluster_num = len(self.data['clusters'].unique())
        self.cluster_names = [f'Cluster {i}' for i in range(0, self.cluster_num)]

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

        # Drinking distributions
        # Create distplot with custom bin_size
        fig_drinking = make_subplots(rows=1, cols=self.cluster_num, subplot_titles=("Frequent drinkers", "Occasional drinkers", "Non-drinkers"))
        fig_frequent_drinkers = ff.create_distplot(frequent_drinkers,
                self.cluster_names,
                bin_size=[.1, .25, .5])

        fig_occasional_drinkers = ff.create_distplot(occasional_drinkers,
                self.cluster_names,
                bin_size=[.1, .25, .5])

        fig_non_drinkers = ff.create_distplot(non_drinkers,
                self.cluster_names,
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
                                width=1200,
                                margin=dict(l=50, r=50, t=50, b=50))
        
        return fig_drinking

    def _show_country_dist(self):
        fig_country = make_subplots(rows=1, 
                                    cols=self.cluster_num,
                                    specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])

        for cluster in range(0, self.cluster_num):
            cluster_data = self.data[self.data['clusters'] == cluster]
            geo_count = cluster_data['geo'].value_counts()
            fig_country.add_trace(go.Pie(labels=geo_count.index,
                                        values=geo_count.values,
                                        title=f"Cluster {cluster}"), 1, cluster + 1)

        # Update layout to show only one legend
        fig_country.update_layout(
            title_text="Country distribution in each cluster",
            showlegend=True, 
            width=1200,
            height=500
        )
        return fig_country
    
    def _show_sex(self):
        
        #Subplot for sex information
        fig_sex = make_subplots(rows=1,
                                cols=self.cluster_num,
                                specs=[[{'type':'domain'},{'type':'domain'},{'type':'domain'}]])

        # Pie charts to each subplot
        for cluster in range(0, self.cluster_num):
            cluster_data = self.data[self.data['clusters'] == cluster]
            sex_count = cluster_data['sex'].value_counts()
            fig_sex.add_trace(go.Pie(labels=sex_count.index, values=sex_count.values, title=f"Cluster {cluster}"), 1, cluster + 1)

        # Layout
        fig_sex.update_layout(
            title_text="Sex distribution in clusters",
            showlegend=True, 
            width=1200, 
            height=500
        )

        return fig_sex
    
    def _show_age(self):
        fig_age = go.Figure()

        # Add bars for each dataset
        for cluster in range(0, self.cluster_num):
            cluster_data = self.data[self.data['clusters'] == cluster]
            age_count = cluster_data['age'].value_counts()
            fig_age.add_trace(go.Bar(x=age_count.index, y=age_count.values, name=f'Cluster {cluster}'))

        # The layout for age groups
        fig_age.update_layout(
            title='Age group occurances in clusters',
            xaxis_title='Age groups',
            yaxis_title='Number of occurances',
            barmode='group',
            width=1200, 
            height=500  
        )

        return fig_age
    
    def _show_edu(self):
        colors = ['red','blue','green','orange','purple','yellow',
                  'cyan', 'magenta', 'black', 'white']
        traces = []
        for cluster in range(0, self.cluster_num):
            cluster_data = self.data[self.data['clusters'] == cluster]
            edu_count = cluster_data['isced11'].value_counts()
            traces.append(go.Bar(
                x=edu_count.index,
                y=edu_count.values,
                name=f'Cluster {cluster}',
                marker_color=colors[cluster]
            ))

        fig_edu = go.Figure(data=traces)

        # The layout for stacked bars
        fig_edu.update_layout(
            barmode='stack',
            title='Education levels in clusters',
            xaxis=dict(title='Education levels'),
            yaxis=dict(title='Number occurances'),
            height=500,
            width=1200
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
