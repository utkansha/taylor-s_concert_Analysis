import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title and Introduction
st.title("Taylor's Concert Analysis")
st.write("An exploratory data analysis on concert data to understand trends and insights from Taylor Swift's shows.")

# File Upload
st.sidebar.header("Upload your dataset")
uploaded_file = st.sidebar.file_uploader("Taylor_Train.csv", type="csv")

if uploaded_file is not None:
    # Load data
    data = pd.read_csv(uploaded_file)
    
    # Data Overview
    st.header("Data Overview")
    st.write("Here's a quick look at your data:")
    st.write(data.head())
    
    # Show basic data information
    st.subheader("Dataset Info")
    st.write(f"Number of Rows: {data.shape[0]}")
    st.write(f"Number of Columns: {data.shape[1]}")
    st.write("Summary Statistics")
    st.write(data.describe())
    
    # Data Analysis - Example Visualization
    st.header("Data Analysis & Visualization")
    st.write("Below is an example of visualizing concert-related data (e.g., attendance or ticket prices).")
    
    # Plotting Example: Histogram
    selected_column = st.selectbox("Select a column for histogram", data.columns)
    
    if pd.api.types.is_numeric_dtype(data[selected_column]):
        fig, ax = plt.subplots()
        ax.hist(data[selected_column], bins=20, color="skyblue", edgecolor="black")
        ax.set_title(f"Distribution of {selected_column}")
        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    else:
        st.write("Please select a numeric column.")

    # Further analysis based on notebook content could go here
else:
    st.write("Please upload a CSV file to begin.")

# Footer
st.sidebar.write("Taylor's Concert Analysis created with Streamlit.")
