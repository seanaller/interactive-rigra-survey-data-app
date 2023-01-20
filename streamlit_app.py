# Home.py

# Libraries
import streamlit as st

# Layout
st.set_page_config(page_title='RIGRA Winter Survey 2022', layout='wide')
st.title('RIGRA Winter Survey 2022')

# Opening Section
st.subheader('Overview')
st.write(
    """
    Welcome to the RIGRA Winter Survey 2022 results app. Please use the lefthand sidebar to navigate to the desired page. 
    """
)

# Footer
c1, c2, c3 = st.columns(3)
with c1:
    st.info('**Created by:** Sean Aller', icon = "🧑‍💻")
with c2:
    st.info('**Twitter: [@seanaller](https://twitter.com/seanaller)**', icon="💡")
with c3:
    st.info('**GitHub: [@seanaller](https://github.com/seanaller)**', icon="💻")