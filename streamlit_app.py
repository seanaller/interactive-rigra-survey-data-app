# streamlit_app.py

## Environment Setup
import pandas as pd
import gspread
import streamlit as st

import plotly.express as px
import plotly.graph_objects as go

## Load Google Sheet
gc = gspread.service_account('.streamlit/credentials.json')
gc_responses = gc.open_by_key(st.secrets.gsheet.sheet_id)
df_responses = pd.DataFrame(gc_responses.worksheet(st.secrets.gsheet.sheet_responses).get_all_records())

## App Setup
st.set_page_config(
    page_title="rigra", page_icon="🖼️", initial_sidebar_state="collapsed"
)
st.markdown("# RIGRA Winter Survey 2022")

## Survey Responses Bar Chat - All
st.bar_chart(df_responses[df_responses['Type'] == 'all'],
             x = 'Description',
             y = 'Number')

## Survey Responses Bar Chat - Resident Type
df_responses_resident_type = df_responses[df_responses['Type'] == 'resident_type']
pie_counts_resident_type = go.Figure(
    data = [
        go.Pie(labels = df_responses_resident_type.Description,
               values = df_responses_resident_type.Number,
               hole = .3)
        ]
    )
st.plotly_chart(pie_counts_resident_type, use_container_width=True)

## Survey Responses Bar Chat - Building Name
st.bar_chart(df_responses[df_responses['Type'] == 'building_name'],
             x = 'Description',
             y = 'Number')

## Survey Responses Bar Chat - Building Floor
st.bar_chart(df_responses[df_responses['Type'] == 'building_floor'],
             x = 'Description',
             y = 'Number')

## Survey Responses Bar Chat - Resident Length
st.bar_chart(df_responses[df_responses['Type'] == 'resident_length'],
             x = 'Description',
             y = 'Number')