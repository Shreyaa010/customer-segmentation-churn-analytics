import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Customer Segmentation & Churn Analytics",
    page_icon="🏦",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("data/bank_churn_segmented.csv")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🔍 Dashboard Filters")

selected_country = st.sidebar.multiselect(
    "Geography",
    options=sorted(df["Geography"].unique()),
    default=sorted(df["Geography"].unique())
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

selected_segment = st.sidebar.multiselect(
    "Customer Segment",
    options=sorted(df["CustomerSegment"].unique()),
    default=sorted(df["CustomerSegment"].unique())
)

# =====================================================
# FILTER DATA
# =====================================================

df_filtered = df[
    (df["Geography"].isin(selected_country))
    & (df["Gender"].isin(selected_gender))
    & (df["CustomerSegment"].isin(selected_segment))
]

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_customers = len(df_filtered)

churned_customers = df_filtered["Exited"].sum()

retained_customers = total_customers - churned_customers

churn_rate = (
    df_filtered["Exited"].mean() * 100
    if total_customers > 0 else 0
)

active_customers = df_filtered["IsActiveMember"].sum()

avg_balance = (
    df_filtered["Balance"].mean()
    if total_customers > 0 else 0
)

avg_credit = (
    df_filtered["CreditScore"].mean()
    if total_customers > 0 else 0
)

# Geographic Risk Index

geo_risk = (
    df_filtered.groupby("Geography")["Exited"]
    .mean()
    .sort_values(ascending=False)
)

if len(geo_risk) > 0:
    highest_risk_region = geo_risk.index[0]
    highest_risk_value = geo_risk.iloc[0] * 100
else:
    highest_risk_region = "N/A"
    highest_risk_value = 0

# Engagement Drop Indicator

inactive_customers = df_filtered[
    df_filtered["IsActiveMember"] == 0
]

if len(inactive_customers) > 0:
    inactive_churn_rate = (
        inactive_customers["Exited"].mean() * 100
    )
else:
    inactive_churn_rate = 0

# =====================================================
# TITLE
# =====================================================

st.title("🏦 Customer Segmentation & Churn Analytics Dashboard")

st.markdown("---")

# =====================================================
# KPI SECTION
# =====================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Churn Rate",
    f"{churn_rate:.2f}%"
)

col3.metric(
    "Active Customers",
    f"{active_customers:,}"
)

col4.metric(
    "Average Credit Score",
    f"{avg_credit:.2f}"
)

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Churned Customers",
    f"{churned_customers:,}"
)

col6.metric(
    "Retained Customers",
    f"{retained_customers:,}"
)

col7.metric(
    "Average Balance",
    f"€{avg_balance:,.2f}"
)

col8.metric(
    "Highest Risk Region",
    highest_risk_region,
    f"{highest_risk_value:.2f}%"
)

st.metric(
    "Inactive Customer Churn Rate",
    f"{inactive_churn_rate:.2f}%"
)

st.markdown("---")

# =====================================================
# GEOGRAPHY ANALYSIS
# =====================================================

st.subheader("🌍 Geography-wise Churn Analysis")

geo_data = (
    df_filtered.groupby("Geography")["Exited"]
    .mean()
    .reset_index()
)

geo_data["Exited"] *= 100

fig_geo = px.bar(
    geo_data,
    x="Geography",
    y="Exited",
    text_auto=".2f",
    title="Churn Rate by Geography (%)"
)

st.plotly_chart(fig_geo, use_container_width=True)

# =====================================================
# GENDER ANALYSIS
# =====================================================

st.subheader("👨‍💼 Gender-wise Churn Analysis")

gender_data = (
    df_filtered.groupby("Gender")["Exited"]
    .mean()
    .reset_index()
)

gender_data["Exited"] *= 100

fig_gender = px.pie(
    gender_data,
    names="Gender",
    values="Exited",
    title="Gender Churn Distribution"
)

st.plotly_chart(fig_gender, use_container_width=True)

# =====================================================
# AGE GROUP ANALYSIS
# =====================================================

st.subheader("👥 Age Group Analysis")

age_data = (
    df_filtered.groupby("AgeGroup")["Exited"]
    .mean()
    .reset_index()
)

age_data["Exited"] *= 100

fig_age = px.bar(
    age_data,
    x="AgeGroup",
    y="Exited",
    text_auto=".2f",
    title="Churn Rate by Age Group (%)"
)

