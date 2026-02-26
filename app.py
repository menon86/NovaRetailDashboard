import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("NovaRetail Customer Intelligence Dashboard")

# Load Data
df = pd.read_excel("NR_dataset.xlsx")

df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])

# Sidebar Filters

st.sidebar.header("Filters")

segment = st.sidebar.multiselect(
    "Customer Segment",
    df['label'].unique(),
    default=df['label'].unique()
)

region = st.sidebar.multiselect(
    "Region",
    df['CustomerRegion'].unique(),
    default=df['CustomerRegion'].unique()
)

category = st.sidebar.multiselect(
    "Category",
    df['ProductCategory'].unique(),
    default=df['ProductCategory'].unique()
)

channel = st.sidebar.multiselect(
    "Channel",
    df['RetailChannel'].unique(),
    default=df['RetailChannel'].unique()
)

age = st.sidebar.multiselect(
    "Age Group",
    df['CustomerAgeGroup'].unique(),
    default=df['CustomerAgeGroup'].unique()
)

date_range = st.sidebar.date_input(
    "Date Range",
    [df['TransactionDate'].min(), df['TransactionDate'].max()]
)

filtered = df[
(df['label'].isin(segment)) &
(df['CustomerRegion'].isin(region)) &
(df['ProductCategory'].isin(category)) &
(df['RetailChannel'].isin(channel)) &
(df['CustomerAgeGroup'].isin(age)) &
(df['TransactionDate'].between(pd.to_datetime(date_range[0]),
pd.to_datetime(date_range[1])))
]

# KPIs

col1,col2,col3,col4 = st.columns(4)

total_revenue = filtered['PurchaseAmount'].sum()
transactions = len(filtered)
avg_sat = filtered['CustomerSatisfaction'].mean()

top_segment = (
filtered.groupby('label')['PurchaseAmount']
.sum()
.idxmax()
)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Transactions", transactions)
col3.metric("Avg Satisfaction", round(avg_sat,2))
col4.metric("Top Segment", top_segment)

# Charts

col1,col2 = st.columns(2)

seg_rev = filtered.groupby('label')['PurchaseAmount'].sum().reset_index()
fig1 = px.bar(seg_rev,x='label',y='PurchaseAmount',
title="Revenue by Segment")
col1.plotly_chart(fig1,use_container_width=True)

cat_rev = filtered.groupby('ProductCategory')['PurchaseAmount'].sum().reset_index()
fig2 = px.bar(cat_rev,x='ProductCategory',y='PurchaseAmount',
title="Revenue by Category")
col2.plotly_chart(fig2,use_container_width=True)

col1,col2 = st.columns(2)

reg_rev = filtered.groupby('CustomerRegion')['PurchaseAmount'].sum().reset_index()
fig3 = px.bar(reg_rev,x='CustomerRegion',y='PurchaseAmount',
title="Revenue by Region")
col1.plotly_chart(fig3,use_container_width=True)

fig4 = px.pie(filtered,
values='PurchaseAmount',
names='RetailChannel',
title="Channel Distribution")
col2.plotly_chart(fig4,use_container_width=True)

sat = px.box(filtered,
x='label',
y='CustomerSatisfaction',
title="Satisfaction by Segment")
st.plotly_chart(sat,use_container_width=True)

trend = filtered.groupby('TransactionDate')['PurchaseAmount'].sum().reset_index()
fig6 = px.line(trend,
x='TransactionDate',
y='PurchaseAmount',
title="Revenue Trend")
st.plotly_chart(fig6,use_container_width=True)

st.subheader("Filtered Data")

st.dataframe(filtered)
