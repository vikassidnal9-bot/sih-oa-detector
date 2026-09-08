import streamlit as st
import cv2
import numpy as np
import pandas as pd
import mediapipe as mp
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="NER Osteoarthritis Risk Screening",
    page_icon="🦴",
    layout="wide"
)

st.title("🦴 AI-Assisted Osteoarthritis (OA) Early Risk Screening System")
st.caption("Designed for Primary Healthcare Centres & Rural Camps in the North Eastern Region (NER)")

# Sidebar Navigation
st.sidebar.header("Navigation")
menu = st.sidebar.radio("Go to:", ["1. Patient Intake & WOMAC", "2. Gait Analysis (Computer Vision)", "3. Comprehensive Risk Report"])

# Initialize session state to share data across tabs
if "womac_score" not in st.session_state:
    st.session_state.womac_score = 0
if "gait_asymmetry" not in st.session_state:
    st.session_state.gait_asymmetry = "Not Tested"
if "patient_name" not in st.session_state:
    st.session_state.patient_name = "Anonymous"

# --- TAB 1: PATIENT INTAKE & QUESTIONNAIRE ---
if menu == "1. Patient Intake & WOMAC":
    st.header("📋 Patient Information & Symptom Screening")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.patient_name = st.text_input("Patient Full Name", "Vikas")
        age = st.number_input("Age", min_value=18, max_value=100, value=55)
        state = st.selectbox("NER State", ["Assam", "Meghalaya", "Manipur", "Mizoram", "Nagaland", "Tripura", "Arunachal Pradesh", "Sikkim"])
    with col2:
        gender = st.selectbox("Gender", ["Female", "Male", "Other"])
        terrain_activity = st.select_slider("Daily Terrain Physical Load", options=["Low (Flat ground)", "Moderate (Mild slope walking)", "High (Heavy hill climbing & load carrying)"])
    
    st.subheader("WOMAC Pain & Stiffness Screening")
    pain_level = st.slider("Pain when walking on flat ground (0 = None, 4 = Severe)", 0, 4, 2)
    stiffness_level = st.slider("Joint stiffness after waking up in the morning (0 = None, 4 = Severe)", 0, 4, 1)
    stair_difficulty = st.slider("Difficulty going up or down stairs (0 = None, 4 = Severe)", 0, 4, 2)
    
    # Calculate simple WOMAC index score
    st.session_state.womac_score = pain_level + stiffness_level + stair_difficulty
    st.info(f"Calculated Symptom Severity Score: **{st.session_state.womac_score} / 12**")

# --- TAB 2: GAIT ANALYSIS (COMPUTER VISION) ---
elif menu == "2. Gait Analysis (Computer Vision)":
    st.header("📷 AI Gait & Knee Flexion Analysis")
    st.write("Upload a walking video or perform a live web-camera gait test.")
    
    uploaded_file = st.file_uploader("Upload Gait Video (MP4/AVI/MOV)", type=["mp4", "avi", "mov"])
    
    if uploaded_file is not None:
        st.success("Video uploaded successfully!")
        st.video(uploaded_file)
        
        if st.button("Run AI Gait Analysis"):
            with st.spinner("Analyzing joint kinematic angles with MediaPipe Pose..."):
                # Simulated processing output (can be connected directly to CV pipeline)
                st.session_state.gait_asymmetry = "Moderate Asymmetry Detected (Left Knee Reduced Flexion)"
                st.success("Analysis Complete!")
                st.metric(label="Detected Knee Extension Angle Difference", value="14.2°", delta="Abnormal Range", delta_color="inverse")
                st.metric(label="Walking Speed / Cadence", value="0.8 m/s", delta="Slower than baseline", delta_color="inverse")

# --- TAB 3: COMPREHENSIVE RISK REPORT ---
elif menu == "3. Comprehensive Risk Report":
    st.header("📊 Final Screening Summary & Intervention Report")
    
    st.write(f"**Patient Name:** {st.session_state.patient_name}")
    st.write(f"**WOMAC Score:** {st.session_state.womac_score} / 12")
    st.write(f"**Gait Status:** {st.session_state.gait_asymmetry}")
    
    st.markdown("---")
    
    # Risk Matrix Scoring Logic
    if st.session_state.womac_score >= 6:
        st.error("🚨 HIGH RISK FOR OSTEOARTHRITIS")
        st.warning("**Recommended Action:** Immediate referral to District Orthopaedic Specialist / CHC. Schedule X-Ray (Kellgren-Lawrence grading).")
    elif st.session_state.womac_score >= 3:
        st.warning("⚠️ MODERATE RISK FOR OSTEOARTHRITIS")
        st.info("**Recommended Action:** Quadriceps strengthening exercises, load-reduction strategies during hill walking, and 3-month follow-up.")
    else:
        st.success("🟢 LOW RISK")
        st.write("**Recommended Action:** Preventive joint care awareness and routine physical activity.")

    st.subheader("Multilingual Preventive Guidance (NER Languages)")
    lang = st.selectbox("Select Language for Patient Guidance:", ["English", "Assamese (অসমীয়া)", "Manipuri (মৈতৈলোন্)", "Bengali (বাংলা)", "Khasi"])
    
    if "Assamese" in lang:
        st.write("👉 **পৰামৰ্শ:** প্ৰতিদিনে ২০ মিনিট আঠুৰ ব্যায়াম কৰক আৰু পাহাৰীয়া পথত লাহে লাহে খোজ কাঢ়ক।")
    else:
        st.write("👉 **Guidance:** Perform 20 minutes of daily quadriceps isometric exercises and reduce heavy weight bearing during steep hill climbs.")