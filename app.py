import streamlit as st
import pickle
import pandas as pd
import numpy as np

# إعدادات الصفحة
st.set_page_config(page_title="SpO2 Prediction", layout="wide")

# تصميم واجهة مخصصة بالـ CSS لتبدو احترافية
st.markdown("""
    <style>
    .main-title {
        font-size: 32px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 18px;
        color: #4B5563;
        text-align: center;
        margin-bottom: 30px;
    }
    .section-header {
        font-size: 20px;
        font-weight: bold;
        color: #2563EB;
        border-bottom: 2px solid #DBEAFE;
        padding-bottom: 8px;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">المنظومة الذكية لتقدير نسبة الأكسجين (SpO2)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">مشروع تخرج مبتكر يعتمد على إشارات الـ PPG والتعلم الآلي المتطور</div>', unsafe_allow_html=True)

# تحميل الموديل
@st.cache_resource
def load_model():
    return pickle.load(open('best_spo2_model (3).pkl', 'rb'))

try:
    model = load_model()
except Exception as e:
    st.error(f"خطأ في تحميل الموديل: {e}")

st.markdown('<div class="section-header">📊 العوامل الحيوية للمريض (XGBoost Inputs)</div>', unsafe_allow_html=True)

# تقسيم المدخلات على شكل سلايدرز في عمودين متناسقين
col1, col2 = st.columns(2)

with col1:
    age = st.slider("العمر (Age)", min_value=1.0, max_value=100.0, value=64.0, step=1.0)
    family_history_cad = st.selectbox("التاريخ العائلي لأمراض الشرايين التاجية (Family History CAD)", [0, 1], help="0 = لا يوجد، 1 = يوجد")
    noise_level_db = st.slider("مستوى الضوضاء (Noise Level dB)", min_value=-100.0, max_value=0.0, value=-37.6, step=0.1)
    pulse_rate_bpm = st.slider("معدل النبض (Pulse Rate BPM)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
    pulse_transit_time_ms = st.slider("زمن انتقال النبضة (Pulse Transit Time ms)", min_value=100.0, max_value=500.0, value=238.0, step=1.0)
    augmentation_index_pct = st.slider("مؤشر التضخيم (Augmentation Index %)", min_value=-50.0, max_value=100.0, value=10.3, step=0.1)
    stiffness_index_m_s = st.slider("مؤشر الصلابة (Stiffness Index m/s)", min_value=1.0, max_value=25.0, value=8.67, step=0.01)
    reflection_index_pct = st.slider("مؤشر الانعكاس (Reflection Index %)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
    systolic_peak_amplitude = st.slider("سعة الذروة الانقباضية (Systolic Peak Amplitude)", min_value=0.0, max_value=5.0, value=0.7094, step=0.0001)

with col2:
    diastolic_peak_amplitude = st.slider("سعة الذروة الانبساطية (Diastolic Peak Amplitude)", min_value=0.0, max_value=5.0, value=0.4069, step=0.0001)
    peak_to_peak_interval_ms = st.slider("الفترة بين الذروتين (Peak-to-Peak Interval ms)", min_value=300.0, max_value=1500.0, value=855.9, step=0.1)
    pulse_wave_velocity_m_s = st.slider("سرعة موجة النبض (Pulse Wave Velocity m/s)", min_value=1.0, max_value=25.0, value=8.64, step=0.01)
    perfusion_index_pct = st.slider("معامل الإرواء (Perfusion Index %)", min_value=0.0, max_value=20.0, value=4.26, step=0.01)
    systolic_upstroke_time_ms = st.slider("زمن الصعود الانقباضي (Systolic Upstroke Time ms)", min_value=10.0, max_value=300.0, value=72.4, step=0.1)
    diastolic_time_ms = st.slider("الزمن الانبساطي (Diastolic Time ms)", min_value=100.0, max_value=1200.0, value=521.9, step=0.1)
    crest_time_ratio = st.slider("نسبة زمن القمة (Crest Time Ratio)", min_value=0.0, max_value=1.0, value=0.1218, step=0.0001)
    ppg_signal_quality = st.slider("جودة إشارة الـ PPG (PPG Signal Quality)", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
    motion_artifact_score = st.slider("مؤشر حركة المريض المشوشة (Motion Artifact Score)", min_value=0.0, max_value=5.0, value=0.26, step=0.01)
    
    site_input = st.selectbox("مكان القياس (Measurement Site)", ["Fingertip", "Wrist"])
    measurement_site = 0 if site_input == "Fingertip" else 1

st.markdown("<br><hr>", unsafe_allow_html=True)

# زر التوقع بتصميم واضح
if st.button("🔮 تشغيل محرك التوقع اللحظي", use_container_width=True):
    # تجميع المدخلات بنفس الترتيب تماماً
    input_data = pd.DataFrame({
        'age': [age],
        'family_history_cad': [family_history_cad],
        'noise_level_db': [noise_level_db],
        'pulse_rate_bpm': [pulse_rate_bpm],
        'pulse_transit_time_ms': [pulse_transit_time_ms],
        'augmentation_index_pct': [augmentation_index_pct],
        'stiffness_index_m_s': [stiffness_index_m_s],
        'reflection_index_pct': [reflection_index_pct],
        'systolic_peak_amplitude': [systolic_peak_amplitude],
        'diastolic_peak_amplitude': [diastolic_peak_amplitude],
        'peak_to_peak_interval_ms': [peak_to_peak_interval_ms],
        'pulse_wave_velocity_m_s': [pulse_wave_velocity_m_s],
        'perfusion_index_pct': [perfusion_index_pct],
        'systolic_upstroke_time_ms': [systolic_upstroke_time_ms],
        'diastolic_time_ms': [diastolic_time_ms],
        'crest_time_ratio': [crest_time_ratio],
        'ppg_signal_quality': [ppg_signal_quality],
        'motion_artifact_score': [motion_artifact_score],
        'measurement_site': [measurement_site]
    })
    
    try:
        # حساب التوقع
        prediction = model.predict(input_data)
        
        # عرض النتيجة بشكل ضخم ومميز
        st.balloons()
        st.metric(label="نسبة الأكسجين المتوقعة بالدم SpO2", value=f"{prediction[0]:.2f} %")
        
    except Exception as e:
        st.error(f"حدث خطأ أثناء حساب التوقع: {e}")
