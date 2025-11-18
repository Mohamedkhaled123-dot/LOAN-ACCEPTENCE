import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Loan Prediction", layout="wide", page_icon="🔮")

# Modern Theme CSS
st.markdown("""
<style>
    .header-pred {
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
        padding: 30px 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
    }
    
    .header-pred h1 {
        color: white;
        font-size: 2.2em;
        margin: 0;
        font-weight: 700;
    }
    
    .header-pred p {
        color: rgba(255, 255, 255, 0.9);
        margin: 10px 0 0 0;
    }
    
    .input-section {
        background: #161B22;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #30363D;
        margin: 20px 0;
    }
    
    .approved-box {
        background: linear-gradient(135deg, #00CC77 0%, #009A56 100%);
        border: 2px solid #00CC77;
        padding: 30px;
        border-radius: 12px;
        color: white;
        text-align: center;
        font-size: 1.5em;
        font-weight: 700;
        box-shadow: 0 8px 24px rgba(0, 204, 119, 0.3);
    }
    
    .rejected-box {
        background: linear-gradient(135deg, #FF6B6B 0%, #CC4444 100%);
        border: 2px solid #FF6B6B;
        padding: 30px;
        border-radius: 12px;
        color: white;
        text-align: center;
        font-size: 1.5em;
        font-weight: 700;
        box-shadow: 0 8px 24px rgba(255, 107, 107, 0.3);
    }
    
    .score-card {
        background: linear-gradient(135deg, #1F6FEB 0%, #004A99 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-pred">
    <h1>🔮 Loan Approval Prediction Engine</h1>
    <p>AI-Powered Loan Decision System with Advanced Analytics</p>
</div>
""", unsafe_allow_html=True)

# ===============================
# CHECK FOR DATA & LOAD MODEL
# ===============================
try:
    model = joblib.load("loan_approval_pipeline.pkl")
    
    model_loaded = True
except:
    model_loaded = False
    st.error("❌ Model files not found. Please ensure 'loan_approval_model.pkl' and 'scaler.pkl' exist.")

# ===============================
# PREDICTION MODE SELECTION
# ===============================
st.markdown("### 📋 Prediction Mode")

pred_mode = st.radio("Choose prediction mode:", ["Single Prediction"], horizontal=True)

if pred_mode == "Single Prediction":
    # ===============================
    # SINGLE PREDICTION
    # ===============================
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    st.markdown("#### 👤 Applicant Information")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="My name")
    with col2:
        city = st.text_input("City", placeholder="Cairo")
    
    st.markdown("#### 💰 Financial Information")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        income = st.number_input(
            "Annual Income ($)",
            min_value=0.0,
            value=50000.0,
            step=1000.0,
            format="%.2f"
        )
    with col2:
        credit_score = st.number_input(
            "Credit Score",
            min_value=300.0,
            max_value=850.0,
            value=650.0,
            step=1.0,
            format="%.2f"
        )
    with col3:
        loan_amount = st.number_input(
            "Loan Amount ($)",
            min_value=0.0,
            value=100000.0,
            step=5000.0,
            format="%.2f"
        )
    
    st.markdown("#### 📊 Additional Details")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        years_employed = st.number_input(
            "Years Employed",
            min_value=0.0,
            value=5.0,
            step=0.5,
            format="%.1f"
        )
    with col2:
        points = st.number_input(
            "Credit Points",
            min_value=0.0,
            max_value=100.0,
            value=50.0,
            step=1.0,
            format="%.2f"
        )
    with col3:
        st.empty()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ===============================
    # FEATURE ENGINEERING FUNCTIONS
    # ===============================
    def create_income_group(x):
        if x < 61000:
            return 0
        elif x < 91000:
            return 1
        elif x < 120000:
            return 2
        else:
            return 3
    
    def create_credit_group(x):
        if x < 579:
            return 0
        elif x < 669:
            return 1
        elif x < 740:
            return 2
        else:
            return 3
    
    def create_points_group(x):
        if x < 30:
            return 0
        elif x < 65:
            return 1
        else:
            return 2
    
    # ===============================
    # PREDICT BUTTON
    # ===============================
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        predict_btn = st.button("🚀 Predict Loan Status", use_container_width=True)
    
    if predict_btn and model_loaded:
        # Build dataframe
        df = pd.DataFrame([{
            "income": income,
            "credit_score": credit_score,
            "loan_amount": loan_amount,
            "years_employed": years_employed,
            "points": points
        }])
        
        # Apply Feature Engineering
        df["income_score_group"] = df["income"].apply(create_income_group)
        df["credit_score_group"] = df["credit_score"].apply(create_credit_group)
        df["points_score_group"] = df["points"].apply(create_points_group)
        
        # IMPORTANT: same column order used during model training
        df_final = df[[
            "income",
            "credit_score",
            "loan_amount",
            "years_employed",
            "points",
            "credit_score_group",
            "points_score_group",
            "income_score_group",
        ]]
        
        # Scaling
        #scaled_data = scaler.transform(df_final)
        
        # Predict
        prediction = model.predict(df_final)[0]
        probability = model.predict_proba(df_final)[0]
        
        # ===============================
        # SHOW RESULTS
        # ===============================
        st.markdown("### 📊 Prediction Result")
        
        if prediction == 1:
            st.markdown(f"""
            <div class="approved-box">
                ✅ LOAN APPROVED<br>
                <small style="font-size: 0.8em; opacity: 0.9;">for {name if name else 'Applicant'}</small>
            </div>
            """, unsafe_allow_html=True)
            
            confidence = max(probability) * 100
            st.success(f"Confidence Score: {confidence:.2f}%")
        else:
            st.markdown(f"""
            <div class="rejected-box">
                ❌ LOAN REJECTED<br>
                <small style="font-size: 0.8em; opacity: 0.9;">for {name if name else 'Applicant'}</small>
            </div>
            """, unsafe_allow_html=True)
            
            confidence = max(probability) * 100
            st.error(f"Confidence Score: {confidence:.2f}%")
        
        # Show detailed metrics
        st.markdown("### 📈 Applicant Profile & Score")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="score-card">
                💰<br>${income:,.2f}<br><small>Annual Income</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="score-card">
                📊<br>{credit_score:.0f}<br><small>Credit Score</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="score-card">
                💵<br>${loan_amount:,.2f}<br><small>Loan Amount</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="score-card">
                ⏰<br>{years_employed:.1f}<br><small>Years Employed</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Processed data
        st.markdown("### 📋 Processed Features")
        st.dataframe(df_final, use_container_width=True, hide_index=True)

