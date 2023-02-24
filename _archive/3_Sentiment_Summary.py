# Libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from data_sources import google_sheets
from plotly.subplots import make_subplots
from src import feedback_lib
from src.resources import colour_palette

# Global Variables
theme_plotly = None  # None or streamlit

# Layout
st.set_page_config(page_title="RIGRA Survey - Sentiment Summary", layout="wide")
st.title("RIGRA Survey Sentiment Summary")

# Data Sources
df = google_sheets.load_sentiment_data()

# Processed Data
## Tab 01
df_tab_01_A = df.groupby(["feedback_category"]).size().reset_index(name="counts")
df_tab_01_B = (
    df.groupby(["feedback_category", "sentiment"]).size().reset_index(name="counts")
)

## Overview
st.header("Overview")
st_col_01, st_col_02, st_col_03, st_col_04 = st.columns(4)
ori_score_pos = feedback_lib.sentiment_percentages(df, "positive")
ori_score_neu = feedback_lib.sentiment_percentages(df, "neutral")
ori_score_neg = feedback_lib.sentiment_percentages(df, "negative")
st_col_01.metric("Feedback Answers", int(df["response_id"].max()))
st_col_02.metric(
    "Positive Feedback Sentiment",
    f"{ori_score_pos} %",
)
st_col_03.metric(
    "Neutral Feedback Sentiment",
    f"{ori_score_neu} %",
)
st_col_04.metric(
    "Negative Feedback Sentiment",
    f"{ori_score_neg} %",
)

## SPACER
st.write("#")

## Feedback - Sentiment
st.header("Survey Feedback - Sentiment")

## Definitions
st.subheader("Definitions")
st.write(
    "Definitions for key terms that are used as part of the feedback sentiment analysis. "
)
st.markdown(
    "**Sentiment Analysis:** Sentiment analysis is used to determine whether a given text contains negative, positive, or neutral emotions."
)
st.markdown(
    "**Polarity:** Polarity refers to the overall sentiment conveyed by a particular text, phrase or word. This polarity can be expressed as a numerical rating. This score can be a number between -1 (negative) and 1 (positive) with 0 representing neutral sentiment"
)
st.markdown(
    "**Subjectivity:** Subjectivity quantifies the amount of personal opinion and factual information contained in the text. A higher subjectivity score means that the text contains personal opinion rather than factual information. This score can be a number between 0 and 1 where 0.0 is very objective (factual) and 1.0 is very subjective (opinionated)."
)

## Visulisations
st.subheader("Sentiment analysis - Visualisations")

### Navigation
tab1, tab2, tab3 = st.tabs(["Summary", "Feedback Breakdown", "Feedback Explorer"])

## SPACER
st.write("#")

#### Tab 1: Summary
with tab1:
    st.header("Sentiment Analysis Summary")
    #bc_01, bc_02 = st.columns(2)

    #with bc_01:
    # Elements
    # > Number of free text feedback responses per question category
    fig = px.bar(
        df_tab_01_A,
        y="feedback_category",
        x="counts",
        text=str("counts"),
        labels={"feedback_category": "Question Category"},
        title="Sentiment - Number of Feedback Responses",
        orientation="h",
        # template="simple_white"
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title="Number of Feedback Responses",
        yaxis_title=None,
        plot_bgcolor=colour_palette["background"],
        margin=dict(l=200),
        yaxis={"categoryorder": "total ascending"},
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    #with bc_02:
    # > Responses by sentiment type
    fig = px.bar(
        df_tab_01_B,
        x="counts",
        y="feedback_category",
        color="sentiment",
        text=str("counts"),
        labels={"feedback_category": "Question Category"},
        title="Sentiment - Percentage of Feedback Responses (Breakdown by Sentiment Type)",
        orientation="h",
        color_discrete_sequence=["red", "blue", "green"],
    )
    fig.update_layout(
        xaxis_title="Number of Feedback Responses",
        yaxis_title=None,
        plot_bgcolor=colour_palette["background"],
        margin=dict(l=200),
        yaxis={"categoryorder": "total ascending"},
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_traces(textposition="auto")
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

#### Tab 2: Feedback Breakdown
with tab2:
    st.header("Breakdown of Feedback")

    ## Overall breakdown - positive vs negative
    df_positive = (
        df[df["sentiment"] == "positive"]
        .groupby(["feedback_category", "sentiment"])
        .size()
        .reset_index(name="counts")
        .rename(columns={"index": "positive"})
    )
    df_negative = (
        df[df["sentiment"] == "negative"]
        .groupby(["feedback_category", "sentiment"])
        .size()
        .reset_index(name="counts")
        .rename(columns={"index": "negative"})
    )
    df_negative["counts"] *= -1
    fig = make_subplots(
        rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0
    )
    fig.append_trace(
        go.Bar(
            x=df_negative.counts,
            y=df_negative.feedback_category,
            orientation="h",
            showlegend=True,
            text=df_negative.counts,
            name="Negative Feedback",
            marker_color="#b20710",
        ),
        1,
        1,
    )
    fig.append_trace(
        go.Bar(
            x=df_positive.counts,
            y=df_positive.feedback_category,
            orientation="h",
            showlegend=True,
            text=df_positive.counts,
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


#### Tab 3: Feedback explorer
# Interactive feedback explorer to select and subset data using different sliders (e.g. sentiment, polarity)
with tab3:
    st.header("Sentiment Analysis Feedback Explorer")
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