import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Data ─────────────────────────────────────────────────────────────────────
DATA = {
    "Jan": pd.DataFrame([
        {"Associate": "Yash",  "Floor Visits": 87, "Site Visits": 71, "Mark YES": 63, "Sugg NO": 24, "Pending": 3, "Sent": 60, "Backlog": 0, "Grand Total": 60},
        {"Associate": "Prath", "Floor Visits": 97, "Site Visits": 56, "Mark YES": 91, "Sugg NO":  6, "Pending": 1, "Sent": 90, "Backlog": 0, "Grand Total": 90},
        {"Associate": "Jiten", "Floor Visits": 29, "Site Visits": 17, "Mark YES":  5, "Sugg NO": 12, "Pending": 5, "Sent":  0, "Backlog": 0, "Grand Total":  0},
    ]),
    "Feb": pd.DataFrame([
        {"Associate": "Yash",  "Floor Visits": 62, "Site Visits": 57, "Mark YES": 36, "Sugg NO": 22, "Pending": 4, "Sent": 35, "Backlog": 3, "Grand Total": 38},
        {"Associate": "Prath", "Floor Visits": 73, "Site Visits": 59, "Mark YES": 51, "Sugg NO":  8, "Pending": 9, "Sent": 58, "Backlog": 1, "Grand Total": 59},
        {"Associate": "Jiten", "Floor Visits": 43, "Site Visits": 31, "Mark YES":  2, "Sugg NO": 29, "Pending": 0, "Sent":  2, "Backlog": 5, "Grand Total":  7},
        {"Associate": "Rutic", "Floor Visits": 36, "Site Visits": 36, "Mark YES": 14, "Sugg NO": 22, "Pending": 1, "Sent": 13, "Backlog": 0, "Grand Total": 13},
        {"Associate": "Harsh", "Floor Visits": 51, "Site Visits": 35, "Mark YES": 15, "Sugg NO": 20, "Pending": 0, "Sent": 26, "Backlog": 0, "Grand Total": 26},
    ]),
    "Mar": pd.DataFrame([
        {"Associate": "Yash",  "Floor Visits": 43, "Site Visits": 41, "Mark YES": 30, "Sugg NO": 13, "Pending": 0, "Sent": 29, "Backlog": 4, "Grand Total": 34},
        {"Associate": "Prath", "Floor Visits": 53, "Site Visits": 39, "Mark YES": 46, "Sugg NO":  7, "Pending": 0, "Sent": 32, "Backlog": 9, "Grand Total": 55},
        {"Associate": "Jiten", "Floor Visits": 31, "Site Visits": 23, "Mark YES":  3, "Sugg NO": 28, "Pending": 0, "Sent":  3, "Backlog": 0, "Grand Total":  3},
        {"Associate": "Rutic", "Floor Visits": 23, "Site Visits": 18, "Mark YES":  4, "Sugg NO": 19, "Pending": 0, "Sent":  3, "Backlog": 1, "Grand Total":  5},
        {"Associate": "Harsh", "Floor Visits": 55, "Site Visits": 46, "Mark YES": 35, "Sugg NO": 20, "Pending": 0, "Sent": 35, "Backlog": 0, "Grand Total": 35},
    ]),
}

MONTHS = list(DATA.keys())

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700;900&family=Syne:wght@700;800&display=swap');

