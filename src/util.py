## util
## Utilities for the Streamlit app

## Library Imports
import streamlit as st 

## Footer Definition
def add_footer():
    ft = """
    <style>
    a:link , a:visited{
    color: #BFBFBF;  /* theme's text color hex code at 75 percent brightness*/
    background-color: transparent;
    text-decoration: none;
    }

    a:hover,  a:active {
    color: #0283C3; /* theme's primary color*/
    background-color: transparent;
    text-decoration: underline;
    }

    #page-container {
    position: relative;
    min-height: 10vh;
    }

    footer{
        visibility:hidden;
    }

    .footer {
    position: relative;
    left: 0;
    top: 0;
    bottom: 0;
    width: 100%;
    background-color: transparent;
    color: #2c3e50; /* theme's text color hex code at 50 percent brightness*/
    text-align: center; /* you can replace 'left' with 'center' or 'right' if you want*/
    }
    </style>

    <div id="page-container">

    <div class="footer">
        <hr>
        <p style='font-size: 12pt;'>
            Made using 
                <a style='display: inline; text-align: left;' href="https://streamlit.io/" target="_blank">Streamlit</a>
            with 
                <img src="https://img.icons8.com/ios/1x/code--v2.gif" alt="code" height= "14"/>
                <a style='display: inline; text-align: left;' href="https://www.seanaller.co.uk" target="_blank"> by Sean Aller</a>
        </p>
    </div>

    </div>
    """
    st.write(ft, unsafe_allow_html=True)