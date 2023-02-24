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

## Topics
df_topics = google_sheets.load_topic_data()

## Data Sources - Add colour column to feedback
values = ['red', 'blue', 'green']

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

def create_colour_conditions(df_colour):
    values = ['#FF0000', '#0000FF', '#00FF00']
    conditions_filtered = [
        (df_colour['feedback_score'] <= 3),
        (df_colour['feedback_score'] > 3) & (df_colour['feedback_score'] <= 4),
        (df_colour['feedback_score'] > 4),
    ]
    df_colour['feedback_colour'] = np.select(conditions_filtered, values)
    return df_colour

### Navigation
tab1, tab2, tab3 = st.tabs(["Feedback Score Summary", "Feedback Score by Building", "Feedback Topics"])

### Tab 01 - Summary
with tab1:
    st.header("Average Feedback Scores")
    df_plot = feedback_lib.feedback_questions_average(df_feedback)
    df_plot = create_colour_conditions(df_plot)
    fig = px.bar(
        df_plot,
        y = "question_category",
        x = "feedback_score",
        title = "Questions - Average Feedback",
        color = 'feedback_colour',
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


def set_color(row):
    if row["feedback_score"] < 3:
        return "negative"
    elif row["feedback_score"] > 4:
        return "positive"
    else:
        return "neutral"

### Loop and plot
# SPACER
with tab2:
    st.header("Average Feedback Score - Split By Building")
    list_building_name = list(df_feedback['building_name'].drop_duplicates())
    for building in list_building_name:
        df_feedback_filtered = df_feedback[df_feedback['building_name'] == building]
        st.write("#")
        st.subheader(f"Average Feedback Score - {building}")
        df_plot_filtered = feedback_lib.feedback_questions_average(df_feedback_filtered)
        df_plot_filtered = df_plot_filtered[['question_category','feedback_score']]
        df_plot_filtered = df_plot_filtered.astype({'feedback_score': 'float'})
        #df_plot_filtered = create_colour_conditions(df_plot_filtered)
        df_plot_filtered = df_plot_filtered.assign(feedback_colour=df_plot_filtered.apply(set_color, axis=1))
        
        fig = px.bar(
            df_plot_filtered,
            y = "question_category",
            x = "feedback_score",
            color = "feedback_colour",
            title = f"Questions - Average Feedback ({building})",
            log_y = False,
            orientation = 'h',
            color_discrete_map= {
                'negative': '#c0392b',
                'neutral': '#2980b9',
                'positive': '#27ae60'
            }
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
        
## Topics
with tab3:
    st.header("Free Text Feedback - Topic Modelling")
    st.write("#")
    st.write("Topic modelling is generated from the free-text feedback for each question category.")
    st.write("If a question category is not present, that means not enough feedback was received to generate topics.")
    st.write("A maximum of 5 topics can be generated for each category.")
    st.write("Each topic is broken down into the top words of that topic.")
    st.write("#")
    st.subheader("Topics Summary: All feedback")
    df_topics_all = df_topics[df_topics['feedback_category'] == 'All']
    list_topics_all = list(set(df_topics_all['topic']))
    list_topics_all.sort()
    for topics_all in list_topics_all:
        tmp_topics = ', '.join(list(df_topics_all['word'][df_topics_all['topic'] == topics_all]))
        st.write(f'{topics_all}: {tmp_topics}')
    st.write("#")
    feedback_cat_list = list(set(df_topics['feedback_category']))
    feedback_cat_list = [x for x in feedback_cat_list if x != 'All']
    for feed_cat in feedback_cat_list:
        st.subheader(f"Topics Summary: {feed_cat}")
        df_topics_feed = df_topics[df_topics['feedback_category'] == feed_cat]
        list_topics_feed = list(set(df_topics_feed['topic']))
        list_topics_feed.sort()
        for topics_feed in list_topics_feed:
            tmp_topics = ', '.join(list(df_topics_feed['word'][df_topics_feed['topic'] == topics_feed]))
            st.write(f'{topics_feed}: {tmp_topics}')
            
            
## Add Footer
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