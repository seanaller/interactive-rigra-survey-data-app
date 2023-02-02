# Libraries
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

from data_sources import google_sheets
from src import feedback_lib
from src.resources import colour_palette

# Global Variables
theme_plotly = None  # None or streamlit

# Layout
st.set_page_config(page_title="RIGRA Survey - Feedback Summary", layout="wide")
st.title("RIGRA Survey Feedback Summary")

# Data Sources
df_feedback = google_sheets.load_feedback_data()
df_mapping = df_feedback[['question_category','question']].drop_duplicates()

## Overview
st.subheader("Overview")
st_col_01, st_col_02, st_col_03, st_col_04, st_col_05 = st.columns(5)
st_col_01.metric(
    "Responses", int(df_feedback['response_id'].max())
)
st_col_02.metric(
    "Average Feedback", 
    f'{feedback_lib.feedback_all_mean(df_feedback)}',
    "Out of 5.0",
    "off"
)
st_col_03.metric(
    "Positive Feedback", 
    f"{feedback_lib.feedback_all_nps_percentages(df_feedback, 'positive')}%",
    "Score 4+",
    "off"
)
st_col_04.metric(
    "Neutral Feedback", 
    f"{feedback_lib.feedback_all_nps_percentages(df_feedback, 'neutral')}%",
    "Score 3-4",
    "off"
)
st_col_05.metric(
    "Negative Feedback", 
    f"{feedback_lib.feedback_all_nps_percentages(df_feedback, 'negative')}%",
    "Score 1-3",
    "off"
)

## SPACER
st.write("#")

## Feedback - Summary
st.subheader("Survey Feedback")
st.write(
    "Survey feedback is presented as average scores for each question category. Scores for questions ranged from 1 (Most Negative) to 5 (Most Positive)."
)
st.markdown(
    "Questions and mapping to question categories are shown below"
)
mapping_style = df_mapping.style.hide_index()
st.write(mapping_style.to_html(), unsafe_allow_html=True)

## SPACER
st.write("#")

### Tab 01 - Summary
st.header("Average Feedback Scores")
fig = px.bar(
    feedback_lib.feedback_questions_average(df_feedback),
    y = "question_category",
    x = "feedback_score",
    title = "Questions - Average Feedback",
    log_y = False,
    orientation = 'h'
)
fig.update_layout(
    showlegend = False,
    yaxis_title = None,
    xaxis_title = "Feedback Score (Average)",
    yaxis = {"categoryorder": "category descending"},
    plot_bgcolor = colour_palette['background'],
    margin = dict(l = 200),
    xaxis_range=[1,5]
)
fig.update_xaxes(showgrid = False)
fig.update_yaxes(showgrid = False)
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


### Loop and plot
# SPACER
st.write("#")
st.header("Average Feedback Score - Split By Building")
list_building_name = list(df_feedback['building_name'].drop_duplicates())
for building in list_building_name:
    df_feedback_filtered = df_feedback[df_feedback['building_name'] == building]
    st.write("#")
    st.subheader(f"Average Feedback Score - {building}")
    fig = px.bar(
        feedback_lib.feedback_questions_average(df_feedback_filtered),
        y = "question_category",
        x = "feedback_score",
        title = f"Questions - Average Feedback ({building})",
        log_y = False,
        orientation = 'h'
    )
    fig.update_layout(
        showlegend = False,
        yaxis_title = None,
        xaxis_title = "Feedback Score (Average)",
        yaxis = {"categoryorder": "category descending"},
        plot_bgcolor = colour_palette['background'],
        margin = dict(l = 200),
        xaxis_range=[1,5]
    )
    fig.update_xaxes(showgrid = False)
    fig.update_yaxes(showgrid = False)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)