# profit_dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="Company Profit Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .stMetric {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">📊 Company Profit Dashboard</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎛️ Dashboard Controls")

# Function to generate or load data
@st.cache_data
def load_data():
    # Check if CSV files exist
    if os.path.exists('profit_data.csv'):
        df = pd.read_csv('profit_data.csv')
        df['Date'] = pd.to_datetime(df['Date'])
    else:
        # Generate sample data if files don't exist
        np.random.seed(42)
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
        
        data = []
        for date in dates:
            for product in products:
                if product == 'Product A':
                    base_price, base_cost = 50, 30
                    base_quantity = np.random.randint(50, 150)
                elif product == 'Product B':
                    base_price, base_cost = 75, 45
                    base_quantity = np.random.randint(30, 100)
                elif product == 'Product C':
                    base_price, base_cost = 100, 60
                    base_quantity = np.random.randint(20, 80)
                elif product == 'Product D':
                    base_price, base_cost = 35, 20
                    base_quantity = np.random.randint(60, 200)
                else:
                    base_price, base_cost = 150, 90
                    base_quantity = np.random.randint(10, 50)
                
                price = base_price * (1 + np.random.uniform(-0.1, 0.1))
                cost = base_cost * (1 + np.random.uniform(-0.1, 0.1))
                
                data.append({
                    'Date': date,
                    'Product': product,
                    'Unit_Price': round(price, 2),
                    'Unit_Cost': round(cost, 2),
                    'Quantity_Sold': base_quantity
                })
        
        df = pd.DataFrame(data)
        
        # Calculate profit
        df['Total_Sales'] = df['Unit_Price'] * df['Quantity_Sold']
        df['Total_Cost'] = df['Unit_Cost'] * df['Quantity_Sold']
        df['Profit'] = df['Total_Sales'] - df['Total_Cost']
        df['Profit_Margin'] = (df['Profit'] / df['Total_Sales']) * 100
    
    return df

# Load data
df = load_data()

# Sidebar filters
st.sidebar.subheader("📅 Date Range")
date_range = st.sidebar.date_input(
    "Select date range",
    value=(df['Date'].min(), df['Date'].max()),
    min_value=df['Date'].min(),
    max_value=df['Date'].max(),
    key='date_range'
)

# Product filter
st.sidebar.subheader("📦 Product Selection")
all_products = df['Product'].unique()
selected_products = st.sidebar.multiselect(
    "Select products",
    options=all_products,
    default=all_products
)

# Filter data
if len(date_range) == 2:
    mask = (df['Date'] >= pd.Timestamp(date_range[0])) & (df['Date'] <= pd.Timestamp(date_range[1]))
    filtered_df = df.loc[mask]
else:
    filtered_df = df

if selected_products:
    filtered_df = filtered_df[filtered_df['Product'].isin(selected_products)]

# Calculate metrics
total_sales = filtered_df['Total_Sales'].sum()
total_cost = filtered_df['Total_Cost'].sum()
total_profit = filtered_df['Profit'].sum()
avg_profit_margin = filtered_df['Profit_Margin'].mean()
roi = (total_profit / total_cost * 100) if total_cost > 0 else 0

# Main dashboard
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trends", "📦 Products", "📋 Data Table"])

