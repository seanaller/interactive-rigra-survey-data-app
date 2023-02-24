# Home.py

# Libraries
import streamlit as st
from PIL import Image

from src.util import add_footer

# Layout
st.set_page_config(page_title='RIGRA Survey', layout='wide')

# RIGRA logo
logo_rigra = Image.open('./images/rigra_logo.png')
image_col1, image_col2, image_col3 = st.columns(3)
with image_col1:
    st.write(' ')
with image_col2:
    st.image(logo_rigra)
with image_col3:
    st.write(' ')

# Title
st.title('RIGRA Winter Survey 2022')

# Opening Section
st.subheader('Overview')
st.markdown(
    """
    Welcome to the River Gardens Estate survey results interactive app! 
    Here, you can explore the Winter 2022 survey results, which received 159 responses across the entire estate.
    
    Please use the sidebar (left-hand side) to navigate through the RIGRA Survey app.
    
    The sections are as follows:
    1. Survey Summary: Overview of the RIGRA survey, including number of respondents, average feedback score etc. 
    1. Feedback Explorer: Interactive exploration of the feedback. Feedback can be split by building and question.
    1. Contact Us: Contact details for RIGRA if you would like to raise anything from using the survey app.
    
    Additionally, the free-text feedback responses were analyzed using sentiment analysis to understand overall sentiment.
    
    The purpose of this app is to interactively explore the survey feedback, providing residents with the opportunity to understand and contribute to improving the River Gardens Estate.
    
    """
)

## Download Options
st.subheader('Downloads')
st.write(
    """
    If you'd like to download a copy of the survey data please use the download buttons below.
    """
)

### Survey Data
with open('exports/RIGRA_Survey_Winter2022_Summary.xlsx', 'rb') as f:
    st.download_button(
        label = '📁 Survey Data (.xlsx)',
        data = f,
        file_name = 'RIGRA_Survey_Winter2022.xlsx'
        )


## Footnotes
st.write('')
st.write('')
st.write('')
st.markdown('**Footnotes**')
st.markdown('ℹ️ *Sentiment analysis is a technique used to understand the emotional tone of a text. In this case, it was used to analyze the free-text feedback and identify overall sentiment.*')

## Add Footer
add_footer()