/* ── Global ── */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main .block-container { padding: 2rem 3rem 4rem; max-width: 1400px; }
[data-testid="stAppViewContainer"] { background: #F0F4FA; }
[data-testid="stHeader"] { background: transparent; }

/* ── Hide streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }

/* ── Header ── */
.dash-header {
    display: flex; align-items: center; gap: 20px;
    margin-bottom: 2.5rem;
}
.dash-icon {
    width: 60px; height: 60px; border-radius: 18px;
    background: linear-gradient(135deg, #3B82F6, #2563EB);
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; box-shadow: 0 8px 24px rgba(59,130,246,0.35);
    flex-shrink: 0;
}
.dash-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem; font-weight: 800;
    color: #0F172A; letter-spacing: -0.02em;
    margin: 0; line-height: 1.1;
}
.dash-sub {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.18em;
    color: #94A3B8; text-transform: uppercase; margin-top: 4px;
}

/* ── Month Pills ── */
.stRadio > div { display: flex; gap: 8px; }
.stRadio label {
    background: white; border-radius: 50px;
    padding: 8px 28px; font-size: 0.72rem;
    font-weight: 800; letter-spacing: 0.15em;
    text-transform: uppercase; cursor: pointer;
    color: #94A3B8; border: 1px solid #E2E8F0;
    transition: all 0.2s;
}
.stRadio label:has(input:checked) {
    background: #0F172A; color: white;
    border-color: #0F172A;
}
.stRadio [data-testid="stMarkdownContainer"] { display: none; }

/* ── KPI Cards ── */
.kpi-card {
    background: white; border-radius: 24px;
    padding: 24px 24px 20px; position: relative;
    box-shadow: 0 4px 24px rgba(0,0,0,0.04);
    border: 1px solid rgba(255,255,255,0.8);
    overflow: hidden; height: 150px;
}
.kpi-card::before {
    content: ''; position: absolute;
    top: -40px; right: -40px;
    width: 110px; height: 110px;
    border-radius: 50%; opacity: 0.07;
}
.kpi-icon {
    font-size: 1.6rem; margin-bottom: 10px;
}
.kpi-label {
    font-size: 0.62rem; font-weight: 800; letter-spacing: 0.18em;
    text-transform: uppercase; color: #94A3B8; margin-bottom: 4px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.5rem; font-weight: 800;
    color: #0F172A; line-height: 1; margin-bottom: 10px;
}
.kpi-delta-up {
    display: inline-flex; align-items: center; gap: 4px;
    background: #ECFDF5; color: #059669;
    font-size: 0.68rem; font-weight: 800;
    padding: 3px 10px; border-radius: 8px;
}
.kpi-delta-down {
    display: inline-flex; align-items: center; gap: 4px;
    background: #FFF1F2; color: #E11D48;
    font-size: 0.68rem; font-weight: 800;
    padding: 3px 10px; border-radius: 8px;
}
.kpi-base { font-size: 0.62rem; color: #CBD5E1; font-weight: 700; font-style: italic; }

/* ── Section Cards ── */
.section-card {
    background: white; border-radius: 28px;
    padding: 28px 28px 24px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.04);
    border: 1px solid rgba(255,255,255,0.8);
    margin-bottom: 1rem;
}
.section-title {
    font-size: 0.62rem; font-weight: 800; letter-spacing: 0.22em;
    text-transform: uppercase; color: #0F172A;
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 20px;
}
.section-title-bar {
    width: 5px; height: 20px;
    border-radius: 4px; display: inline-block;
}

/* ── Leaderboard bars ── */
.lb-row { margin-bottom: 18px; }
.lb-meta {
    display: flex; justify-content: space-between;
    font-size: 0.68rem; font-weight: 800;
    text-transform: uppercase; margin-bottom: 6px;
}
.lb-name { color: #475569; }
.lb-val { color: #94A3B8; }
.lb-track {
    background: #F1F5F9; border-radius: 99px;
    height: 10px; overflow: hidden;
}
.lb-fill {
    height: 100%; border-radius: 99px;
    background: linear-gradient(90deg, #3B82F6, #6366F1);
    transition: width 0.8s ease;
}

/* ── Table ── */
.styled-table { width: 100%; border-collapse: collapse; }
.styled-table th {
    background: #F8FAFC; font-size: 0.6rem;
    font-weight: 800; letter-spacing: 0.18em;
    text-transform: uppercase; color: #94A3B8;
    padding: 14px 16px; text-align: center;
    border-bottom: 1px solid #F1F5F9;
}
.styled-table th:first-child { text-align: left; padding-left: 20px; }
.styled-table th:last-child  { text-align: right; padding-right: 20px; }
.styled-table td {
    padding: 14px 16px; text-align: center;
    font-size: 0.82rem; font-weight: 600;
    color: #475569; border-bottom: 1px solid #F8FAFC;
}
.styled-table td:first-child {
    text-align: left; padding-left: 20px;
    font-weight: 800; color: #0F172A;
    text-transform: uppercase; font-size: 0.78rem;
}
.styled-table td:last-child { text-align: right; padding-right: 20px; font-weight: 900; color: #0F172A; }
.badge-green {
    background: #ECFDF5; color: #059669;
    padding: 3px 10px; border-radius: 8px;
    font-weight: 800; font-size: 0.75rem;
}
.badge-amber {
    background: #FFFBEB; color: #D97706;
    padding: 3px 10px; border-radius: 8px;
    font-weight: 800; font-size: 0.75rem;
    border: 1px solid #FDE68A;
}
.badge-blue {
    color: #3B82F6; font-weight: 900;
}
.styled-table tfoot td {
    background: #0F172A; color: white;
    font-weight: 800; font-size: 0.78rem;
    padding: 16px; text-align: center;
}
.styled-table tfoot td:first-child { text-align: left; padding-left: 20px; letter-spacing: 0.15em; text-transform: uppercase; font-size: 0.62rem; color: #94A3B8; border-radius: 0 0 0 20px; }
.styled-table tfoot td:last-child  { text-align: right; padding-right: 20px; color: #60A5FA; font-size: 1.2rem; font-family: 'Syne', sans-serif; border-radius: 0 0 20px 0; }

/* ── Search box ── */
.stTextInput input {
    border-radius: 14px !important;
    border: 1.5px solid #E2E8F0 !important;
    font-size: 0.72rem !important; font-weight: 700 !important;
    letter-spacing: 0.1em !important; text-transform: uppercase !important;
    padding: 10px 16px !important; background: #F8FAFC !important;
}
.stTextInput input:focus { border-color: #3B82F6 !important; box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important; }
[data-testid="stTextInput"] label { display: none !important; }

/* ── Download button ── */
.stDownloadButton button {
    background: #0F172A !important; color: white !important;
    border-radius: 14px !important; border: none !important;
    font-size: 0.7rem !important; font-weight: 800 !important;
    letter-spacing: 0.12em !important; padding: 10px 22px !important;
}
.stDownloadButton button:hover { background: #1E293B !important; }

/* ── Divider ── */
hr { border: none; border-top: 1px solid #F1F5F9; margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────
def totals(df):
    return df[["Floor Visits","Site Visits","Mark YES","Sugg NO","Pending","Sent","Backlog","Grand Total"]].sum()

def delta_badge(val):
    if val > 0:
        return f'<span class="kpi-delta-up">▲ {int(val)}</span>'
    elif val < 0:
        return f'<span class="kpi-delta-down">▼ {int(abs(val))}</span>'
    return f'<span class="kpi-delta-up">— 0</span>'


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <div class="dash-icon">📊</div>
  <div>
    <div class="dash-title">EXECUTIVE DASHBOARD</div>
    <div class="dash-sub">📅 Performance Suite · Site Report Tracker 2024</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Month Selector ────────────────────────────────────────────────────────────
active_month = st.radio("Month", MONTHS, index=2, horizontal=True, label_visibility="collapsed")

df = DATA[active_month].copy()
prev_idx = MONTHS.index(active_month) - 1
prev_df = DATA[MONTHS[prev_idx]] if prev_idx >= 0 else None

curr_totals = totals(df)
prev_totals = totals(prev_df) if prev_df is not None else None

st.markdown("<br>", unsafe_allow_html=True)

# ── KPI Cards ────────────────────────────────────────────────────────────────
kpis = [
    ("🏢", "Total Tower Visits", int(curr_totals["Floor Visits"]),
     int(curr_totals["Floor Visits"] - prev_totals["Floor Visits"]) if prev_totals is not None else None),
    ("📍", "Total Site Visits", int(curr_totals["Site Visits"]),
     int(curr_totals["Site Visits"] - prev_totals["Site Visits"]) if prev_totals is not None else None),
    ("📄", "Total Reports Sent", int(curr_totals["Grand Total"]),
     int(curr_totals["Grand Total"] - prev_totals["Grand Total"]) if prev_totals is not None else None),
    ("⏳", "Pending Reports", int(curr_totals["Pending"]),
     int(curr_totals["Pending"] - prev_totals["Pending"]) if prev_totals is not None else None),
]

cols = st.columns(4, gap="medium")
for col, (icon, label, value, delta) in zip(cols, kpis):
    if delta is not None:
        badge = delta_badge(delta)
        delta_html = f'<span style="font-size:0.6rem;color:#CBD5E1;font-weight:700;margin-right:6px;">VS LAST MONTH</span>{badge}'
    else:
        delta_html = '<span class="kpi-base">BASE MONTH</span>'
    col.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      <div>{delta_html}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row ────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([4, 8], gap="large")

# Leaderboard
with left_col:
    st.markdown(f"""
    <div class="section-card" style="height:420px">
      <div class="section-title">
        <span class="section-title-bar" style="background:#3B82F6"></span>
        Reports Sent Leaderboard
        <span style="margin-left:auto;background:#F1F5F9;color:#94A3B8;font-size:0.58rem;padding:3px 10px;border-radius:99px;">{active_month.upper()} '24</span>
      </div>
    """, unsafe_allow_html=True)

    lb_df = df.sort_values("Grand Total", ascending=False)
    max_val = lb_df["Grand Total"].max() or 1
    for _, row in lb_df.iterrows():
        pct = (row["Grand Total"] / max_val) * 100
        st.markdown(f"""
        <div class="lb-row">
          <div class="lb-meta">
            <span class="lb-name">{row['Associate'].upper()}</span>
            <span class="lb-val">{int(row['Grand Total'])} REPORTS</span>
          </div>
          <div class="lb-track">
            <div class="lb-fill" style="width:{pct:.1f}%"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Bar Chart
with right_col:
    st.markdown("""
    <div class="section-card" style="height:420px; overflow:visible">
      <div class="section-title">
        <span class="section-title-bar" style="background:#6366F1"></span>
        Tower vs Site Activity Analysis
        <span style="margin-left:auto;display:flex;gap:16px">
          <span style="font-size:0.6rem;color:#94A3B8;font-weight:700;display:flex;align-items:center;gap:5px">
            <span style="width:9px;height:9px;border-radius:50%;background:#6366F1;display:inline-block"></span> TOWER
          </span>
          <span style="font-size:0.6rem;color:#94A3B8;font-weight:700;display:flex;align-items:center;gap:5px">
            <span style="width:9px;height:9px;border-radius:50%;background:#10B981;display:inline-block"></span> SITE
          </span>
        </span>
      </div>
    """, unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df["Associate"], x=df["Floor Visits"],
        name="Tower Visits", orientation="h",
        marker=dict(color="#6366F1", line=dict(width=0)),
        width=0.35,
    ))
    fig.add_trace(go.Bar(
        y=df["Associate"], x=df["Site Visits"],
        name="Site Visits", orientation="h",
        marker=dict(color="#10B981", line=dict(width=0)),
        width=0.35,
    ))
    fig.update_layout(
        barmode="group", bargap=0.25, bargroupgap=0.1,
        margin=dict(l=0, r=10, t=0, b=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False, height=290,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(
            showgrid=False, zeroline=False,
            tickfont=dict(family="DM Sans", size=11, color="#94A3B8"),
        ),
        font=dict(family="DM Sans"),
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E8F0", font_family="DM Sans"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Data Table ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
  <div class="section-title">
    <span class="section-title-bar" style="background:#F59E0B"></span>
    Detailed Performance Breakdown
    <span style="margin-left:8px;font-size:0.58rem;color:#CBD5E1;font-weight:600;letter-spacing:0.05em">Full ledger of associate outputs & conversions</span>
  </div>
""", unsafe_allow_html=True)

tc1, tc2, tc3 = st.columns([5, 3, 2], gap="small")
with tc1:
    search = st.text_input("", placeholder="🔍  Filter associate name...")
with tc3:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇  Export CSV", data=csv,
                       file_name=f"dashboard_{active_month.lower()}_2024.csv",
                       mime="text/csv", use_container_width=True)

filtered = df[df["Associate"].str.lower().str.contains(search.lower())] if search else df

show_backlog = active_month != "Jan"

# Build table HTML
cols_show = ["Associate","Floor Visits","Site Visits","Mark YES","Sugg NO","Pending","Sent"]
if show_backlog:
    cols_show.append("Backlog")
cols_show.append("Grand Total")

headers = "".join([f"<th>{c}</th>" for c in cols_show])

def row_html(r):
    def cell(col, val):
        v = int(val)
        if col == "Associate":
            return f"<td>{v}</td>"  # handled below
        if col == "Mark YES":
            return f'<td><span class="badge-green">{v}</span></td>'
        if col == "Sugg NO":
            return f'<td style="color:#F87171;font-weight:700">{v}</td>'
        if col == "Pending":
            badge = f'<span class="badge-amber">{v}</span>' if v > 0 else f'<span style="color:#E2E8F0">{v}</span>'
            return f'<td>{badge}</td>'
        if col == "Backlog":
            style = 'class="badge-blue"' if v > 0 else 'style="color:#E2E8F0"'
            return f'<td><span {style}>{v}</span></td>'
        if col == "Grand Total":
            return f'<td style="font-weight:900;color:#0F172A;text-align:right;padding-right:20px">{v}</td>'
        return f'<td>{v}</td>'

    cells = f'<td style="text-align:left;padding-left:20px;font-weight:800;color:#0F172A;text-transform:uppercase;font-size:0.76rem">{r["Associate"]}</td>'
    for c in cols_show[1:]:
        cells += cell(c, r[c])
    return f'<tr>{cells}</tr>'

body_rows = "".join([row_html(r) for _, r in filtered.iterrows()])

# Footer totals
t = totals(filtered)
def foot_cell(col, val):
    v = int(val)
    if col == "Mark YES":     return f'<td style="color:#34D399">{v}</td>'
    if col == "Sugg NO":      return f'<td style="color:#F87171">{v}</td>'
    if col == "Pending":      return f'<td style="color:#FBBF24">{v}</td>'
    if col == "Backlog":      return f'<td style="color:#60A5FA">{v}</td>'
    if col == "Sent":         return f'<td style="color:#E2E8F0">{v}</td>'
    if col == "Grand Total":  return f'<td style="font-size:1.2rem;font-weight:900;color:#60A5FA;text-align:right;padding-right:20px">{v}</td>'
    return f'<td style="color:#64748B">{v}</td>'

foot = '<td style="text-align:left;padding-left:20px;letter-spacing:0.15em;font-size:0.6rem;color:#64748B;border-radius:0 0 0 20px">TEAM AGGREGATE</td>'
for c in cols_show[1:]:
    foot += foot_cell(c, t[c])

table_html = f"""
<table class="styled-table">
  <thead><tr>{headers}</tr></thead>
  <tbody>{body_rows}</tbody>
  <tfoot><tr>{foot}</tr></tfoot>
</table>
"""
st.markdown(table_html, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