with tab1:
    st.subheader("💰 Key Performance Indicators")
    
    # KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Sales",
            value=f"${total_sales:,.2f}",
            delta=f"{total_sales/1000:.1f}K"
        )
    
    with col2:
        st.metric(
            label="Total Cost",
            value=f"${total_cost:,.2f}",
            delta=f"{total_cost/1000:.1f}K"
        )
    
    with col3:
        st.metric(
            label="Total Profit",
            value=f"${total_profit:,.2f}",
            delta=f"{(total_profit/total_sales*100):.1f}%",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Avg Profit Margin",
            value=f"{avg_profit_margin:.2f}%",
            delta=f"{avg_profit_margin - 30:.1f}%"
        )
    
    with col5:
        st.metric(
            label="ROI",
            value=f"{roi:.2f}%",
            delta=f"{roi - 50:.1f}%"
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Profit Distribution by Product")
        product_profit = filtered_df.groupby('Product')['Profit'].sum().reset_index()
        fig_pie = px.pie(
            product_profit, 
            values='Profit', 
            names='Product',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("📈 Sales vs Cost vs Profit")
        metrics_data = pd.DataFrame({
            'Metric': ['Sales', 'Cost', 'Profit'],
            'Value': [total_sales, total_cost, total_profit]
        })
        fig_bar = px.bar(
            metrics_data, 
            x='Metric', 
            y='Value',
            color='Metric',
            color_discrete_sequence=['green', 'red', 'blue']
        )
        st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.subheader("📈 Trend Analysis")
    
    # Monthly trends
    filtered_df['Month'] = pd.to_datetime(filtered_df['Date']).dt.to_period('M').astype(str)
    monthly_data = filtered_df.groupby('Month').agg({
        'Total_Sales': 'sum',
        'Total_Cost': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    # Line chart for trends
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=monthly_data['Month'], 
        y=monthly_data['Total_Sales'],
        mode='lines+markers',
        name='Sales',
        line=dict(color='green', width=2)
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly_data['Month'], 
        y=monthly_data['Total_Cost'],
        mode='lines+markers',
        name='Cost',
        line=dict(color='red', width=2)
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly_data['Month'], 
        y=monthly_data['Profit'],
        mode='lines+markers',
        name='Profit',
        line=dict(color='blue', width=2)
    ))
    
    fig_trend.update_layout(
        title='Monthly Financial Trends',
        xaxis_title='Month',
        yaxis_title='Amount ($)',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Daily profit trend
    st.subheader("📅 Daily Profit Trend")
    daily_profit = filtered_df.groupby('Date')['Profit'].sum().reset_index()
    fig_daily = px.line(
        daily_profit, 
        x='Date', 
        y='Profit',
        title='Daily Profit Trend'
    )
    st.plotly_chart(fig_daily, use_container_width=True)

with tab3:
    st.subheader("📦 Product Performance Analysis")
    
    # Product summary
    product_summary = filtered_df.groupby('Product').agg({
        'Total_Sales': 'sum',
        'Total_Cost': 'sum',
        'Profit': 'sum',
        'Profit_Margin': 'mean',
        'Quantity_Sold': 'sum'
    }).round(2)
    
    product_summary['ROI'] = (product_summary['Profit'] / product_summary['Total_Cost'] * 100).round(2)
    
    # Product comparison chart
    fig_product = go.Figure(data=[
        go.Bar(name='Sales', x=product_summary.index, y=product_summary['Total_Sales']),
        go.Bar(name='Cost', x=product_summary.index, y=product_summary['Total_Cost']),
        go.Bar(name='Profit', x=product_summary.index, y=product_summary['Profit'])
    ])
    
    fig_product.update_layout(
        title='Product Performance Comparison',
        barmode='group',
        xaxis_title='Product',
        yaxis_title='Amount ($)'
    )
    
    st.plotly_chart(fig_product, use_container_width=True)
    
    # Product metrics table
    st.subheader("📊 Product Metrics Table")
    st.dataframe(
        product_summary.style.format({
            'Total_Sales': '${:,.2f}',
            'Total_Cost': '${:,.2f}',
            'Profit': '${:,.2f}',
            'Profit_Margin': '{:.2f}%',
            'ROI': '{:.2f}%'
        }).background_gradient(cmap='RdYlGn', subset=['Profit', 'ROI']),
        use_container_width=True
    )

with tab4:
    st.subheader("📋 Detailed Data Table")
    
    # Add download button
    col1, col2 = st.columns([6, 1])
    with col2:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f'profit_data_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv'
        )
    
    # Display data table
    st.dataframe(
        filtered_df.style.format({
            'Unit_Price': '${:.2f}',
            'Unit_Cost': '${:.2f}',
            'Total_Sales': '${:,.2f}',
            'Total_Cost': '${:,.2f}',
            'Profit': '${:,.2f}',
            'Profit_Margin': '{:.2f}%'
        }),
        use_container_width=True,
        height=600
    )
    
    # Summary statistics
    st.subheader("📊 Summary Statistics")
    st.write(filtered_df.describe())

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>💼 Company Profit Analysis Dashboard | Built with Streamlit 📊</p>
        <p>Formula: Profit = (Sales Price × Quantity) - (Cost × Quantity)</p>
    </div>
    """,
    unsafe_allow_html=True
)