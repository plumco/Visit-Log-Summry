import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Executive Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
    .main {
        background-color: #F8FAFC;
    }
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        border: 1px solid #F1F5F9;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 800;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: #94a3b8;
        text-align: center;
        padding: 10px;
        font-size: 10px;
        font-weight: bold;
        letter-spacing: 2px;
        border-top: 1px solid #F1F5F9;
    }
    </style>
    """, unsafe_allow_html=True)

# Data Store based on provided images
DATA = {
    "January": [
        {"Associate ID": "Yash", "Floor Visit": 87, "Site Visit": 71, "Report Mark (YES)": 63, "Suggestion (NO)": 24, "Pending": 3, "Sent": 60, "Backlog": 0, "Total": 60},
        {"Associate ID": "Prath", "Floor Visit": 97, "Site Visit": 56, "Report Mark (YES)": 91, "Suggestion (NO)": 6, "Pending": 1, "Sent": 90, "Backlog": 0, "Total": 90},
        {"Associate ID": "Jiten", "Floor Visit": 29, "Site Visit": 17, "Report Mark (YES)": 5, "Suggestion (NO)": 12, "Pending": 5, "Sent": 0, "Backlog": 0, "Total": 0},
    ],
    "February": [
        {"Associate ID": "Yash", "Floor Visit": 62, "Site Visit": 57, "Report Mark (YES)": 36, "Suggestion (NO)": 22, "Pending": 4, "Sent": 35, "Backlog": 3, "Total": 38},
        {"Associate ID": "Prath", "Floor Visit": 73, "Site Visit": 59, "Report Mark (YES)": 51, "Suggestion (NO)": 8, "Pending": 9, "Sent": 58, "Backlog": 1, "Total": 59},
        {"Associate ID": "Jiten", "Floor Visit": 43, "Site Visit": 31, "Report Mark (YES)": 2, "Suggestion (NO)": 29, "Pending": 0, "Sent": 2, "Backlog": 5, "Total": 7},
        {"Associate ID": "Rutic", "Floor Visit": 36, "Site Visit": 36, "Report Mark (YES)": 14, "Suggestion (NO)": 22, "Pending": 1, "Sent": 13, "Backlog": 0, "Total": 13},
        {"Associate ID": "Harsh", "Floor Visit": 51, "Site Visit": 35, "Report Mark (YES)": 15, "Suggestion (NO)": 20, "Pending": 0, "Sent": 26, "Backlog": 0, "Total": 26},
    ],
    "March": [
        {"Associate ID": "Yash", "Floor Visit": 43, "Site Visit": 41, "Report Mark (YES)": 30, "Suggestion (NO)": 13, "Pending": 0, "Sent": 29, "Backlog": 4, "Total": 33},
        {"Associate ID": "Prath", "Floor Visit": 53, "Site Visit": 39, "Report Mark (YES)": 46, "Suggestion (NO)": 7, "Pending": 0, "Sent": 32, "Backlog": 9, "Total": 41},
        {"Associate ID": "Jiten", "Floor Visit": 31, "Site Visit": 23, "Report Mark (YES)": 3, "Suggestion (NO)": 28, "Pending": 0, "Sent": 3, "Backlog": 0, "Total": 3},
        {"Associate ID": "Rutic", "Floor Visit": 23, "Site Visit": 18, "Report Mark (YES)": 4, "Suggestion (NO)": 19, "Pending": 0, "Sent": 3, "Backlog": 1, "Total": 4},
        {"Associate ID": "Harsh", "Floor Visit": 55, "Site Visit": 46, "Report Mark (YES)": 35, "Suggestion (NO)": 20, "Pending": 0, "Sent": 35, "Backlog": 0, "Total": 35},
    ]
}

# Sidebar Navigation
st.sidebar.title("Navigation")
active_month = st.sidebar.selectbox("Select Month", options=list(DATA.keys()), index=2)
st.sidebar.markdown("---")
st.sidebar.info("This dashboard tracks associate field performance across multiple months.")

# Prepare Dataframes
df_current = pd.DataFrame(DATA[active_month])

# Calculate Totals
totals = df_current.sum(numeric_only=True)
prev_totals = None
if active_month == "February":
    prev_totals = pd.DataFrame(DATA["January"]).sum(numeric_only=True)
elif active_month == "March":
    prev_totals = pd.DataFrame(DATA["February"]).sum(numeric_only=True)

def get_delta(current, prev):
    if prev is None: return None
    return int(current - prev)

# Header
st.title("Executive Dashboard")
st.caption(f"Performance Analytics Suite • {active_month.upper()} 2024")

# KPI Rows
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Tower Visits", totals["Floor Visit"], delta=get_delta(totals["Floor Visit"], prev_totals["Floor Visit"] if prev_totals is not None else None))
m2.metric("Total Site Visits", totals["Site Visit"], delta=get_delta(totals["Site Visit"], prev_totals["Site Visit"] if prev_totals is not None else None))
m3.metric("Total Reports Sent", totals["Total"], delta=get_delta(totals["Total"], prev_totals["Total"] if prev_totals is not None else None))
m4.metric("Total Pending", totals["Pending"], delta=get_delta(totals["Pending"], prev_totals["Pending"] if prev_totals is not None else None), delta_color="inverse")

st.markdown("---")

# Charts Row
c1, c2 = st.columns([1, 1.5])

with c1:
    st.subheader("Reports Sent Leaderboard")
    fig_sent = px.bar(
        df_current.sort_values("Total", ascending=True),
        x="Total",
        y="Associate ID",
        orientation='h',
        text="Total",
        color_discrete_sequence=['#3B82F6'],
        template="plotly_white"
    )
    fig_sent.update_layout(showlegend=False, height=400, margin=dict(l=0, r=0, t=20, b=0))
    st.plotly_chart(fig_sent, use_container_width=True)

with c2:
    st.subheader("Tower vs Site Visits Breakdown")
    fig_visits = go.Figure()
    fig_visits.add_trace(go.Bar(
        y=df_current["Associate ID"],
        x=df_current["Floor Visit"],
        name='Tower Visits',
        orientation='h',
        marker_color='#6366f1'
    ))
    fig_visits.add_trace(go.Bar(
        y=df_current["Associate ID"],
        x=df_current["Site Visit"],
        name='Site Visits',
        orientation='h',
        marker_color='#10b981'
    ))
    fig_visits.update_layout(
        barmode='group',
        template="plotly_white",
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_visits, use_container_width=True)

# Table Section
st.subheader("Detailed Performance Breakdown")
search = st.text_input("Filter Associate by Name", "")
if search:
    df_display = df_current[df_current["Associate ID"].str.contains(search, case=False)]
else:
    df_display = df_current

# Style the dataframe
st.dataframe(df_display, use_container_width=True, hide_index=True)

# Totals Footer Row (Manual styling for emphasis)
t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.columns([1.5, 1, 1, 1, 1, 1, 1, 1, 1])
with t1: st.write("**TEAM TOTALS**")
with t2: st.write(f"**{totals['Floor Visit']}**")
with t3: st.write(f"**{totals['Site Visit']}**")
with t4: st.write(f"**{totals['Report Mark (YES)']}**")
with t5: st.write(f"**{totals['Suggestion (NO)']}**")
with t6: st.write(f"**{totals['Pending']}**")
with t7: st.write(f"**{totals['Sent']}**")
with t8: st.write(f"**{totals['Backlog']}**")
with t9: st.write(f"**{totals['Total']}**")

st.markdown('<div class="footer">GENERATED FOR EXECUTIVE REVIEW • PROPRIETARY FIELD ANALYTICS</div>', unsafe_allow_html=True)