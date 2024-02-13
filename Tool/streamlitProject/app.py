# Launch the app using the following command (using the terminal):
# python -m streamlit run app.py


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
import pickle

# from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

# Function to decompose time series and display sub-time series
def decompose_and_display(data, selected_column):
    # Set 'time' as index for seasonal decomposition
    data.set_index('Discrete_Time', inplace=True)

    # Decompose time series into trend, seasonal, and residual components
    result = seasonal_decompose(data[selected_column], model='additive', period=10)  # Assuming seasonality period is 12

    # Create a new DataFrame with decomposed components
    decomposed_data = pd.DataFrame({
        'Original': data[selected_column],
        'Trend': result.trend,
        'Residual': result.resid
    })

    # Plot each sub-time series
    fig = go.Figure()

    for column in decomposed_data.columns:
        fig.add_trace(go.Scatter(x=decomposed_data.index, y=decomposed_data[column], mode='lines', name=column))

    # Set layout options
    fig.update_layout(showlegend=True)

    st.plotly_chart(fig, use_container_width=True)

# Function to load and visualize time series data with Plotly
def visualize_time_series(data, selected_column):
    # Create a scatter plot for the entire time series
    fig = go.Figure()

    # Add a line trace for the entire time series
    fig.add_trace(go.Scatter(x=data['Discrete_Time'], y=data[selected_column], mode='lines', name='Time Series'))

    # Identify points lower than 0.85 and higher than 1.05
    below_threshold = data[data[selected_column] < 0.83]
    above_threshold = data[data[selected_column] > 1.075]

    # Add scatter traces for points below 0.85 and above 1.05
    fig.add_trace(go.Scatter(x=below_threshold['Discrete_Time'], y=below_threshold[selected_column], mode='markers', marker=dict(color='red'), name='Below 0.83'))
    fig.add_trace(go.Scatter(x=above_threshold['Discrete_Time'], y=above_threshold[selected_column], mode='markers', marker=dict(color='red'), name='Above 1.075'))

    # Set layout options
    fig.update_layout(width=800, showlegend=True)
    
    st.subheader(f"Time Series Visualization for {selected_column}:")
    st.plotly_chart(fig, use_container_width=True)


# Set page configuration to make the interface wider
st.set_page_config(page_title="T-Sentry", page_icon="📈", layout="wide")

# Page title
st.title("T-Sentry")

# File upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Divide the space into two columns
col1, col2 = st.columns(2)

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file, sep=";")
    dff = df.copy()

    # Value columns of the dataframe
    value_columns = dff.columns.to_list()
    value_columns.remove('Acquisition_Number')
    value_columns.remove('Discrete_Time')

    # Visualize time series
    with col1:
        st.subheader("Time Series Visualization:")
        # Allow user to choose the column to visualize
        selected_column = st.selectbox("Select a column to visualize", value_columns)

        # Visualize time series
        visualize_time_series(dff, selected_column)

# Classify data
if uploaded_file is not None:
    with col2:
        st.subheader("Classify Time Series:")
        with open('../../saved_models/pruned_classifier_model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
            print("Model loaded successfully!")
            print(model)
        
        # Add a button to classify time series as anomaly or not
        if st.button("Predict Anomalies"):
            # Predict anomalies
            predictions = model.predict(dff)

            # Display predictions
            st.subheader("Anomaly Predictions:")
            st.write(predictions)
        
        # Display statistics on the main page in a styled container
        st.markdown("## Time Series Statistics", unsafe_allow_html=True)
        st.markdown(f"**Selected Column:** {selected_column}")
        st.markdown(f"**Mean:** {df[selected_column].mean()}")
        st.markdown(f"**Variance:** {df[selected_column].var()}")
        st.markdown(f"**Minimum:** {df[selected_column].min()}")
        st.markdown(f"**Maximum:** {df[selected_column].max()}")
        # Add more statistics as needed

# Decompose time series
if uploaded_file is not None:
    st.subheader(f"Decomposed Time Series for {selected_column}:")
    decompose_and_display(dff, selected_column)


# TODO
# 1. Load the model correctly
# 2. Adjust the thresholds for the points classified as anomalies
# 3. Display statistics on the main page in a styled container
