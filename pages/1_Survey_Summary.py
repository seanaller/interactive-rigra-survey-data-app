## Survey Summary

## Library Imports
import streamlit as st
from PIL import Image
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

from data_sources import google_sheets
from src import feedback_lib, summary_lib
from src.resources import colour_palette
from src.util import add_footer
from plotly.subplots import make_subplots

## Outline
# 1: Headline
# 2: Summary statement
# 3: How many people responded
# 4: Average feedback scores in each area
# 5: Main topics identified from feedback text
# 5: Buildings - Average Feedback Score
# 6: Breakdown for each building

# Global Variables
theme_plotly = None  # None or streamlit

# Layout
st.set_page_config(page_title='RIGRA Survey', layout='wide')

# Data Sources
df_summary = google_sheets.load_summary_data()
df_feedback = google_sheets.load_feedback_data()
df_mapping = df_feedback[['question_category','question']].drop_duplicates()

## Topics
df_topics = google_sheets.load_topic_data()

## Data Sources - Add colour column to feedback
values = ['red', 'blue', 'green']

# RIGRA logo
logo_rigra = Image.open('./images/rigra_logo.png')
image_col1, image_col2, image_col3 = st.columns(3)
with image_col1:
    st.write(' ')
with image_col2:
    st.image(logo_rigra)
with image_col3:
    st.write(' ')
    
def create_colour_conditions(df_colour):
    values = ['#FF0000', '#0000FF', '#00FF00']
    conditions_filtered = [
        (df_colour['feedback_score'] <= 3),
        (df_colour['feedback_score'] > 3) & (df_colour['feedback_score'] <= 4),
        (df_colour['feedback_score'] > 4),
    ]
    df_colour['feedback_colour'] = np.select(conditions_filtered, values)
    return df_colour

# Title
st.title('Survey Summary')

## Header

## Summary
st.markdown(
    '''
    The survey consisted of 8 categories of questions, with options to rate each question from 1 (worst) to 5 (best). 
    
    The average feedback across all questions was **3.4** out of 5.
    
    The majority of the feedback received was **neutral** (score of 3 or 4). There was more negative (1-3) than positive (5) feedback. 
    
    The survey results show that the questions on **Communal Areas** and **R&R Satisfaction - Facilities** had the most negative feedback.
    '''
)
st.write('')
st.write('')

st.markdown('---')

## Survey Responses Overview
st.subheader("Survey Responses Overview")
st_col_01, st_col_02, st_col_03, st_col_04, st_col_05 = st.columns(5)
st_col_01.metric("All Responses", summary_lib.metric_residents_all(df_summary))
st_col_02.metric(
    "Contactable Responses", summary_lib.metric_residents_contactable(df_summary)
)
st_col_03.metric(
    "Leaseholders", f"{summary_lib.metric_residents_leaseholder(df_summary)}%"
)
st_col_04.metric("Non-resident Leaseholders", f"{summary_lib.metric_residents_nonresident_leaseholder(df_summary)}%")
st_col_05.metric("Tenants", f"{summary_lib.metric_residents_tenant(df_summary)}%")
st.write('')
bc_01, bc_02 = st.columns(2)

with bc_01:
    fig = px.bar(
        summary_lib.filter_summary_data(df_summary, "resident_type"),
        x="Description",
        y="Number",
        title="Resident Type",
        log_y=False,
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title=None,
        yaxis_title="Number of Responses",
        xaxis={"categoryorder": "category ascending"},
        plot_bgcolor=colour_palette['background'],
    )
    fig.update_xaxes(showgrid = False)
    fig.update_yaxes(showgrid = False)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.bar(
        summary_lib.filter_summary_data(df_summary, "building_name"),
        x="Description",
        y="Number",
        title="Building Name",
        log_y=False,
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title=None,
        yaxis_title="Number of Responses",
        xaxis={"categoryorder": "category ascending"},
        plot_bgcolor=colour_palette['background'],
    )
    fig.update_xaxes(showgrid = False)
    fig.update_yaxes(showgrid = False)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
