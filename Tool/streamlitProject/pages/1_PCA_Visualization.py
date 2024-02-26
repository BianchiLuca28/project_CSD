import streamlit as st
import pandas as pd
import pickle
import plotly.express as px

# Compute PCA components
def compute_pca(data):
    # Load and apply PCA to the time series
    with open('saved_models/pca_transformer.pkl', 'rb') as pca_file:
        pca = pickle.load(pca_file)
        principalComponents = pca.transform(data[value_columns])
        principalDf = pd.DataFrame(data = principalComponents, columns = ['principal_component_1', 'principal_component_2'])
        principalDf['prediction'] = "no_guasto"

    return principalDf


st.set_page_config(page_title="PCA Visualization", page_icon="📈", layout="wide")

st.session_state.update(st.session_state)

value_columns = ['Board1Acc1', 'Board1Acc2', 'Board1Acc3',
                'Board2Acc1', 'Board2Acc2', 'Board2Acc3',
                'Board3Acc1', 'Board3Acc2', 'Board3Acc3']

st.sidebar.header("PCA Visualization")

st.title("PCA Visualization Tool")

st.write("This tool allows you to visualize the principal components of the time series data.")

# File upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file, sep=";")
    dff = df.copy()

    # Save the dataset to a session variable
    st.session_state['data'] = dff

if 'data' in st.session_state:
    dff = st.session_state['data']
    principalDf = compute_pca(dff)
    
    if 'predictions' in st.session_state and uploaded_file == st.session_state['file_classified']:
        predictions = st.session_state['predictions']
        principalDf['prediction'] = predictions

    # Plot the principal components
    fig = px.scatter(principalDf, x="principal_component_1", y="principal_component_2", title="Principal Components", 
                     color='prediction', labels={'principal_component_1': 'Principal Component 1', 'principal_component_2': 'Principal Component 2'}, 
                    color_discrete_map={"no_guasto": "#6ABDFF", "guasto": "#FF6A6A"})
    fig.for_each_trace(lambda t: t.update(name='Not Outlier' if t.name == 'no_guasto' else 'Outlier'))
    fig.update_layout(height=850)

    st.plotly_chart(fig, use_container_width=True, height=800)
else:
    st.write("Please upload a CSV file to visualize the principal components.")