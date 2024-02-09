# Launch the app using the following command (using the terminal):
# python -m streamlit run app.py


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Function to load and visualize time series data with Plotly
def visualize_time_series(data):
    # Create a scatter plot for the entire time series
    fig = go.Figure()

    # Add a line trace for the entire time series
    fig.add_trace(go.Scatter(x=data['Discrete_Time'], y=data['Board1Acc1'], mode='lines', name='Time Series'))

    # Identify points lower than 0.85 and higher than 1.05
    below_threshold = data[data['Board1Acc1'] < 0.83]
    above_threshold = data[data['Board1Acc1'] > 1.075]

    # Add scatter traces for points below 0.85 and above 1.05
    fig.add_trace(go.Scatter(x=below_threshold['Discrete_Time'], y=below_threshold['Board1Acc1'], mode='markers', marker=dict(color='red'), name='Below 0.83'))
    fig.add_trace(go.Scatter(x=above_threshold['Discrete_Time'], y=above_threshold['Board1Acc1'], mode='markers', marker=dict(color='red'), name='Above 1.075'))

    # Set layout options
    fig.update_layout(title='Time Series Visualization', width=800, showlegend=True)

    st.plotly_chart(fig, use_container_width=True)

# Streamlit app
def main():
    # Set page configuration to make the interface wider
    st.set_page_config(page_title="Time Series App", page_icon="📈", layout="wide")

    # Page title
    st.title("Time Series Visualization App")

    # File upload
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Load data
        df = pd.read_csv(uploaded_file, sep=";")
        dff = df.copy()

        dff = dff[['Discrete_Time', 'Board1Acc1']]

        # Display the first few rows of the dataset
        st.subheader("Data Preview:")
        st.write(df.head())

        # Visualize time series
        st.subheader("Time Series Visualization:")
        visualize_time_series(dff)

if __name__ == "__main__":
    main()