with bc_02:

    fig = px.bar(
        summary_lib.filter_summary_data(df_summary, "resident_length"),
        x="Description",
        y="Number",
        title="Resident Length",
        log_y=False,
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title=None,
        yaxis_title="Number of Responses",
        xaxis={"categoryorder": "category ascending"},
        plot_bgcolor=colour_palette['background'],
    )
    fig.update_xaxes(showgrid = False)
    fig.update_yaxes(showgrid = False)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
st.write()


## Feedback Overview
st.markdown('---')
st.subheader("Feedback Overview")
stf_col_01, stf_col_02, stf_col_03, stf_col_04, stf_col_05 = st.columns(5)
stf_col_01.metric(
    "Responses", int(df_feedback['response_id'].max())
)
stf_col_02.metric(
    "Average Feedback", 
    f'{feedback_lib.feedback_all_mean(df_feedback)}',
    "Out of 5.0",
    "off"
)
stf_col_03.metric(
    "Positive Feedback", 
    f"{feedback_lib.feedback_all_nps_percentages(df_feedback, 'positive')}%",
    "Score 4+",
    "off"
)
stf_col_04.metric(
    "Neutral Feedback", 
    f"{feedback_lib.feedback_all_nps_percentages(df_feedback, 'neutral')}%",
    "Score 3-4",
    "off"
)
stf_col_05.metric(
    "Negative Feedback", 
    f"{feedback_lib.feedback_all_nps_percentages(df_feedback, 'negative')}%",
    "Score 1-3",
    "off"
)

## SPACER
st.write("#")

## Feedback Questions
st.subheader('Feedback Questions - Categories')
st.markdown(
    "Questions and mapping to question categories are shown below"
)
mapping_style = df_mapping.style.hide_index()
st.write(mapping_style.to_html(), unsafe_allow_html=True)

## SPACER
st.write("#")
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

    ## Question Feedback Breakdown
    st.write('')
    st.subheader('Breakdown of Feedback - Positive and Negative Question Feedback')
    st.write('Note: Feedback here also takes into account the fre-text feedback (the sentiment of those answers). The higher the value, the more overall positive responses there were. The more negative the value, the more overall negative responses there were.')
    ## Overall breakdown - positive vs negative
    df_fb = google_sheets.load_sentiment_data()
    df_fb_positive = (
        df_fb[df_fb["sentiment"] == "positive"]
        .groupby(["feedback_category", "sentiment"])
        .size()
        .reset_index(name="counts")
        .rename(columns={"index": "positive"})
    )
    df_fb_negative = (
        df_fb[df_fb["sentiment"] == "negative"]
        .groupby(["feedback_category", "sentiment"])
        .size()
        .reset_index(name="counts")
        .rename(columns={"index": "negative"})
    )
    df_fb_negative["counts"] *= -1
    fig = make_subplots(
        rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0
    )
    fig.append_trace(
        go.Bar(
            x=df_fb_negative.counts,
            y=df_fb_negative.feedback_category,
            orientation="h",
            showlegend=True,
            #text=df_fb_negative.counts,
            name="Negative Feedback",
            marker_color="#b20710",
        ),
        1,
        1,
    )
    fig.append_trace(
        go.Bar(
            x=df_fb_positive.counts,
            y=df_fb_positive.feedback_category,
            orientation="h",
            showlegend=True,
            #text=df_fb_positive.counts,
            name="Positive Feedback",
            marker_color="green",
        ),
        1,
        2,
    )
    fig.update_layout(
        plot_bgcolor=colour_palette["background"],
        margin=dict(l=200),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        showgrid=False, categoryorder="total ascending", ticksuffix=" ", showline=False
    )
    fig.update_traces(textposition="auto")
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
add_footer()