st.plotly_chart(fig_age, use_container_width=True)

# =====================================================
# CREDIT BAND ANALYSIS
# =====================================================

st.subheader("💳 Credit Score Band Analysis")

credit_data = (
    df_filtered.groupby("CreditBand")["Exited"]
    .mean()
    .reset_index()
)

credit_data["Exited"] *= 100

fig_credit = px.bar(
    credit_data,
    x="CreditBand",
    y="Exited",
    text_auto=".2f",
    title="Churn Rate by Credit Band (%)"
)

st.plotly_chart(fig_credit, use_container_width=True)

# =====================================================
# TENURE ANALYSIS
# =====================================================

st.subheader("📅 Tenure Group Analysis")

tenure_data = (
    df_filtered.groupby("TenureGroup")["Exited"]
    .mean()
    .reset_index()
)

tenure_data["Exited"] *= 100

fig_tenure = px.bar(
    tenure_data,
    x="TenureGroup",
    y="Exited",
    text_auto=".2f",
    title="Churn Rate by Tenure Group (%)"
)

st.plotly_chart(fig_tenure, use_container_width=True)

# =====================================================
# BALANCE SEGMENT ANALYSIS
# =====================================================

st.subheader("💵 Balance Segment Analysis")

balance_data = (
    df_filtered.groupby("BalanceSegment")["Exited"]
    .mean()
    .reset_index()
)

balance_data["Exited"] *= 100

fig_balance = px.bar(
    balance_data,
    x="BalanceSegment",
    y="Exited",
    text_auto=".2f",
    title="Churn Rate by Balance Segment (%)"
)

st.plotly_chart(fig_balance, use_container_width=True)

# =====================================================
# CUSTOMER SEGMENT ANALYSIS
# =====================================================

st.subheader("👥 Customer Segment Analysis")

segment_data = (
    df_filtered.groupby("CustomerSegment")["Exited"]
    .mean()
    .reset_index()
)

segment_data["Exited"] *= 100

fig_segment = px.bar(
    segment_data,
    x="CustomerSegment",
    y="Exited",
    text_auto=".2f",
    title="Churn Rate by Customer Segment (%)"
)

st.plotly_chart(fig_segment, use_container_width=True)

# =====================================================
# HIGH VALUE CUSTOMER ANALYSIS
# =====================================================

st.subheader("💰 High Value Customer Analysis")

high_value = df_filtered[
    df_filtered["Balance"] > 100000
]

if len(high_value) > 0:

    hv_churn = (
        high_value["Exited"].mean() * 100
    )

    revenue_risk = (
        high_value[
            high_value["Exited"] == 1
        ]["Balance"].sum()
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "High Value Customer Churn Rate",
        f"{hv_churn:.2f}%"
    )

    col2.metric(
        "Revenue At Risk",
        f"€{revenue_risk:,.2f}"
    )

# =====================================================
# SEGMENT DRILL DOWN
# =====================================================

st.subheader("🔎 Customer Segment Drill-Down")

selected_segment_detail = st.selectbox(
    "Select Segment",
    sorted(df_filtered["CustomerSegment"].unique())
)

segment_view = df_filtered[
    df_filtered["CustomerSegment"]
    == selected_segment_detail
]

st.write(
    f"Customers in Segment {selected_segment_detail}:",
    len(segment_view)
)

st.dataframe(segment_view.head(50))

# =====================================================
# HIGH VALUE CUSTOMER EXPLORER
# =====================================================

st.subheader("💎 High Value Customer Explorer")

st.dataframe(
    high_value[
        [
            "Geography",
            "Gender",
            "Age",
            "Balance",
            "EstimatedSalary",
            "Exited"
        ]
    ].head(50)
)

# =====================================================
# DATASET PREVIEW
# =====================================================

st.subheader("📋 Dataset Preview")

st.dataframe(df_filtered.head(20))

# =====================================================
# RECOMMENDATIONS
# =====================================================

st.subheader("💡 Business Recommendations")

st.success("""
1. Focus retention efforts on high-risk customer segments.

2. Improve engagement among inactive customers.

3. Develop geography-specific retention campaigns.

4. Reward loyal customers with long tenure.

5. Monitor high-value customers proactively.

6. Create personalized offers for churn-prone customers.
""")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Customer Segmentation & Churn Pattern Analytics in European Banking"
)