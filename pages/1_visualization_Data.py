import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Visualization", layout="wide", page_icon="📊")

# Modern Theme CSS
st.markdown("""
<style>
    .header-viz {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E72 100%);
        padding: 30px 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .header-viz h1 {
        color: white;
        font-size: 2.2em;
        margin: 0;
        font-weight: 700;
    }
    
    .header-viz p {
        color: rgba(255, 255, 255, 0.9);
        margin: 10px 0 0 0;
    }
    
    .info-alert {
        background: rgba(255, 107, 107, 0.1);
        border-left: 4px solid #FF6B6B;
        padding: 15px;
        border-radius: 8px;
        color: #FF6B6B;
        margin: 15px 0;
    }
    
    .viz-section {
        background: #161B22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363D;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-viz">
    <h1>📊 Data Visualization Dashboard</h1>
    <p>Explore and visualize your loan data interactively with advanced charts</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# CHECK FOR UPLOADED DATA IN SESSION STATE
# ==========================================
if "uploaded_data" not in st.session_state or st.session_state["uploaded_data"] is None:
    st.markdown("""
    <div class="info-alert">
        ⬆️ Please upload a CSV file from the <strong>main page</strong> first.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

data = st.session_state["uploaded_data"]
st.success("✅ Data loaded successfully from session!")

# ==========================================
# DATA GROUPING & FEATURE ENGINEERING
# ==========================================
st.markdown("### 🔧 Data Processing")

# Create score groups for analysis
bins = [300, 579, 669, 740, 850]
labels = ['Poor', 'Fair', 'Good', 'Excellent']
data['credit_score_group'] = pd.cut(data['credit_score'], bins=bins, labels=labels, include_lowest=True).astype(str)

bins = [0, 35, 60, 100]
labels = ['Poor', 'Fair', 'Excellent']
data['points_score_group'] = pd.cut(data['points'], bins=bins, labels=labels, include_lowest=True).astype(str)

bins = [30053.00, 61000.00, 91000.00, 120000.00, 150000.00]
labels = ['Limited', 'Moderate', 'Solid', 'High']
data['income_score_group'] = pd.cut(data['income'], bins=bins, labels=labels, include_lowest=True).astype(str)

st.info("✅ Data grouping complete - Ready for visualization")

# ==========================================
# VISUALIZATION TABS
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(['📍 Scatter Plot', '🎻 Violin Plot', '📊 Histogram', '🍩 Donut & Countplot'])

# ==========================================
# TAB 1: SCATTER PLOT
# ==========================================
with tab1:
    st.markdown("<div class='viz-section'>", unsafe_allow_html=True)
    st.subheader("Scatter Plot Analysis")
    
    col1, col2, col3 = st.columns(3)
    numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    with col1:
        x_axis = st.selectbox("Select X axis", options=numeric_columns, index=0, key='x')
    with col2:
        y_axis = st.selectbox("Select Y axis", options=numeric_columns, index=1, key='y')
    with col3:
        color_option = st.selectbox("Select color", options=data.columns, index=2, key='color')
    
    if st.button('🎨 Visualize Scatter Plot', key='scatter_btn'):
        try:
            fig = px.scatter(
                data, 
                x=x_axis, 
                y=y_axis, 
                color=color_option,
                title=f"Scatter Plot: {y_axis} vs {x_axis}",
                hover_data=data.columns.tolist()[:5],
                template="plotly_dark",
                color_continuous_scale="Viridis"
            )
            fig.update_layout(
                height=600,
                font=dict(size=12),
                hovermode='closest'
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating scatter plot: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 2: VIOLIN PLOT
# ==========================================
with tab2:
    st.markdown("<div class='viz-section'>", unsafe_allow_html=True)
    st.subheader("Violin Plot Analysis")
    
    col1, col2 = st.columns(2)
    numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_columns = data.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
    
    with col1:
        x_axis = st.selectbox("Select X axis (categorical)", options=categorical_columns, index=0, key='x_violin')
    with col2:
        y_axis = st.selectbox("Select Y axis (numeric)", options=numeric_columns, index=0, key='y_violin')
    
    if st.button('🎨 Visualize Violin Plot', key='violin_btn'):
        try:
            fig = px.violin(
                data, 
                x=x_axis, 
                y=y_axis, 
                color=x_axis,
                title=f"Violin Plot: {y_axis} by {x_axis}",
                box=True, 
                points="all",
                template="plotly_dark"
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating violin plot: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 3: HISTOGRAM
# ==========================================
with tab3:
    st.markdown("<div class='viz-section'>", unsafe_allow_html=True)
    st.subheader("Histogram Distribution Analysis")
    
    col1, col2 = st.columns(2)
    numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    with col1:
        hist_column = st.selectbox("Select column for Histogram", options=numeric_columns, index=0, key='hist_col')
    with col2:
        bins_count = st.slider("Number of bins", min_value=10, max_value=100, value=50, step=5)
    
    if st.button('🎨 Visualize Histogram', key='hist_btn'):
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            fig.patch.set_facecolor('#0D1117')
            ax.set_facecolor('#161B22')
            
            if 'loan_approved' in data.columns:
                sns.histplot(
                    data=data, 
                    x=hist_column, 
                    bins=bins_count, 
                    kde=True,
                    hue='loan_approved', 
                    element="step", 
                    palette="Set2",
                    ax=ax
                )
            else:
                sns.histplot(
                    data=data, 
                    x=hist_column, 
                    bins=bins_count, 
                    kde=True,
                    element="step", 
                    palette="Set2",
                    ax=ax
                )
            
            ax.set_title(f"Distribution of {hist_column}", fontsize=14, color='white', fontweight='bold')
            ax.set_xlabel(hist_column, color='white')
            ax.set_ylabel("Frequency", color='white')
            ax.tick_params(colors='white')
            
            st.pyplot(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating histogram: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 4: DONUT & COUNTPLOT
# ==========================================
with tab4:
    st.markdown("<div class='viz-section'>", unsafe_allow_html=True)
    st.subheader("Categorical Analysis")
    
    options = ['credit_score_group', 'points_score_group', 'income_score_group']
    col1, col2 = st.columns(2)
    
    with col1:
        donut_column = st.selectbox("Select column for Donut chart", options=options, index=0, key='donut_col')
    with col2:
        countplot_column = st.selectbox("Select column for Countplot", options=options, index=1, key='countplot_col')
    
    if st.button('🎨 Visualize Charts', key='donut_btn'):
        try:
            col_viz1, col_viz2 = st.columns(2)
            
            with col_viz1:
                # Donut Chart
                donut_data = data[donut_column].value_counts().reset_index()
                donut_data.columns = [donut_column, 'count']
                
                fig1 = px.pie(
                    donut_data, 
                    names=donut_column, 
                    values='count',
                    title=f"Distribution of {donut_column}",
                    hole=0.6,
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    template="plotly_dark"
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col_viz2:
                # Countplot
                fig2, ax = plt.subplots(figsize=(10, 6))
                fig2.patch.set_facecolor('#0D1117')
                ax.set_facecolor('#161B22')
                
                if 'loan_approved' in data.columns:
                    sns.countplot(
                        data=data, 
                        x=countplot_column, 
                        hue='loan_approved', 
                        palette="husl",
                        ax=ax
                    )
                else:
                    sns.countplot(
                        data=data, 
                        x=countplot_column,
                        palette="husl",
                        ax=ax
                    )
                
                ax.set_title(f"Count Distribution: {countplot_column}", fontsize=14, color='white', fontweight='bold')
                ax.set_xlabel(countplot_column, color='white')
                ax.set_ylabel("Count", color='white')
                ax.tick_params(colors='white')
                
                st.pyplot(fig2, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error creating visualizations: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# DATA INSIGHTS
# ==========================================
st.markdown("### 📈 Quick Insights")

col_insight1, col_insight2, col_insight3 = st.columns(3)

with col_insight1:
    st.metric("Total Records", len(data), "rows")

with col_insight2:
    st.metric("Total Features", len(data.columns), "columns")

with col_insight3:
    if 'loan_approved' in data.columns:
        approval_rate = (data['loan_approved'].sum() / len(data) * 100)
        st.metric("Approval Rate", f"{approval_rate:.1f}%", "of loans")
