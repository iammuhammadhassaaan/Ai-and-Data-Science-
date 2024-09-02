# import libraries
import streamlit as st


# creating a title for the app
st.title("Basic Streamlit App")

# adda simple text
st.write("This is my first streamlit app")

# add a slider to the app
st.slider("Select a number", min_value=0, max_value=10)

# adding a button 
if st.button("Click me"):
    st.write("You clicked the button")
else:
    st.write("You did not click the button")


# add a dropdown list
option = st.sidebar.selectbox("Select your New Mobile:", ["Apple", "Samsung", "Oppo"])

# display the selected option
st.write("Your selected MObile is:", option)

# add a text input
name = st.sidebar.text_input("Enter your name:")

# display the entered name
st.write("Hello", name)

# add radio button with options 
option = st.sidebar.radio("Your New Book is:", ["Book 1", "Book 2", "Book 3"])

# display the selected option
st.write("You selected:", option)

# add a file uploader
file = st.sidebar.file_uploader("Upload your file:")

# display the uploaded file
st.write("Your file is:", file)