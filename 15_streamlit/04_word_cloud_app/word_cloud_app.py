import streamlit as st
import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import PyPDF2
from docx import Document
import plotly.express as px
import base64
from io import BytesIO

# Function to read text files
def read_txt(file):
    """Reads a .txt file and returns its content as a string."""
    return file.getvalue().decode("utf-8")

# Function to read Word (.docx) files
def read_docx(file):
    """Reads a .docx file and returns its content as a string."""
    doc = Document(file)
    return " ".join([para.text for para in doc.paragraphs])

# Function to read PDF files
def read_pdf(file):
    """Reads a .pdf file and returns its content as a string."""
    pdf = PyPDF2.PdfReader(file)
    return " ".join([page.extract_text() for page in pdf.pages])

# Function to filter out stopwords from the text
def filter_stopwords(text, additional_stopwords=[]):
    """Filters out stopwords from the given text.
    
    Args:
        text (str): The input text to filter.
        additional_stopwords (list): Additional stopwords to remove from the text.
    
    Returns:
        str: The filtered text without stopwords.
    """
    words = text.split()  # Split text into words
    all_stopwords = STOPWORDS.union(set(additional_stopwords))  # Combine standard and additional stopwords
    filtered_words = [word for word in words if word.lower() not in all_stopwords]  # Filter out stopwords
    return " ".join(filtered_words)  # Join filtered words back into a string

# Function to create a download link for the generated plot
def get_image_download_link(buffered, format_):
    """Creates a downloadable link for the generated image plot.
    
    Args:
        buffered (BytesIO): The image buffer.
        format_ (str): The image format (e.g., png, jpeg).
    
    Returns:
        str: HTML link for downloading the image.
    """
    image_base64 = base64.b64encode(buffered.getvalue()).decode()  # Encode image to base64
    return f'<a href="data:image/{format_};base64,{image_base64}" download="wordcloud.{format_}">Download Plot as {format_}</a>'

# Function to create a downloadable link for a DataFrame as CSV
def get_table_download_link(df, filename, file_label):
    """Creates a downloadable link for a DataFrame in CSV format.
    
    Args:
        df (DataFrame): The DataFrame to convert.
        filename (str): Desired filename for the downloaded CSV.
        file_label (str): Label for the download link.
    
    Returns:
        str: HTML link for downloading the CSV file.
    """
    csv = df.to_csv(index=False)  # Convert DataFrame to CSV
    b64 = base64.b64encode(csv.encode()).decode()  # Encode CSV to base64
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{file_label}</a>'

# Streamlit app layout
st.title("Word Cloud Generator")  # Title of the app
st.text("📁 Upload a pdf, docx or text file to generate a word cloud")  # Instruction text

# File uploader for text, PDF, or Word files
uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])

if uploaded_file:
    # Display file details
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
    st.write(file_details)

    # Check the file type and read the content accordingly
    if uploaded_file.type == "text/plain":
        text = read_txt(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        text = read_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = read_docx(uploaded_file)
    else:
        st.error("File type not supported. Please upload a txt, pdf or docx file.")
        st.stop()  # Stop execution if the file type is unsupported

    # Generate a word count table
    words = text.split()  # Split text into words
    word_count = pd.DataFrame({'Word': words}).groupby('Word').size().reset_index(name='Count').sort_values('Count', ascending=False)

    # Sidebar options for stopwords
    use_standard_stopwords = st.sidebar.checkbox("Use standard stopwords?", True)  # Checkbox for standard stopwords
    top_words = word_count['Word'].head(50).tolist()  # Get top 50 words for additional stopwords
    additional_stopwords = st.sidebar.multiselect("Additional stopwords:", sorted(top_words))  # Multi-select for additional stopwords

    # Determine stopwords to use
    if use_standard_stopwords:
        all_stopwords = STOPWORDS.union(set(additional_stopwords))  # Combine standard and additional stopwords
    else:
        all_stopwords = set(additional_stopwords)  # Use only additional stopwords

    # Filter text to remove stopwords
    text = filter_stopwords(text, all_stopwords)

    if text:
        # Set dimensions for the word cloud
        width = st.sidebar.slider("Select Word Cloud Width", 400, 2000, 1200, 50)  # Width slider
        height = st.sidebar.slider("Select Word Cloud Height", 200, 2000, 800, 50)  # Height slider

        # Generate and display the word cloud
        st.subheader("Generated Word Cloud")
        fig, ax = plt.subplots(figsize=(width/100, height/100))  # Convert pixels to inches for figsize
        wordcloud_img = WordCloud(width=width, height=height, background_color='white', max_words=200, contour_width=3, contour_color='steelblue').generate(text)
        ax.imshow(wordcloud_img, interpolation='bilinear')  # Display the word cloud
        ax.axis('off')  # Hide axes

        # Save plot functionality
        format_ = st.selectbox("Select file format to save the plot", ["png", "jpeg", "svg", "pdf"])  # Select box for formats
        resolution = st.slider("Select Resolution", 100, 500, 300, 50)  # Slider for resolution
        
        # Display word count table
        st.subheader("Word Count Table")
        st.write(word_count)  # Show word count table
    st.pyplot(fig)  # Show the generated plot
    
    # Button to save the plot
    if st.button(f"Save as {format_}"):
        buffered = BytesIO()  # Create a buffer to save the plot
        plt.savefig(buffered, format=format_, dpi=resolution)  # Save the plot to buffer
        st.markdown(get_image_download_link(buffered, format_), unsafe_allow_html=True)  # Provide download link

    # Download link for the word count table
    if st.button('Download Word Count Table as CSV'):
        st.markdown(get_table_download_link(word_count, "word_count.csv", "Click Here to Download"), unsafe_allow_html=True)  # Download link for CSV


# Sidebar: Additional Information
st.sidebar.header("About Me")
st.sidebar.text("Name: Muhammad Hassaan")  
st.sidebar.text("Email: muhammadhassaan7896@gmail.com")

# Display logos with specified width, clickable links in one line, centered and with reduced space
st.sidebar.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center;">
        <a href="https://www.linkedin.com/in/iammuhammadhassaan7/" style="margin: 0 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/e/e9/Linkedin_icon.svg" alt="LinkedIn" width="30"/>
        </a>
        <a href="https://github.com/iammuhammadhassaaan" style="margin: 0 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub" width="30"/>
        </a>
        <a href="https://www.kaggle.com/mhassaan1122" style="margin: 0 10px;">
            <img src="https://www.vectorlogo.zone/logos/kaggle/kaggle-icon.svg" alt="Kaggle" width="30"/>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
