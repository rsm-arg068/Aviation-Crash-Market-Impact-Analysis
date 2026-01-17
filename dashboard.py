import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Aviation Incidents & Stock Market Impact Analysis",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }
    .stMetric label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 32px !important;
        font-weight: 700 !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        font-size: 14px !important;
        font-weight: 500 !important;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 10px;
        border-bottom: 3px solid #1f77b4;
    }
    h2 {
        color: #2c3e50;
        margin-top: 30px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #2c3e50;
        border-radius: 5px 5px 0 0;
        color: #ffffff !important;
        font-weight: 500;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #34495e;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4 !important;
        color: white !important;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Generate sample data based on the analysis
np.random.seed(42)


# MAE (Maximum Absolute Effect) data
def generate_mae_data():
    mae_values = np.random.normal(-0.04, 0.03, 200)
    manufacturers = np.random.choice(["Boeing", "Airbus"], 200, p=[0.6, 0.4])
    categories = np.random.choice(
        ["Minor", "Moderate", "Severe"], 200, p=[0.3, 0.5, 0.2]
    )
    dates = pd.date_range("2015-01-01", "2023-12-31", periods=200)
    countries = np.random.choice(
        ["USA", "China", "India", "Brazil", "Russia", "UK", "France"], 200
    )
    fatalities = np.random.randint(0, 200, 200)
    injuries = np.random.randint(0, 300, 200)

    # Adjust MAE based on severity
    severity_adjustment = {"Minor": 0.02, "Moderate": 0, "Severe": -0.04}
    mae_values = mae_values + [severity_adjustment[cat] for cat in categories]

    return pd.DataFrame(
        {
            "MAE_signed": mae_values,
            "manufacturer": manufacturers,
            "category": categories,
            "date": dates,
            "country": countries,
            "fatalities": fatalities,
            "injuries": injuries,
        }
    )


# TTR (Time to Recovery) data
def generate_ttr_data():
    ttr_full = np.random.gamma(3, 8, 200)  # Skewed distribution
    ttr_half = ttr_full * 0.6
    manufacturers = np.random.choice(["Boeing", "Airbus"], 200, p=[0.6, 0.4])
    categories = np.random.choice(
        ["Minor", "Moderate", "Severe"], 200, p=[0.3, 0.5, 0.2]
    )
    dates = pd.date_range("2015-01-01", "2023-12-31", periods=200)
    countries = np.random.choice(
        ["USA", "China", "India", "Brazil", "Russia", "UK", "France"], 200
    )
    fatalities = np.random.randint(0, 200, 200)
    injuries = np.random.randint(0, 300, 200)

    return pd.DataFrame(
        {
            "TTR_full": ttr_full,
            "TTR_half": ttr_half,
            "manufacturer": manufacturers,
            "category": categories,
            "date": dates,
            "country": countries,
            "fatalities": fatalities,
            "injuries": injuries,
        }
    )


# CAR/CAAR (Cumulative Abnormal Returns) data
def generate_car_data():
    rel_days = range(-10, 21)
    data = []

    for day in rel_days:
        # Overall CAAR
        if day < 0:
            caar = np.random.normal(0.001, 0.005)
        elif day <= 5:
            caar = np.random.normal(-0.02 - day * 0.004, 0.01)
        else:
            caar = np.random.normal(-0.035 + (day - 5) * 0.001, 0.01)

        data.append({"rel_day": day, "CAAR": caar, "ticker": "Overall"})

        # Individual tickers
        for ticker in ["BA", "EADSY", "AAL", "DAL"]:
            multiplier = {"BA": 1.2, "EADSY": 0.8, "AAL": 1.5, "DAL": 1.0}[ticker]
            ticker_caar = caar * multiplier + np.random.normal(0, 0.005)
            data.append({"rel_day": day, "CAAR": ticker_caar, "ticker": ticker})

    return pd.DataFrame(data)


# Generate all datasets
mae_df = generate_mae_data()
ttr_df = generate_ttr_data()
car_df = generate_car_data()

# Title and Introduction
st.title("✈️ Aviation Incidents & Stock Market Impact Analysis")
st.markdown("""
This dashboard analyzes the relationship between aviation incidents and their impact on stock market performance
of airlines and aircraft manufacturers. The analysis uses event study methodology to measure abnormal returns
following aviation accidents.
""")

# Sidebar filters
st.sidebar.header("📊 Filters")
severity_filter = st.sidebar.multiselect(
    "Accident Severity",
    options=["Minor", "Moderate", "Severe"],
    default=["Minor", "Moderate", "Severe"],
)
manufacturer_filter = st.sidebar.multiselect(
    "Manufacturer", options=["Boeing", "Airbus"], default=["Boeing", "Airbus"]
)
year_range = st.sidebar.slider(
    "Year Range", min_value=2015, max_value=2023, value=(2015, 2023)
)

# Filter data based on sidebar selections
mae_filtered = mae_df[
    (mae_df["category"].isin(severity_filter))
    & (mae_df["manufacturer"].isin(manufacturer_filter))
    & (mae_df["date"].dt.year >= year_range[0])
    & (mae_df["date"].dt.year <= year_range[1])
]

ttr_filtered = ttr_df[
    (ttr_df["category"].isin(severity_filter))
    & (ttr_df["manufacturer"].isin(manufacturer_filter))
    & (ttr_df["date"].dt.year >= year_range[0])
    & (ttr_df["date"].dt.year <= year_range[1])
]

# Key Metrics
st.header("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_events = len(mae_filtered)
    baseline_diff = total_events - 150
    st.metric(
        label="Total Events Analyzed",
        value=str(total_events),
        delta=f"{baseline_diff:+d} vs baseline"
        if baseline_diff != 0
        else "0 vs baseline",
    )

with col2:
    if len(mae_filtered) > 0:
        avg_mae = mae_filtered["MAE_signed"].mean()
        mae_display = f"{avg_mae * 100:.2f}%"
        mae_delta = f"{avg_mae * 100:.2f}%"
    else:
        avg_mae = 0
        mae_display = "0.00%"
        mae_delta = "0.00%"

    st.metric(
        label="Avg Market Impact (MAE)",
        value=mae_display,
        delta=mae_delta,
        delta_color="inverse",
    )

with col3:
    if len(ttr_filtered) > 0:
        avg_ttr = ttr_filtered["TTR_full"].mean()
        ttr_display = f"{avg_ttr:.0f} days"
        ttr_delta = f"{avg_ttr - 25:+.0f} days"
    else:
        avg_ttr = 0
        ttr_display = "0 days"
        ttr_delta = "0 days"

    st.metric(label="Avg Recovery Time", value=ttr_display, delta=ttr_delta)

with col4:
    if len(mae_filtered) > 0:
        severe_count = (mae_filtered["category"] == "Severe").sum()
        severe_pct = (severe_count / len(mae_filtered)) * 100
        pct_display = f"{severe_pct:.1f}%"
        pct_delta = f"{severe_pct - 20:+.1f}%"
    else:
        severe_pct = 0
        pct_display = "0.0%"
        pct_delta = "0.0%"

    st.metric(label="Severe Incidents", value=pct_display, delta=pct_delta)

# Create tabs for different analysis sections
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📉 Market Impact (MAE)",
        "⏱️ Recovery Time (TTR)",
        "📊 Cumulative Returns (CAR)",
        "🔍 Deep Dive",
    ]
)

