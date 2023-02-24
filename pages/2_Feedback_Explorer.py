## Feedback Explorer

## Library Imports
import streamlit as st
from src.util import add_footer
from PIL import Image
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from data_sources import google_sheets
from plotly.subplots import make_subplots
from src import feedback_lib
from src.resources import colour_palette

## Outline
# 1. Headline
# 2. Description
# 3. Feedback Explorer: 3 tabs
#   3a: Overall feedback 
#   3b: By building
#   3c: By Question Category

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
st.title('Feedback Explorer')
st.write('')
st.write('Please use the interactive table below to explore the feedback data from the RIGRA Survey Winter 2022.')
st.markdown('---')
st.write('')
# Data Sources
df = google_sheets.load_sentiment_data()
ori_score_pos = feedback_lib.sentiment_percentages(df, "positive")
ori_score_neu = feedback_lib.sentiment_percentages(df, "neutral")
ori_score_neg = feedback_lib.sentiment_percentages(df, "negative")

# > Question Category Selection
st_q_01_tab03, st_q_02_tab03 = st.columns(2)
df_tab_03 = df
with st_q_01_tab03:
    sel_question = st.selectbox(
        "Question categories for breakdown:",
        ["All"] + [x for x in list(set(df["feedback_category"]))],
    )
    if sel_question == "All":
        df_tab_03 = df_tab_03
    else:
        df_tab_03 = df_tab_03[df_tab_03["feedback_category"] == sel_question]
with st_q_02_tab03:
    sel_building = st.selectbox(
        "Buildings for breakdown:",
        ["All"] + [x for x in list(set(df_tab_03["building_name"]))],
    )
    if sel_building == "All":
        df_tab_03 = df_tab_03
    else:
        df_tab_03 = df_tab_03[df_tab_03["building_name"] == sel_building]

# > Selection
sel_sentiment = st.multiselect(
    "Sentiment types to include",
    ["Positive", "Neutral", "Negative"],
    default=["Positive", "Neutral", "Negative"],
)
sel_sentiment = [x.lower() for x in sel_sentiment]
df_tab_03 = df_tab_03[df_tab_03["sentiment"].isin(sel_sentiment)]

## Hidden for advanced manipulation
with st.expander("Advanced filtering"):
    # > Sliders
    con_polarity = st.slider(
        "Polarity Score", min_value=-1.0, max_value=1.0, value=(-1.0, 1.0), step=0.1
    )
    df_tab_03 = df_tab_03[df_tab_03["polarity"] >= con_polarity[0]]
    df_tab_03 = df_tab_03[df_tab_03["polarity"] <= con_polarity[1]]

    con_subjectivity = st.slider(
        "Subjectivity Score",
        min_value=0.0,
        max_value=1.0,
        value=(0.0, 1.0),
        step=0.1,
    )
    df_tab_03 = df_tab_03[df_tab_03["subjectivity"] >= con_subjectivity[0]]
    df_tab_03 = df_tab_03[df_tab_03["subjectivity"] <= con_subjectivity[1]]

# space
st.write("#")

# Details
st_col_01_tab03, st_col_02_tab03, st_col_03_tab03 = st.columns(3)
st_col_01_tab03.metric(
    "Positive Feedback Sentiment",
    f'{feedback_lib.sentiment_percentages(df_tab_03,"positive")} %',
    feedback_lib.sentiment_percentages(df_tab_03, "positive") - ori_score_pos,
)
st_col_02_tab03.metric(
    "Neutral Feedback Sentiment",
    f'{feedback_lib.sentiment_percentages(df_tab_03,"neutral")} %',
    feedback_lib.sentiment_percentages(df_tab_03, "neutral") - ori_score_neu,
)
st_col_03_tab03.metric(
    "Negative Feedback Sentiment",
    f'{feedback_lib.sentiment_percentages(df_tab_03,"negative")} %',
    feedback_lib.sentiment_percentages(df_tab_03, "negative") - ori_score_neg,
)

# > Data
df_tab_03 = df_tab_03[
    [
        "resident_type",
        "building_name",
        "building_floor",
        "resident_length",
        "feedback_category",
        "sentiment",
        "free_text",
    ]
].rename(
    columns={
        "resident_type": "Resident",
        "building_name": "Building Name",
        "building_floor": "Building Floor",
        "resident_length": "Length of Residency",
        "feedback_category": "Category",
        "free_text": "Feedback Response",
        "sentiment": "Sentiment Category",
    }
)

## Output
def color_col(col, pattern_map, default=""):
    return np.select(
        [col.str.contains(k, na=False) for k in pattern_map.keys()],
        [f"background-color: {v}" for v in pattern_map.values()],
        default=default,
    ).astype(str)

styler = df_tab_03.style.apply(
    color_col,
    pattern_map={
        "neutral": "#C0F9FA",
        "negative": "#FCCCCC",
        "positive": "#92F294",
    },
    subset=["Sentiment Category"],
)
styler.hide_index()
st.write(styler.to_html(), unsafe_allow_html=True)
# st.dataframe(
#     data = df_tab_03,
#     use_container_width = True
#     )

## Add Footer
add_footer()