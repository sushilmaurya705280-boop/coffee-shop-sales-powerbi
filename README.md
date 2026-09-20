 
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Coffee Sales Dashboard", layout="wide", page_icon="☕")
st.title("☕ Afficionado Coffee Roasters - 2025 Dashboard")
st.markdown("**By Sushil Maurya | Power BI to Streamlit**")

df = None
# Try to find any csv/xlsx
for f in os.listdir('.'):
    if f.lower().endswith(('.csv','.xlsx','.xls')):
        try:
            if f.endswith('.csv'):
                df = pd.read_csv(f)
            else:
                df = pd.read_excel(f, sheet_name=None)
                # if multiple sheets, take first big sheet
                if isinstance(df, dict):
                    for k,v in df.items():
                        if len(v) > 20:
                            df = v
                            break
                if isinstance(df, dict):
                    df = list(df.values())[0]
            if df is not None and len(df) > 5:
                st.caption(f"Loaded: {f} ({len(df)} rows)")
                break
        except Exception as e:
            st.write(f"Error reading {f}: {e}")

# If still no data, create sample data for demo
if df is None or len(df) < 5:
    st.warning("Original data nahi mila, sample data se dashboard dikha raha hu. Resume me chalega!")
    import numpy as np
    from datetime import datetime, timedelta
    np.random.seed(42)
    dates = [datetime(2025,1,1)+timedelta(days=i) for i in range(100)]
    products = ['Latte','Cappuccino','Espresso','Americano','Mocha']
    category = ['Coffee','Tea','Bakery']
    df = pd.DataFrame({
        'transaction_date': np.random.choice(dates, 500),
        'product_detail': np.random.choice(products, 500),
        'product_category': np.random.choice(category, 500),
        'transaction_qty': np.random.randint(1,5,500),
        'unit_price': np.random.uniform(3,7,500),
    })
    df['revenue'] = df['transaction_qty']*df['unit_price']

df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
if 'revenue' not in df.columns and 'transaction_qty' in df.columns and 'unit_price' in df.columns:
    df['revenue'] = df['transaction_qty']*df['unit_price']

c1,c2,c3 = st.columns(3)
c1.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")
c2.metric("Total Orders", f"{len(df)}")
c3.metric("Avg Order", f"${df['revenue'].mean():.2f}")

col1, col2 = st.columns(2)
with col1:
    if 'product_category' in df.columns:
        cat = df.groupby('product_category')['revenue'].sum().reset_index().sort_values('revenue', ascending=False)
        fig = px.bar(cat, x='product_category', y='revenue', color='revenue', title="Revenue by Category", color_continuous_scale='Oranges')
        st.plotly_chart(fig, use_container_width=True)
with col2:
    pcol = 'product_detail' if 'product_detail' in df.columns else df.columns[1]
    top = df.groupby(pcol)['revenue'].sum().sort_values(ascending=False).head(10).reset_index()
    fig2 = px.pie(top, values='revenue', names=pcol, hole=0.5, title=f"Top 10 {pcol}")
    st.plotly_chart(fig2, use_container_width=True)

if 'transaction_date' in df.columns:
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    daily = df.groupby(df['transaction_date'].dt.date)['revenue'].sum().reset_index()
    fig3 = px.line(daily, x='transaction_date', y='revenue', title="Daily Revenue Trend", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

st.dataframe(df.head(500), use_container_width=True)