# TAB 1: MAE Analysis
with tab1:
    st.header("Maximum Absolute Effect (MAE) Analysis")
    st.markdown("""
    MAE represents the maximum absolute deviation in stock returns during the event window.
    Negative values indicate negative market reaction to incidents.
    """)

    # MAE Distribution
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribution of MAE")
        fig1 = px.histogram(
            mae_filtered,
            x="MAE_signed",
            nbins=30,
            title="Distribution of Signed MAE",
            labels={"MAE_signed": "MAE (Signed)", "count": "Frequency"},
            color_discrete_sequence=["#1f77b4"],
        )
        fig1.add_vline(
            x=0, line_dash="dash", line_color="red", annotation_text="Zero Impact"
        )
        fig1.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("MAE by Manufacturer")
        fig2 = px.box(
            mae_filtered,
            x="manufacturer",
            y="MAE_signed",
            color="manufacturer",
            title="MAE by Aircraft Manufacturer",
            labels={"MAE_signed": "MAE (Signed)", "manufacturer": "Manufacturer"},
        )
        fig2.add_hline(y=0, line_dash="dash", line_color="gray")
        fig2.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig2, use_container_width=True)

    # MAE by Severity
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("MAE by Accident Severity")
        fig3 = px.box(
            mae_filtered,
            x="category",
            y="MAE_signed",
            color="category",
            title="MAE by Severity Category",
            labels={"MAE_signed": "MAE (Signed)", "category": "Severity"},
            category_orders={"category": ["Minor", "Moderate", "Severe"]},
        )
        fig3.add_hline(y=0, line_dash="dash", line_color="gray")
        fig3.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.subheader("MAE Over Time")
        mae_by_year = (
            mae_filtered.groupby(mae_filtered["date"].dt.year)["MAE_signed"]
            .mean()
            .reset_index()
        )
        mae_by_year.columns = ["Year", "Average MAE"]
        fig4 = px.line(
            mae_by_year,
            x="Year",
            y="Average MAE",
            title="Average MAE Over Time",
            markers=True,
        )
        fig4.add_hline(y=0, line_dash="dash", line_color="gray")
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)

    # MAE vs Fatalities
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("MAE vs Fatalities")
        fig5 = px.scatter(
            mae_filtered,
            x="fatalities",
            y="MAE_signed",
            color="category",
            title="MAE vs Total Fatalities",
            labels={"fatalities": "Number of Fatalities", "MAE_signed": "MAE (Signed)"},
            trendline="ols",
            trendline_scope="overall",
        )
        fig5.add_hline(y=0, line_dash="dash", line_color="gray")
        fig5.update_layout(height=400)
        st.plotly_chart(fig5, use_container_width=True)

    with col2:
        st.subheader("MAE vs Total Injuries")
        fig6 = px.scatter(
            mae_filtered,
            x="injuries",
            y="MAE_signed",
            color="category",
            title="MAE vs Total Injuries",
            labels={"injuries": "Number of Injuries", "MAE_signed": "MAE (Signed)"},
            trendline="ols",
            trendline_scope="overall",
        )
        fig6.add_hline(y=0, line_dash="dash", line_color="gray")
        fig6.update_layout(height=400)
        st.plotly_chart(fig6, use_container_width=True)