else:
    # ===============================
    # BATCH PREDICTION
    # ===============================
    st.markdown("### 📦 Batch Prediction from Uploaded Data")
    
    if "uploaded_data" in st.session_state and st.session_state["uploaded_data"] is not None:
        data = st.session_state["uploaded_data"]
        
        # Check for required columns
        required_cols = ["income", "credit_score", "loan_amount", "years_employed", "points"]
        missing_cols = [col for col in required_cols if col not in data.columns]
        
        if not missing_cols and model_loaded:
            st.info(f"✅ Found {len(data)} records to predict")
            
            if st.button("🚀 Predict for All Records", use_container_width=True):
                # Feature engineering
                df_batch = data[required_cols].copy()
                
                def create_income_group(x):
                    if x < 61000:
                        return 0
                    elif x < 91000:
                        return 1
                    elif x < 120000:
                        return 2
                    else:
                        return 3
                
                def create_credit_group(x):
                    if x < 579:
                        return 0
                    elif x < 669:
                        return 1
                    elif x < 740:
                        return 2
                    else:
                        return 3
                
                def create_points_group(x):
                    if x < 30:
                        return 0
                    elif x < 65:
                        return 1
                    else:
                        return 2
                
                df_batch["income_score_group"] = df_batch["income"].apply(create_income_group)
                df_batch["credit_score_group"] = df_batch["credit_score"].apply(create_credit_group)
                df_batch["points_score_group"] = df_batch["points"].apply(create_points_group)
                
                df_batch_final = df_batch[[
                    "income",
                    "credit_score",
                    "loan_amount",
                    "years_employed",
                    "points",
                    "credit_score_group",
                    "points_score_group",
                    "income_score_group",
                ]]
                
                # Predict
                
                predictions = model.predict(df_batch_final)
                probabilities = model.predict_proba(df_batch_final)
                
                # Add predictions to dataframe
                result_df = data.copy()
                result_df["prediction"] = predictions
                result_df["prediction_text"] = result_df["prediction"].apply(
                    lambda x: "✅ APPROVED" if x == 1 else "❌ REJECTED"
                )
                result_df["confidence"] = probabilities.max(axis=1) * 100
                
                # Show results
                st.markdown("### 📊 Batch Prediction Results")
                
                # Summary stats
                approved_count = (predictions == 1).sum()
                rejected_count = (predictions == 0).sum()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Predictions", len(result_df))
                with col2:
                    st.metric("✅ Approved", approved_count)
                with col3:
                    st.metric("❌ Rejected", rejected_count)
                
                # Show detailed results
                st.dataframe(
                    result_df[["prediction_text", "confidence", "income", "credit_score", "loan_amount"]],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Download results
                csv = result_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Predictions",
                    data=csv,
                    file_name="loan_predictions.csv",
                    mime="text/csv"
                )
        else:
            if missing_cols:
                st.warning(f"⚠️ Missing required columns: {', '.join(missing_cols)}")
    else:
        st.info("📂 Please upload a CSV file from the main page to use batch prediction")
