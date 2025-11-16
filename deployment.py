import pandas as pd
import streamlit as st
import seaborn as sns
import plotly.express as px
import os
import io

# ==========================================
# PAGE CONFIG & THEME
# ==========================================
st.set_page_config(
    page_title="Loan Approval Dashboard",
    layout="wide",
    page_icon="🏦",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
st.markdown("""
<style>
    /* Main theme */
    :root {
        --primary-color: #0066CC;
        --secondary-color: #00D9FF;
        --success-color: #00CC77;
        --danger-color: #FF6B6B;
        --dark-bg: #0F1117;
        --card-bg: #161B22;
        --text-primary: #C9D1D9;
        --text-secondary: #8B949E;
    }
    
    /* Remove default streamlit padding */
    .main {
        padding-top: 0;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #0066CC 0%, #00D9FF 100%);
        padding: 40px 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
    }
    
    .header-container h1 {
        color: white;
        font-size: 2.5em;
        margin: 0;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .header-container p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1em;
        margin: 10px 0 0 0;
    }
    
    /* Card styling */
    .card {
        background: linear-gradient(135deg, #161B22 0%, #0D1117 100%);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #30363D;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        border-color: #00D9FF;
        box-shadow: 0 4px 16px rgba(0, 217, 255, 0.2);
    }
    
    /* File uploader styling */
    .uploadedFile {
        background: linear-gradient(135deg, #1F6FEB 0%, #00D9FF 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        font-weight: 600;
    }
    
    /* Stat boxes */
    .stat-box {
        background: linear-gradient(135deg, #0066CC 0%, #004A99 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-size: 1.3em;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.25);
    }
    
    .stat-box.success {
        background: linear-gradient(135deg, #00CC77 0%, #009A56 100%);
        box-shadow: 0 4px 12px rgba(0, 204, 119, 0.25);
    }
    
    .stat-box.info {
        background: linear-gradient(135deg, #00D9FF 0%, #0099CC 100%);
        box-shadow: 0 4px 12px rgba(0, 217, 255, 0.25);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #0066CC 0%, #00D9FF 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 102, 204, 0.4);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        border-bottom: 2px solid #30363D;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        color: #8B949E;
        font-weight: 600;
        padding: 12px 20px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        color: #00D9FF;
        border-bottom: 3px solid #00D9FF;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #161B22 0%, #0D1117 100%);
        border-radius: 8px;
        border: 1px solid #30363D;
    }
    
    /* Alert styling */
    .success-box {
        background: rgba(0, 204, 119, 0.1);
        border-left: 4px solid #00CC77;
        padding: 15px;
        border-radius: 8px;
        color: #00CC77;
        margin: 15px 0;
    }
    
    .warning-box {
        background: rgba(255, 182, 91, 0.1);
        border-left: 4px solid #FFB65B;
        padding: 15px;
        border-radius: 8px;
        color: #FFB65B;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# INITIALIZE SESSION STATE
# ==========================================
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None
if "uploaded_data" not in st.session_state:
    st.session_state["uploaded_data"] = None

# ==========================================
# HEADER
# ==========================================
st.markdown("""
<div class="header-container">
    <h1>🏦 Loan Approval Dashboard</h1>
    <p>Modern Analytics & Predictive Intelligence for Loan Decisions</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# FILE UPLOAD SECTION
# ==========================================
st.markdown("### 📂 Data Upload & Management")

col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Upload your CSV file",
        type=["csv"],
        help="Drag and drop your CSV file or click to browse",
        label_visibility="collapsed"
    )

with col2:
    if st.session_state["uploaded_file"] is not None:
        if st.button("🔄 Clear Data", use_container_width=True):
            st.session_state["uploaded_file"] = None
            st.session_state["uploaded_data"] = None
            st.rerun()

# ==========================================
# PROCESS & STORE UPLOADED FILE
# ==========================================
if uploaded_file is not None:
    # Store file in session state for persistence across tabs
    st.session_state["uploaded_file"] = uploaded_file
    
    # Load and cache data
    @st.cache_data(show_spinner=False)
    def load_data(file_object):
        return pd.read_csv(file_object)
    
    try:
        data = load_data(uploaded_file)
        st.session_state["uploaded_data"] = data
        
        # Success message with file info
        st.markdown(f"""
        <div class="success-box">
            ✅ File loaded successfully! | <strong>{uploaded_file.name}</strong> | Rows: {len(data)} | Columns: {len(data.columns)}
        </div>
        """, unsafe_allow_html=True)
        
        # ==========================================
        # DATA OVERVIEW
        # ==========================================
        st.markdown("### 📊 Data Overview")
        
        overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)
        
        with overview_col1:
            st.markdown(f"""
            <div class="stat-box">
                📈<br>{len(data)}<br><small>Total Rows</small>
            </div>
            """, unsafe_allow_html=True)
        
        with overview_col2:
            st.markdown(f"""
            <div class="stat-box info">
                🏛️<br>{len(data.columns)}<br><small>Columns</small>
            </div>
            """, unsafe_allow_html=True)
        
        with overview_col3:
            missing = data.isnull().sum().sum()
            st.markdown(f"""
            <div class="stat-box">
                ⚠️<br>{missing}<br><small>Missing Values</small>
            </div>
            """, unsafe_allow_html=True)
        
        with overview_col4:
            if 'loan_approved' in data.columns:
                approved = (data['loan_approved'] == 1).sum()
                st.markdown(f"""
                <div class="stat-box success">
                    ✅<br>{approved}<br><small>Approved</small>
                </div>
                """, unsafe_allow_html=True)
        
        # ==========================================
        # DATA PREVIEW WITH CONTROLS
        # ==========================================
        st.markdown("### 📋 Data Preview")
        
        preview_col1, preview_col2 = st.columns([2, 1])
        
        with preview_col1:
            n_rows = st.slider(
                "Select number of rows to view",
                min_value=5,
                max_value=min(50, len(data)),
                value=10,
                step=1
            )
        
        with preview_col2:
            show_all_cols = st.checkbox("Show all columns", value=True)
        
        if show_all_cols:
            st.dataframe(
                data.head(n_rows),
                use_container_width=True,
                height=400
            )
        else:
            columns_to_show = st.multiselect(
                "Select columns to display",
                options=data.columns,
                default=data.columns.tolist()[:5]
            )
            st.dataframe(
                data[columns_to_show].head(n_rows),
                use_container_width=True,
                height=400
            )
        
        # ==========================================
        # DATA STATISTICS
        # ==========================================
        st.markdown("### 📈 Statistical Summary")
        
        stats_tab1, stats_tab2 = st.tabs(["Numeric Statistics", "Data Types"])
        
        with stats_tab1:
            st.dataframe(
                data.describe(),
                use_container_width=True
            )
        
        with stats_tab2:
            dtype_summary = pd.DataFrame({
                'Column': data.columns,
                'Data Type': data.dtypes.astype(str),
                'Non-Null Count': data.count(),
                'Null Count': data.isnull().sum()
            })
            st.dataframe(dtype_summary, use_container_width=True, hide_index=True)
        
        # ==========================================
        # DOWNLOAD OPTION
        # ==========================================
        st.markdown("### 💾 Download Data")
        
        col_download1, col_download2 = st.columns(2)
        
        with col_download1:
            csv = data.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"processed_{uploaded_file.name}",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_download2:
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                data.to_excel(writer, index=False)
            excel_buffer.seek(0)
            st.download_button(
                label="📊 Download as Excel",
                data=excel_buffer,
                file_name=f"processed_{uploaded_file.name.replace('.csv', '.xlsx')}",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    except Exception as e:
        st.markdown(f"""
        <div class="warning-box">
            ❌ Error loading file: {str(e)}
        </div>
        """, unsafe_allow_html=True)

else:
    # Show welcome message when no file is uploaded
    if st.session_state["uploaded_file"] is None:
        st.markdown("""
        <div class="card">
            <h3>🚀 Getting Started</h3>
            <p>Upload a CSV file containing loan data to begin:</p>
            <ul>
                <li><strong>Visualize</strong> your data with interactive charts</li>
                <li><strong>Predict</strong> loan approval using our ML model</li>
                <li><strong>Analyze</strong> patterns and insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-box">
            ⬆️ Please upload a CSV file to continue
        </div>
        """, unsafe_allow_html=True)
    else:
        # If data was previously uploaded, restore it
        st.success("✅ Previous data restored from session!")