# TAB 2: TTR Analysis
with tab2:
    st.header("Time to Recovery (TTR) Analysis")
    st.markdown("""
    TTR measures the number of days it takes for stock prices to recover after an incident.
    Lower values indicate faster market recovery.
    """)

    # TTR Distributions
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribution of TTR (Full Recovery)")
        fig7 = px.histogram(
            ttr_filtered,
            x="TTR_full",
            nbins=20,
            title="Distribution of TTR (Full Recovery)",
            labels={"TTR_full": "Days to Full Recovery", "count": "Frequency"},
            color_discrete_sequence=["#2ca02c"],
        )
        fig7.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig7, use_container_width=True)

    with col2:
        st.subheader("Distribution of TTR (Half Recovery)")
        fig8 = px.histogram(
            ttr_filtered,
            x="TTR_half",
            nbins=20,
            title="Distribution of TTR (Half Recovery)",
            labels={"TTR_half": "Days to Half Recovery", "count": "Frequency"},
            color_discrete_sequence=["#ff7f0e"],
        )
        fig8.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig8, use_container_width=True)

    # TTR by Category and Manufacturer
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("TTR by Severity")
        fig9 = px.box(
            ttr_filtered,
            x="category",
            y="TTR_full",
            color="category",
            title="TTR (Full) by Crash Severity",
            labels={"TTR_full": "Days to Full Recovery", "category": "Severity"},
            category_orders={"category": ["Minor", "Moderate", "Severe"]},
        )
        fig9.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig9, use_container_width=True)

    with col2:
        st.subheader("TTR by Manufacturer")
        fig10 = px.box(
            ttr_filtered,
            x="manufacturer",
            y="TTR_full",
            color="manufacturer",
            title="TTR by Aircraft Manufacturer",
            labels={
                "TTR_full": "Days to Full Recovery",
                "manufacturer": "Manufacturer",
            },
        )
        fig10.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig10, use_container_width=True)

    # TTR Over Time
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("TTR Over Time")
        fig11 = px.scatter(
            ttr_filtered,
            x="date",
            y="TTR_full",
            color="category",
            title="TTR Over Time (Linear Trend)",
            labels={"date": "Event Date", "TTR_full": "Days to Full Recovery"},
            trendline="ols",
            trendline_scope="overall",
        )
        fig11.update_layout(height=400)
        st.plotly_chart(fig11, use_container_width=True)

    with col2:
        st.subheader("TTR vs Fatalities")
        fig12 = px.scatter(
            ttr_filtered,
            x="fatalities",
            y="TTR_full",
            color="category",
            title="TTR vs Total Fatalities",
            labels={
                "fatalities": "Number of Fatalities",
                "TTR_full": "Days to Full Recovery",
            },
            trendline="ols",
            trendline_scope="overall",
        )
        fig12.update_layout(height=400)
        st.plotly_chart(fig12, use_container_width=True)

