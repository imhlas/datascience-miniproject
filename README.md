# Alcohol Consumption Insights in EU

This mini-project was carried out as part of the "Introduction to Data Science" course at the University of Helsinki. The project focuses on analyzing alcohol consumption patterns in EU countries using various data science techniques.

A link to the web application can be found here: https://alcoholconsumptionineu.streamlit.app/.

The codebase consists of four folders:
- data: contains three types of datasets:
  - datasets_raw: original datasets from https://ec.europa.eu/eurostat/web/health/database under sections (Detailed datasets/Health/Health determinants/Alcohol consumption), each of the files ending in _al1e, _al1i and _al1u.
  - datasets_clean: contains the data after processing (beware of empty rows, those with 0.0 frequencies in all three columns Frequent drinkers,Non-drinkers,Occasional drinkers)
  - clusters: contains our clustering of the cleaned datasets, after dropping empty rows.
- sandbox: contains the notebooks were we tested code.
- main: contains the code for loading, modifying and clustering the data. Everything can be run using the backend.py file. One may edit the flags in get_clusters to get different data.
- pages: contains the streamlit app, that is the frontend. It is run with:
`$ streamlit run <YOUR FOLDER>/datascience-miniproject/pages/app.py`

Everything works at least in python 3.10.12, using a virtual environment as explained in https://docs.python.org/3/library/venv.html.

After creating and activating the environment, which is done to avoid dependency conflicts, install the required packages running `$ pip install kneed streamlit plotly kmodes`.