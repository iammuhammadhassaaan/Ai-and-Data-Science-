import streamlit as st
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.svm import SVR, SVC
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

def preprocess_data(X, y, problem_type):
    # Identify numeric and categorical columns
    numeric_cols = X.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Impute numeric columns
    if numeric_cols:
        imp_numeric = IterativeImputer()
        X[numeric_cols] = imp_numeric.fit_transform(X[numeric_cols])

    # Impute categorical columns (if needed) and encode them
    if categorical_cols:
        for col in categorical_cols:
            X[col] = X[col].fillna(X[col].mode()[0])  # Filling with mode (most frequent value)
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))

    # Ensure the shape of the DataFrame is consistent
    if X.shape[1] != len(numeric_cols) + len(categorical_cols):
        st.error("Imputation has altered the number of columns. Please check the data.")
        return None, None
    
    # Use OneHotEncoder for categorical features if there are any
    if categorical_cols:
        preprocessor = ColumnTransformer(
            transformers=[
                ('encoder', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
            ],
            remainder='passthrough'  # Keep non-categorical columns
        )
        X_processed = preprocessor.fit_transform(X)
    else:
        X_processed = X.values

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_processed)
    
    return X_scaled, y

# Function to train and evaluate models
def train_and_evaluate(X_train, X_test, y_train, y_test, model):
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    return predictions

# Main application function
def main():
    st.title("Machine Learning Application")
    st.write("Welcome to the machine learning application. This app allows you to train and evaluate different machine learning models on your dataset.")
    
    # Data upload or example data selection
    data_source = st.sidebar.selectbox("Do you want to upload data or use example data?", ["Upload", "Example"])
    
    if data_source == "Upload":
        uploaded_file = st.sidebar.file_uploader("Choose a file", type=['csv', 'xlsx', 'tsv'])
        if uploaded_file is not None:
            if uploaded_file.type == "text/csv":
                data = pd.read_csv(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                data = pd.read_excel(uploaded_file)
            elif uploaded_file.type == "text/tab-separated-values":
                data = pd.read_csv(uploaded_file, sep='\t')
    else:
        dataset_name = st.sidebar.selectbox("Select a dataset", ["titanic", "tips", "iris"])
        data = sns.load_dataset(dataset_name)
    
    if data is not None and not data.empty:
        st.write("Data Head:", data.head())
        st.write("Data Shape:", data.shape)
        st.write("Data Description:", data.describe())
        st.write("Column Names:", data.columns.tolist())
        
        # Select features and target
        features = st.multiselect("Select features columns", data.columns.tolist())
        target = st.selectbox("Select target column", data.columns.tolist())
        problem_type = st.selectbox("Problem Type", ["Classification", "Regression"])
        
        if features and target and problem_type:
            X = data[features]
            y = data[target]
            
            st.write(f"You have selected a {problem_type} problem.")
            
            # Button to start analysis
            if st.button("Run Analysis"):
                # Pre-process data
                X_processed, y_processed = preprocess_data(X, y, problem_type)
                
                if X_processed is not None and y_processed is not None:
                    # Train-test split
                    # Correct the slider code by explicitly naming the `value` parameter
                    test_size = st.slider("Select test split size", min_value=0.1, max_value=0.5, value=0.2, step=0.1)
                    X_train, X_test, y_train, y_test = train_test_split(X_processed, y_processed, test_size=test_size, random_state=42)
                    
                    # Model selection based on problem type
                    model_options = ['Linear Regression', 'Decision Tree', 'Random Forest', 'SVM'] if problem_type == 'Regression' else ['Decision Tree', 'Random Forest', 'SVM']
                    selected_model = st.sidebar.selectbox("Select model", model_options)
                    
                    # Initialize model
                    if selected_model == 'Linear Regression':
                        model = LinearRegression()
                    elif selected_model == 'Decision Tree':
                        model = DecisionTreeRegressor() if problem_type == 'Regression' else DecisionTreeClassifier()
                    elif selected_model == 'Random Forest':
                        model = RandomForestRegressor() if problem_type == 'Regression' else RandomForestClassifier()
                    elif selected_model == 'SVM':
                        model = SVR() if problem_type == 'Regression' else SVC()
                        
                    # Train and evaluate model
                    predictions = train_and_evaluate(X_train, X_test, y_train, y_test, model)
                    
                    # Evaluation metrics and results presentation
                    # Implement evaluation based on the problem type as required.
                    # This section is simplified for brevity.
                    
                    st.write("Model training and evaluation complete. Implement specific metrics display here.")
                    
                    # Download model, make predictions, and show results
                    # Further implementation needed based on application requirements.
                
if __name__ == "__main__":
    main()
