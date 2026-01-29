
import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import load_data
from data_cleaning import clean_students_data
from analytics import add_risk_levels, kpi_metrics
st.title("New version check")

# ----------------------------------
# Page configuration
# ----------------------------------
st.set_page_config(
    page_title="Student Mental Health Dashboard",
    layout="wide"
)

st.title("🧠 Student Mental Health Monitoring Dashboard")
st.write("Understanding how social media addiction affects students' mental well-being.")

# ----------------------------------
# Load and process data
# ----------------------------------
DATA_PATH = "data/raw/students_social_media_addiction.csv"

df = load_data(DATA_PATH)
df = clean_students_data(df)
df = add_risk_levels(df)

# ----------------------------------
# Sidebar filters
# ----------------------------------
st.sidebar.header("Filters")

gender = st.sidebar.multiselect(
    "Gender",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

academic_level = st.sidebar.multiselect(
    "Academic Level",
    options=df["academic_level"].unique(),
    default=df["academic_level"].unique()
)

country = st.sidebar.multiselect(
    "Country",
    options=df["country"].unique(),
    default=df["country"].unique()
)

filtered_df = df[
    (df["gender"].isin(gender)) &
    (df["academic_level"].isin(academic_level)) &
    (df["country"].isin(country))
]

# ----------------------------------
# KPIs
# ----------------------------------
metrics = kpi_metrics(filtered_df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Students", metrics["students"])
c2.metric("Avg Mental Health Score", metrics["avg_mental_health"])
c3.metric("Avg Addiction Score", metrics["avg_addiction"])
c4.metric("High Risk %", f"{metrics['high_risk_pct']}%")

st.markdown("---")

# ----------------------------------
# Visualizations
# ----------------------------------

st.subheader("📉 Social Media Usage vs Mental Health")
fig1 = px.scatter(
    filtered_df,
    x="avg_daily_usage_hours",
    y="mental_health_score",
    color="mental_health_risk",
    labels={
        "avg_daily_usage_hours": "Average Daily Usage (hours)",
        "mental_health_score": "Mental Health Score"
    }
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("😴 Sleep vs Mental Health Risk")
fig2 = px.box(
    filtered_df,
    x="mental_health_risk",
    y="sleep_hours_per_night",
    labels={
        "mental_health_risk": "Mental Health Risk",
        "sleep_hours_per_night": "Sleep Hours per Night"
    }
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📱 Platform-wise Addiction Score")
platform_df = (
    filtered_df
    .groupby("most_used_platform")["addicted_score"]
    .mean()
    .reset_index()
    .sort_values("addicted_score", ascending=False)
)

fig3 = px.bar(
    platform_df,
    x="most_used_platform",
    y="addicted_score",
    labels={
        "most_used_platform": "Platform",
        "addicted_score": "Average Addiction Score"
    }
)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("🧠 Mental Health Risk Distribution")
fig4 = px.pie(
    filtered_df,
    names="mental_health_risk"
)
st.plotly_chart(fig4, use_container_width=True)

# ----------------------------------
# Insights
# ----------------------------------
st.markdown("---")
st.subheader("🔍 Key Insights")

st.write("""
• Higher social media usage is associated with lower mental health scores  
• High-risk students tend to sleep less  
• Certain platforms show higher addiction scores  
• Mental health risk varies across student groups  
""")
