import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Data Analysis and Plotting", layout="wide")

# Sidebar for navigation between pages
page = st.sidebar.radio("Select a page:", ["Data Analysis", "Plotting"])

# Data Analysis Page
if page == "Data Analysis":
    # Set title
    st.title("Data Analysis App")
    st.text("A simple data analysis app created by Muhammad Hassaan.")

    # Sidebar for Data Analysis functionalities
    st.sidebar.subheader("Data Analysis Options")
    dataset_name = st.sidebar.selectbox("Select Dataset", ("Iris", "titanic", "tips", "flights", "diamonds"))
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "xls"])

    # Read the dataset
    if dataset_name == "Iris":
        data = sns.load_dataset("iris")
    elif dataset_name == "titanic":
        data = sns.load_dataset("titanic")
    elif dataset_name == "tips":
        data = sns.load_dataset("tips")
    elif dataset_name == "flights":
        data = sns.load_dataset("flights")
    elif dataset_name == "diamonds":
        data = sns.load_dataset("diamonds")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    
    # Display dataset
    st.write("Your Selected Dataset:")
    st.write(data)

    # Display dataset shape
    st.write("Shape of Dataset:")
    st.write(f"There are {data.shape[0]} rows and {data.shape[1]} columns.")

    # Display dataset description
    st.write("Description of Dataset:")
    st.write(data.describe())

    # Display the column names of selected dataset with data types
    st.write("Column Names and Data Types:")
    st.write(data.dtypes)

    # Calculate null values and their percentages
    null_counts = data.isnull().sum()
    null_percentages = (null_counts / data.shape[0]) * 100

    # Create a DataFrame to display the results
    null_summary = pd.DataFrame({
        'Null Values': null_counts,
        'Percentage of Nulls (%)': null_percentages
    })

    # Display the summary
    st.write("Missing Values:")
    st.write(null_summary)


# Plotting Page
elif page == "Plotting":
    st.title("Data Visualization")

    # Sidebar for Data Visualization
    st.sidebar.subheader("Data Visualization")
    dataset_name = st.sidebar.selectbox("Select Dataset", ("Iris", "titanic", "tips", "flights", "diamonds"))
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "xls"])

    # Read the dataset
    if dataset_name == "Iris":
        data = sns.load_dataset("iris")
    elif dataset_name == "titanic":
        data = sns.load_dataset("titanic")
    elif dataset_name == "tips":
        data = sns.load_dataset("tips")
    elif dataset_name == "flights":
        data = sns.load_dataset("flights")
    elif dataset_name == "diamonds":
        data = sns.load_dataset("diamonds")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

    if 'data' in locals():  # Check if 'data' is defined
        # Encode categorical columns
        categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
        if categorical_cols:
            st.sidebar.subheader("Encoding Options")
            encoding_method = st.sidebar.selectbox("Select Encoding Method", ["One-Hot Encoding", "Label Encoding"])

            if encoding_method == "One-Hot Encoding":
                data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)
            elif encoding_method == "Label Encoding":
                from sklearn.preprocessing import LabelEncoder
                for col in categorical_cols:
                    le = LabelEncoder()
                    data[col] = le.fit_transform(data[col])

        # Dropdown for selecting X and Y columns
        x_column = st.sidebar.selectbox("Select X-axis", data.columns)
        y_column = st.sidebar.selectbox("Select Y-axis", data.columns)

        # Dropdown for selecting plot type
        plot_type = st.sidebar.selectbox("Select Plot Type", [
            "Scatter Plot", "Bar Plot", "Box Plot", "Line Plot", 
            "Histogram", "Area Plot", "Violin Plot", "Pie Chart", 
            "Strip Plot", "Bubble Chart", "Correlation Heatmap"
        ])

        if st.sidebar.button("Generate Plot"):
            if plot_type == "Scatter Plot":
                fig = px.scatter(data, x=x_column, y=y_column, title=f"{y_column} vs {x_column} - Scatter Plot")
            elif plot_type == "Bar Plot":
                fig = px.bar(data, x=x_column, y=y_column, title=f"{y_column} vs {x_column} - Bar Plot")
            elif plot_type == "Box Plot":
                fig = px.box(data, x=x_column, y=y_column, title=f"{y_column} vs {x_column} - Box Plot")
            elif plot_type == "Line Plot":
                fig = px.line(data, x=x_column, y=y_column, title=f"{y_column} vs {x_column} - Line Plot")
            elif plot_type == "Histogram":
                fig = px.histogram(data, x=x_column, title=f"Histogram of {x_column}")
            elif plot_type == "Area Plot":
                fig = px.area(data, x=x_column, y=y_column, title=f"Area Plot of {y_column} vs {x_column}")
            elif plot_type == "Violin Plot":
                fig = px.violin(data, x=x_column, y=y_column, title=f"Violin Plot of {y_column} vs {x_column}")
            elif plot_type == "Pie Chart":
                fig = px.pie(data, names=x_column, values=y_column, title=f"Pie Chart of {x_column}")
            elif plot_type == "Strip Plot":
                fig = px.strip(data, x=x_column, y=y_column, title=f"Strip Plot of {y_column} vs {x_column}")
            elif plot_type == "Bubble Chart":
                fig = px.scatter(data, x=x_column, y=y_column, size=data[y_column], title=f"Bubble Chart of {y_column} vs {x_column}")

            # Display the selected plot
            st.plotly_chart(fig)

        # Separate option for generating correlation heatmap for the entire dataset
        if st.sidebar.button("Generate Correlation Heatmap"):
            correlation = data.corr()
            fig = go.Figure(data=go.Heatmap(
                z=correlation.values,
                x=correlation.columns,
                y=correlation.columns,
                colorscale='Viridis'
            ))
            fig.update_layout(title='Correlation Heatmap', xaxis_title='Features', yaxis_title='Features')
            st.plotly_chart(fig)