# Launch the app using the following command (using the terminal):
# python -m streamlit run app.py


import streamlit as st
import pandas as pd

# Function to load and visualize time series data
def visualize_time_series(data):
    st.line_chart(data, width=100, height=0)

# Streamlit app
def main():
    # Page title
    st.title("Time Series Visualization App")

    # File upload
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Load data
        df = pd.read_csv(uploaded_file, sep=";")
        dff = df.copy()

        dff = dff['Board1Acc1']

        # Display the first few rows of the dataset
        st.subheader("Data Preview:")
        st.write(df.head())

        # Visualize time series
        st.subheader("Time Series Visualization:")
        visualize_time_series(dff)

if __name__ == "__main__":
    main()