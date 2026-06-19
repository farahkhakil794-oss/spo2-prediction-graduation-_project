import streamlit as st
import pickle
import pandas as pd

# 1. تحميل الموديل
model = pickle.load(open('best_spo2_model (3).pkl', 'rb'))

st.title("المنظومة الطبية الذكية")

# 2. المدخلات
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", value=50.0)
    family_history_cad = st.selectbox("Family History CAD", [0, 1])
    noise_level_db = st.number_input("Noise Level dB", value=-30.0)
    pulse_rate_bpm = st.number_input("Pulse Rate BPM", value=75.0)
    pulse_transit_time_ms = st.number_input("Pulse Transit Time ms", value=200.0)
    augmentation_index_pct = st.number_input("Augmentation Index %", value=10.0)
    stiffness_index_m_s = st.number_input("Stiffness Index m/s", value=8.0)
    reflection_index_pct = st.number_input("Reflection Index %", value=50.0)
    systolic_peak_amplitude = st.number_input("Systolic Peak Amplitude", value=0.7)
    diastolic_peak_amplitude = st.number_input("Diastolic Peak Amplitude", value=0.4)

with col2:
    peak_to_peak_interval_ms = st.number_input("Peak-to-Peak Interval ms", value=800.0)
    pulse_wave_velocity_m_s = st.number_input("Pulse Wave Velocity m/s", value=8.0)
    perfusion_index_pct = st.number_input("Perfusion Index %", value=4.0)
    systolic_upstroke_time_ms = st.number_input("Systolic Upstroke Time ms", value=70.0)
    diastolic_time_ms = st.number_input("Diastolic Time ms", value=500.0)
    crest_time_ratio = st.number_input("Crest Time Ratio", value=0.1)
    ppg_signal_quality = st.number_input("PPG Signal Quality", value=0.7)
    motion_artifact_score = st.number_input("Motion Artifact Score", value=0.2)
    site_input = st.selectbox("Measurement Site", ["Fingertip", "Wrist"])
    measurement_site = 0 if site_input == "Fingertip" else 1

# 3. التوقع (بترتيب إجباري)
if st.button("توقع نسبة الأكسجين"):
    # إنشاء قاموس بالبيانات
    data_dict = {
        'age': [age], 'family_history_cad': [family_history_cad], 'noise_level_db': [noise_level_db],
        'pulse_rate_bpm': [pulse_rate_bpm], 'pulse_transit_time_ms': [pulse_transit_time_ms],
        'augmentation_index_pct': [augmentation_index_pct], 'stiffness_index_m_s': [stiffness_index_m_s],
        'reflection_index_pct': [reflection_index_pct], 'systolic_peak_amplitude': [systolic_peak_amplitude],
        'diastolic_peak_amplitude': [diastolic_peak_amplitude], 'peak_to_peak_interval_ms': [peak_to_peak_interval_ms],
        'pulse_wave_velocity_m_s': [pulse_wave_velocity_m_s], 'perfusion_index_pct': [perfusion_index_pct],
        'systolic_upstroke_time_ms': [systolic_upstroke_time_ms], 'diastolic_time_ms': [diastolic_time_ms],
        'crest_time_ratio': [crest_time_ratio], 'ppg_signal_quality': [ppg_signal_quality],
        'motion_artifact_score': [motion_artifact_score], 'measurement_site': [measurement_site]
    }
    
    input_df = pd.DataFrame(data_dict)
    
    # --- السطر السحري ---
    # هذا السطر يجبر الداتا أن تترتب بالضبط كما يحب الموديل
    if hasattr(model, 'feature_names_in_'):
        input_df = input_df[model.feature_names_in_]
    
    try:
        prediction = model.predict(input_df)
        st.success(f"النسبة المتوقعة للـ SpO2 هي: {prediction[0]:.2f}%")
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
        st.write("الأسماء التي يحتاجها الموديل هي:", model.feature_names_in_)
