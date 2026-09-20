import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Coffee Sales Dashboard", layout="wide", page_icon="☕")
st.title("☕ Afficionado Coffee Roasters - 2025 Dashboard")
st.markdown("**By Sushil Maurya | Power BI to Streamlit**")

# Find data file automatically
files = [f for f in os.listdir('.') if f.lower().endswith(('.csv','.xlsx','.xls')) and 'app' not in f.lower()]
df = None
for f in files:
    try:
        if f.endswith('.csv'):
            df = pd.read_csv(f)
        else:
            df = pd.read_excel(f)
        if len(df) > 20:
            st.caption(f"Using file: {f}")
            break
    except:
        pass

if df is None:
    st.error("Data file load nahi hua, excel ka naam check karo")
    st.stop()

# Clean columns
df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

# Make revenue column if not exists
if 'revenue' not in df.columns:
    if 'transaction_qty' in df.columns and 'unit_price' in df.columns:
        df['revenue'] = df['transaction_qty'] * df['unit_price']

# Metrics
c1,c2,c3 = st.columns(3)
if 'revenue' in df.columns:
    c1.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")
    c2.metric("Total Orders", f"{len(df)}")
    c3.metric("Avg Order", f"${df['revenue'].mean():.2f}")

col1, col2 = st.columns(2)

with col1:
    if 'product_category' in df.columns:
        cat = df.groupby('product_category')['revenue'].sum().reset_index().sort_values('revenue', ascending=False)
        fig = px.bar(cat, x='product_category', y='revenue', color='revenue', title="Revenue by Product Category", color_continuous_scale='Oranges')
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if 'product_detail' in df.columns or 'product_type' in df.columns:
        pcol = 'product_detail' if 'product_detail' in df.columns else 'product_type'
        top = df.groupby(pcol)['revenue'].sum().sort_values(ascending=False).head(10).reset_index()
        fig2 = px.pie(top, values='revenue', names=pcol, hole=0.5, title=f"Top 10 {pcol}")
        st.plotly_chart(fig2, use_container_width=True)

# Daily trend
date_col = None
for dc in ['transaction_date','date','order_date']:
    if dc in df.columns:
        date_col = dc
        break

if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    daily = df.groupby(df[date_col].dt.date)['revenue'].sum().reset_index()
    fig3 = px.line(daily, x=date_col, y='revenue', title="Daily Revenue Trend", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Data Preview")
st.dataframe(df.head(500), use_container_width=True)
