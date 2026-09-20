import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Coffee Sales Dashboard", layout="wide", page_icon="☕")
st.title("☕ Afficionado Coffee Roasters - 2025 Dashboard")
st.markdown("**By Sushil Maurya | Power BI to Streamlit**")

df = None
for f in os.listdir('.'):
    if f.lower().endswith(('.csv','.xlsx','.xls')):
        try:
            if f.endswith('.csv'):
                df = pd.read_csv(f)
            else:
                xls = pd.read_excel(f, sheet_name=None)
                for v in xls.values():
                    if len(v) > 20:
                        df = v
                        break
            if df is not None and len(df) > 5:
                break
        except:
            pass

if df is None or len(df) < 5:
    st.info("Sample data se dashboard chal raha hai - Live hai!")
    np.random.seed(42)
    dates = [datetime(2025,1,1)+timedelta(days=i) for i in range(90)]
    df = pd.DataFrame({
        'transaction_date': np.random.choice(dates, 400),
        'product_detail': np.random.choice(['Latte','Cappuccino','Espresso','Mocha'], 400),
        'product_category': np.random.choice(['Coffee','Tea','Bakery'], 400),
        'transaction_qty': np.random.randint(1,4,400),
        'unit_price': np.random.uniform(3,7,400),
    })
    df['revenue'] = df['transaction_qty']*df['unit_price']

df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
if 'revenue' not in df.columns:
    if 'transaction_qty' in df.columns and 'unit_price' in df.columns:
        df['revenue'] = df['transaction_qty']*df['unit_price']

c1,c2,c3 = st.columns(3)
c1.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")
c2.metric("Total Orders", f"{len(df)}")
c3.metric("Avg Order", f"${df['revenue'].mean():.2f}")

col1,col2 = st.columns(2)
with col1:
    cat = df.groupby('product_category')['revenue'].sum().reset_index()
    fig = px.bar(cat, x='product_category', y='revenue', color='revenue', title="Revenue by Category", color_continuous_scale='Oranges')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    top = df.groupby('product_detail')['revenue'].sum().sort_values(ascending=False).head(8).reset_index()
    fig2 = px.pie(top, values='revenue', names='product_detail', hole=0.5, title="Top Products")
    st.plotly_chart(fig2, use_container_width=True)

df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
daily = df.groupby(df['transaction_date'].dt.date)['revenue'].sum().reset_index()
fig3 = px.line(daily, x='transaction_date', y='revenue', title="Daily Revenue Trend", markers=True)
st.plotly_chart(fig3, use_container_width=True)
st.dataframe(df.head(300), use_container_width=True)




