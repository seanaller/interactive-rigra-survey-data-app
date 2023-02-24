## Contact Us

## Library Imports
import streamlit as st
from src.util import add_footer
from PIL import Image

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

    
## Title
st.title("Contact Us")
st.write('')
st.write('''
         If you'd like to reach out with a question or query, you can contact RIGRA using one of the methods below.
         ''')
st.write('')
st.write('')
st.write('')
c1, c2, c3 = st.columns(3)
with c1:
    st.subheader('📧 Email')
    st.markdown('[rigracomm@gmail.com](mailto:rigracomm@gmail.com)')
with c2:
    st.subheader('📞 Phone')
    st.write('07493181351')
with c3:
    st.subheader('🌐 Forum')
    st.markdown('[River Gardens Forum](http://www.rivergardensforum.uk)')
st.write('')
st.write('')
st.write('')
## Add Footer
add_footer()