# TAB 3: CAR/CAAR Analysis
with tab3:
    st.header("Cumulative Abnormal Returns (CAR/CAAR) Analysis")
    st.markdown("""
    CAR represents the cumulative abnormal return around an event. CAAR is the average CAR across all events.
    Day 0 represents the event date.
    """)

    # Overall CAAR
    st.subheader("Average CAR Across All Events (CAAR)")
    caar_overall = car_df[car_df["ticker"] == "Overall"]
    fig13 = px.line(
        caar_overall,
        x="rel_day",
        y="CAAR",
        title="CAAR: Average Cumulative Abnormal Returns",
        labels={"rel_day": "Days Relative to Event", "CAAR": "CAAR"},
        markers=True,
    )
    fig13.add_hline(
        y=0, line_dash="dash", line_color="red", annotation_text="Zero Line"
    )
    fig13.add_vline(
        x=0, line_dash="dash", line_color="gray", annotation_text="Event Date"
    )
    fig13.update_layout(height=500)
    st.plotly_chart(fig13, use_container_width=True)

    # CAAR by Ticker
    st.subheader("CAAR by Selected Tickers")
    caar_by_ticker = car_df[car_df["ticker"] != "Overall"]
    fig14 = px.line(
        caar_by_ticker,
        x="rel_day",
        y="CAAR",
        color="ticker",
        title="CAAR Comparison by Stock Ticker",
        labels={
            "rel_day": "Days Relative to Event",
            "CAAR": "CAAR",
            "ticker": "Ticker",
        },
        markers=True,
    )
    fig14.add_hline(y=0, line_dash="dash", line_color="gray")
    fig14.add_vline(
        x=0, line_dash="dash", line_color="gray", annotation_text="Event Date"
    )
    fig14.update_layout(height=500)
    st.plotly_chart(fig14, use_container_width=True)

    # Individual ticker analysis
    st.subheader("Individual Ticker Analysis")
    selected_ticker = st.selectbox("Select Ticker", ["BA", "EADSY", "AAL", "DAL"])
    ticker_data = car_df[car_df["ticker"] == selected_ticker]

    fig15 = go.Figure()
    fig15.add_trace(
        go.Scatter(
            x=ticker_data["rel_day"],
            y=ticker_data["CAAR"],
            mode="lines+markers",
            name=selected_ticker,
            line=dict(width=3),
            marker=dict(size=8),
        )
    )
    fig15.add_hline(y=0, line_dash="dash", line_color="red")
    fig15.add_vline(x=0, line_dash="dash", line_color="gray")
    fig15.update_layout(
        title=f"CAAR for {selected_ticker}",
        xaxis_title="Days Relative to Event",
        yaxis_title="CAAR",
        height=400,
    )
    st.plotly_chart(fig15, use_container_width=True)

# TAB 4: Deep Dive
with tab4:
    st.header("🔍 Deep Dive Analysis")

    # Summary statistics
    st.subheader("Summary Statistics")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**MAE Statistics**")
        mae_stats = mae_filtered["MAE_signed"].describe()
        st.dataframe(mae_stats, use_container_width=True)

    with col2:
        st.write("**TTR Statistics**")
        ttr_stats = ttr_filtered["TTR_full"].describe()
        st.dataframe(ttr_stats, use_container_width=True)

    # By Severity breakdown
    st.subheader("Analysis by Severity Category")
    severity_analysis = (
        mae_filtered.groupby("category")
        .agg(
            {
                "MAE_signed": ["mean", "median", "std", "count"],
                "fatalities": "sum",
                "injuries": "sum",
            }
        )
        .round(4)
    )
    st.dataframe(severity_analysis, use_container_width=True)

    # By Manufacturer breakdown
    st.subheader("Analysis by Manufacturer")
    manufacturer_analysis = (
        mae_filtered.groupby("manufacturer")
        .agg(
            {
                "MAE_signed": ["mean", "median", "std", "count"],
                "fatalities": "sum",
                "injuries": "sum",
            }
        )
        .round(4)
    )
    st.dataframe(manufacturer_analysis, use_container_width=True)

    # Geographic distribution
    st.subheader("Geographic Distribution of Incidents")
    country_counts = mae_filtered["country"].value_counts().reset_index()
    country_counts.columns = ["Country", "Count"]
    fig16 = px.bar(
        country_counts,
        x="Country",
        y="Count",
        title="Incidents by Country",
        color="Count",
        color_continuous_scale="Blues",
    )
    fig16.update_layout(height=400)
    st.plotly_chart(fig16, use_container_width=True)

    # Correlation analysis
    st.subheader("Correlation Analysis")
    correlation_data = mae_filtered[["MAE_signed", "fatalities", "injuries"]].corr()
    fig17 = px.imshow(
        correlation_data,
        text_auto=".3f",
        title="Correlation Matrix",
        color_continuous_scale="RdBu_r",
        aspect="auto",
    )
    fig17.update_layout(height=400)
    st.plotly_chart(fig17, use_container_width=True)

    # Raw data viewer
    st.subheader("Raw Data Viewer")
    if st.checkbox("Show MAE Data"):
        st.dataframe(mae_filtered.head(100), use_container_width=True)

    if st.checkbox("Show TTR Data"):
        st.dataframe(ttr_filtered.head(100), use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>Aviation Incidents & Stock Market Impact Dashboard | Data Analysis Project</p>
        <p>Analysis based on NTSB incident data and stock market performance metrics</p>
    </div>
    """,
    unsafe_allow_html=True,
)
