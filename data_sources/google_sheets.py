# google_sheets.py
"""
Description
- App sub-module for loading google sheets data
"""

"""
Script Setup
- Import relevant python modules and setup google sheet credentials using secrets.toml and gsheetsdb
"""

## Module Imports
import pandas as pd
from gsheetsdb import connect
import streamlit as st

'''
Define functions for obtaining data
- Class allows for multiple sheet selection (using variables loaded from secrets.toml)
'''

'''
Hard Coded Variables
'''
# Time to live: the maximum number of seconds to keep an entry in the cache
TTL = 24 * 60 * 60    
    
'''
Supporting Functions
'''
# Share the connector across all users connected to the app
@st.experimental_singleton()
def _get_connector():
    return connect()

# SQL Query to Pandas DataFrame
@st.experimental_memo(ttl = TTL)
def _query_to_dataframe(_connector, query: str) -> pd.DataFrame:
    rows = _connector.execute(query, headers=1)
    dataframe = pd.DataFrame(list(rows))
    return dataframe

# Query from Google Sheet to Pandas DataFrame
@st.experimental_memo(ttl = 600)
def _get_data(_connector, gsheet_url) -> pd.DataFrame:
    return _query_to_dataframe(_connector, f'SELECT * FROM "{gsheet_url}"')

'''
Main Function
'''

## Survey summary data
def load_summary_data():
    # Create connector
    gsheet_connector = _get_connector()
    # Connect to the google sheet
    gsheets_url = st.secrets["gsheets"]["summary"]
    # Download data
    data = _get_data(gsheet_connector, gsheets_url)
    # Return data
    return data

## Feedback data
def load_feedback_data():
    # Create connector
    gsheet_connector = _get_connector()
    # Connect to the google sheet
    gsheets_url = st.secrets["gsheets"]["feedback"]
    # Download data
    data = _get_data(gsheet_connector, gsheets_url)
    # Return data
    return data

## Sentiment data
def load_sentiment_data():
    # Create connector
    gsheet_connector = _get_connector()
    # Connect to the google sheet
    gsheets_url = st.secrets["gsheets"]["sentiment"]
    # Download data
    data = _get_data(gsheet_connector, gsheets_url)
    # Return data
    return data

## Topic data
def load_topic_data():
    # Create connector
    gsheet_connector = _get_connector()
    # Connect to the google sheet
    gsheets_url = st.secrets["gsheets"]["topics"]
    # Download data
    data = _get_data(gsheet_connector, gsheets_url)
    # Return data
    return data