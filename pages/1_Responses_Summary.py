# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px

from data_sources import google_sheets
from src import summary_lib
from src.resources import colour_palette

# Global Variables
theme_plotly = None  # None or streamlit

# Layout
st.set_page_config(page_title="RIGRA Survey - Responses Summary", layout="wide")
st.title("RIGRA Survey Responses Summary")

# Data Sources
df_summary = google_sheets.load_summary_data()

## Overview
st.subheader("Overview")
st_col_01, st_col_02, st_col_03, st_col_04 = st.columns(4)
st_col_01.metric("All Responses", summary_lib.metric_residents_all(df_summary))
st_col_02.metric(
    "Contactable Responses", summary_lib.metric_residents_contactable(df_summary)
)
st_col_03.metric(
    "Leaseholders", f"{summary_lib.metric_residents_leaseholder(df_summary)}%"
)
st_col_04.metric("Tenants", f"{summary_lib.metric_residents_tenant(df_summary)}%")

## SPACER
st.write("#")

## Visualisations
st.subheader("Survey Responses Summary")
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
        summary_lib.filter_summary_data(df_summary, "building_floor"),
        x="Description",
        y="Number",
        title="Building Floor",
        log_y=False,
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title=None,
        yaxis_title="Number of Responses",
        xaxis = {"categoryorder": "category ascending"},
        plot_bgcolor=colour_palette['background'],
    )
    fig.update_xaxes(showgrid = False)
    fig.update_yaxes(showgrid = False)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

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
