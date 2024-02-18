# Launch the app using the following command (using the terminal):
# python -m streamlit run Home.py
import base64

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
import pickle
import time

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
    # Calculate Q1 and Q3
    Q1 = data[selected_column].quantile(0.25)
    Q3 = data[selected_column].quantile(0.75)
    IQR = Q3 - Q1

    # Define bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify points outside the bounds
    outliers = data[(data[selected_column] < lower_bound) | (data[selected_column] > upper_bound)]

    # Create a scatter plot for the entire time series
    fig = go.Figure()

    # Add a line trace for the entire time series
    fig.add_trace(go.Scatter(x=data['Discrete_Time'], y=data[selected_column], mode='lines', name='Time Series'))

    # Add scatter trace for outliers
    fig.add_trace(
        go.Scatter(x=outliers['Discrete_Time'], y=outliers[selected_column], mode='markers', marker=dict(color='red'),
                   name='Outliers'))

    # Set layout options
    fig.update_layout(showlegend=True)

    st.subheader(f"Time Series Visualization for {selected_column}:")
    st.plotly_chart(fig, use_container_width=True)

# Function to classify time series as anomaly or not
def classify_and_update_pie_chart(button, pie_chart, data, value_columns):
    # Add a button to classify time series as anomaly or not
    if button:
        # Load the model
        with open('../../saved_models/pruned_classifier_model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
            print("Model loaded successfully!")
        
        # Load and apply PCA to the time series
        with open('../../saved_models/pca_transformer.pkl', 'rb') as pca_file:
            pca = pickle.load(pca_file)
            print("PCA loaded successfully!")
            principalComponents = pca.transform(data[value_columns])
            principalDf = pd.DataFrame(data = principalComponents, columns = ['principal_component_1', 'principal_component_2'])

        # Predict anomalies using principal components 1 and 2
        predictions = model.predict(principalDf)
        
        # Calculate the percentage of anomalies
        percentage_anomalies = (predictions == "guasto").sum() / len(predictions) * 100

        # Display pie chart
        pie_chart.update_traces(values=[percentage_anomalies, 100 - percentage_anomalies])

LOGO_IMAGE = "images/logo_sentry_transparent.png"
LOGO_TITLE = "T-Sentry"
UNICAM_LOGO = "images/logo_unicam.png"
SCHNELL_LOGO = "images/logo_Schnell.png"

st.set_page_config(page_title="T-Sentry", page_icon="📈", layout="wide")

# Create a Streamlit sidebar for navigation
st.sidebar.header("Home")

st.markdown(
    """
    <style>
    .headerContainer {
        display: flex;
        justify-content: space-between;
    }
    .logoContainer {
        display: flex;
        align-items: center;
    }
    .companiesContainer {
        display: flex;
        flex-direction: column;
        align-items: center; /* Center items horizontally */
        text-align: center; /* Center text horizontally */
    }
    .title-logo-text {
        font-weight: 700 !important;
        font-size: 70px !important;
        padding-top: 0px;
        margin-bottom: 0px;
    }
    .title-logo-img {
        width: 150px;
        height: 150px;
    }
    .company-logo-img {
        max-height: 100px; 
        width: auto;
        margin-bottom: 10px; 
    }
    .collaboration-text {
        font-size: 25px; 
        margin-bottom: 5px; 
        text-align: center; 
    }
    .statistics-container {
        display: flex;
        flex-direction: column;
        border: 1px solid #d3d3d3;
        padding: 10px;
        padding-left: 30px;
        margin-top: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    .sidebar-container {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        margin: 5px 0;
        cursor: pointer;
        border: none;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="headerContainer">
        <div class="logoContainer">
            <img class="title-logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
            <p class="title-logo-text">{LOGO_TITLE}</p>
        </div>
        <div class="companiesContainer">
            <p class="collaboration-text">In collaboration with:</p>
            <div>
                <img class="company-logo-img" src="data:image/png;base64,{base64.b64encode(open(UNICAM_LOGO, "rb").read()).decode()}">
                <img class="company-logo-img" src="data:image/png;base64,{base64.b64encode(open(SCHNELL_LOGO, "rb").read()).decode()}">
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# File upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Divide the space into two columns
col1, col2 = st.columns([2, 1], gap="large")

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file, sep=";")
    dff = df.copy()

    # Value columns of the dataframe to be used
    value_columns = ['Board1Acc1', 'Board1Acc2', 'Board1Acc3',
                'Board2Acc1', 'Board2Acc2', 'Board2Acc3',
                'Board3Acc1', 'Board3Acc2', 'Board3Acc3']

    # Visualize time series
    with col1:
        st.subheader("Time Series Visualization:")
        # Allow user to choose the column to visualize
        selected_column = st.selectbox("Select a column to visualize", value_columns)

        # Visualize time series
        visualize_time_series(dff, selected_column)

# Classify data
if uploaded_file is not None:
    # On the second column add the classifier and the button to classify the time series
    with col2:
        st.subheader("Classify Time Series:")

        # Create a button to trigger classification
        classify_button = st.button("Classify Time Series")

        # Create an initially empty pie chart
        pie_chart = go.Figure(go.Pie(labels=['Anomalies', 'Normal'], values=[0, 100], hole=0.3, marker_colors=['#FF6347', '#4CAF50']))
        pie_chart.update_layout(width=300, height=300)

        st.subheader("Time Series Classification")

        # Perform classification and update the pie chart
        classify_and_update_pie_chart(classify_button, pie_chart, dff, value_columns)

        # Display the pie chart
        st.plotly_chart(pie_chart, use_container_width=True)
        
        st.subheader("Time Series Statistics")
        st.markdown(
            f"""
            <div class="statistics-container">
                <p>Selected Column: {selected_column}</p>
                <p>Mean: {dff[selected_column].mean()}</p>
                <p>Variance: {dff[selected_column].var()}</p>
                <p>Minimum: {dff[selected_column].min()}</p>
                <p>Maximum: {dff[selected_column].max()}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Decompose time series into trend and residual components
if uploaded_file is not None:
    st.divider()
    st.subheader(f"Decomposed Time Series for {selected_column}:")
    decompose_and_display(dff, selected_column)