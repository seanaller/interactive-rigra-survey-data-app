# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px

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

### TAB NAVIAGTION
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Summary", "Detailed Summary", "Resident Type", 
    "Resident Length (Years)", "Building Name", "Building Floor"
    ])

## SPACER
st.write("#")

### Tab 01 - Summary
with tab1:
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


### Tab 02 - Detailed Summary
with tab2:
    st.header("Detailed Feedback Scores")
    
    fig = px.box(
        df_feedback,
        y = "question_category",
        x = "feedback_score",
        orientation = 'h'
    )
    
    fig.update_layout(
        showlegend = False,
        yaxis_title = None,
        xaxis_title = "Feedback Score",
        yaxis = {"categoryorder": "category descending"},
        plot_bgcolor = colour_palette['background'],
        margin = dict(l = 200),
        xaxis_range=[1,5]
    )
    
    fig.update_xaxes(showgrid = False)
    fig.update_yaxes(showgrid = False)
    
    st.plotly_chart(
        fig,
        use_container_width = True,
        theme = theme_plotly
    )

### Tab 03 - Resident Type
with tab3:
    st.header("Average Feedback Scores by Resident Type")


### Tab 04 - Resident Length
with tab4:
    st.header("Average Feedback Scores by Resident Length (Years)")


### Tab 05 - Building Name
with tab5:
    st.header("Average Feedback Scores by Building Name")


### Tab 06 - Building Floor
with tab6:
    st.header("Average Feedback Scores by Building Floor")
