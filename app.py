import streamlit as st
import pickle
import pandas as pd
import numpy as np

# إعدادات الصفحة لتكون متناسقة واحترافية
st.set_page_config(page_title="SpO2 Prediction System", layout="wide")

# تصميم واجهة مخصصة بالـ CSS لتطابق الألوان والستايل الأزرق بدقة
st.markdown("""
    <style>
    /* تصميم الهيدر الأزرق الكبير في أعلى الصفحة */
    .hero-banner {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        position: relative;
    }
    .hero-banner h1 {
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px;
        color: white !important;
    }
    .hero-banner p {
        font-size: 18px;
        opacity: 0.9;
        margin-bottom: 0;
    }
    /* تصميم العناوين الجانبية */
    .section-title {
        font-size: 22px;
        font-weight: bold;
        color: #1e3c72;
        margin-top: 20px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    /* تعديل صناديق الإدخال لتبدو متناسقة */
    div.stNumberInput input {
        border-radius: 8px !important;
        border: 1px solid #cbd5e1 !important;
        padding: 10px !important;
    }
    /* تصميم زر التوقع الأزرق المحترف */
    div.stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 15px 30px !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(37, 99, 235, 0.4) !important;
    }
    /* صندوق عرض النتيجة النهاییة المميز */
    .result-box {
        background-color: #f0fdf4;
        border: 2px solid #bbf7d0;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-top: 25px;
    }
    .result-box h2 {
        color: #166534 !important;
        font-size: 28px;
        margin-bottom: 5px;
    }
    .result-box p {
        font-size: 38px;
        font-weight: bold;
        color: #15803d;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# عرض الهيدر الاحترافي باللون الأزرق المتدرج في المقدمة
st.markdown("""
    <div class="hero-banner">
        <h1>المنظومة الذكية لتقدير نسبة الأكسجين (SpO2)</h1>
        <p>مشروع تخرج مبتكر يعتمد على إشارات الـ PPG والتعلم الآلي المتطور</p>
    </div>
""", unsafe_allow_html=True)

# تحميل موديل XGBoost المخزن
@st.cache_resource
def load_model():
    return pickle.load(open('best_spo2_model (3).pkl', 'rb'))

try:
    model = load_model()
except Exception as e:
    st.error(f"خطأ في تحميل الموديل: {e}")

st.markdown('<div class="section-title">📊 العوامل الحيوية للمريض (XGBoost Inputs)</div>', unsafe_allow_html=True)

# تقسيم المدخلات في عمودين متناسقين باستخدام صناديق الأرقام (Number Inputs)
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("العمر (Age)", min_value=1.0, max_value=120.0, value=64.0, step=1.0)
    family_history_cad = st.selectbox("التاريخ العائلي لأمراض الشرايين التاجية (Family History CAD)", [0, 1], help="0 = لا يوجد، 1 = يوجد")
    noise_level_db = st.number_input("مستوى الضوضاء (Noise Level dB)", value=-37.6, format="%.2f")
    pulse_rate_bpm = st.number_input("معدل النبض (Pulse Rate BPM)", min_value=30.0, max_value=220.0, value=70.0, format="%.2f")
    pulse_transit_time_ms = st.number_input("زمن انتقال النبضة (Pulse Transit Time ms)", min_value=50.0, max_value=600.0, value=238.0, step=1.0)
    augmentation_index_pct = st.number_input("مؤشر التضخيم (Augmentation Index %)", value=10.3, format="%.2f")
    stiffness_index_m_s = st.number_input("مؤشر الصلابة (Stiffness Index m/s)", value=8.67, format="%.2f")
    reflection_index_pct = st.number_input("مؤشر الانعكاس (Reflection Index %)", value=50.0, format="%.2f")
    systolic_peak_amplitude = st.number_input("سعة الذروة الانقباضية (Systolic Peak Amplitude)", value=0.7094, format="%.4f")

with col2:
    diastolic_peak_amplitude = st.number_input("سعة الذروة الانبساطية (Diastolic Peak Amplitude)", value=0.4069, format="%.4f")
    peak_to_peak_interval_ms = st.number_input("الفترة بين الذروتين (Peak-to-Peak Interval ms)", value=855.9, format="%.2f")
    pulse_wave_velocity_m_s = st.number_input("سرعة موجة النبض (Pulse Wave Velocity m/s)", value=8.64, format="%.2f")
    perfusion_index_pct = st.number_input("معامل الإرواء (Perfusion Index %)", value=4.26, format="%.2f")
    systolic_upstroke_time_ms = st.number_input("زمن الصعود الانقباضي (Systolic Upstroke Time ms)", value=72.4, format="%.2f")
    diastolic_time_ms = st.number_input("الزمن الانبساطي (Diastolic Time ms)", value=521.9, format="%.2f")
    crest_time_ratio = st.number_input("نسبة زمن القمة (Crest Time Ratio)", value=0.1218, format="%.4f")
    ppg_signal_quality = st.number_input("جودة إشارة الـ PPG (PPG Signal Quality)", min_value=0.0, max_value=1.0, value=0.70, format="%.2f")
    motion_artifact_score = st.number_input("مؤشر حركة المريض المشوشة (Motion Artifact Score)", value=0.26, format="%.2f")
    
    site_input = st.selectbox("مكان القياس (Measurement Site)", ["Fingertip", "Wrist"])
    measurement_site = 0 if site_input == "Fingertip" else 1

st.markdown("<br><br>", unsafe_allow_html=True)

# زر التوقع الكبير المتناسق باللون الأزرق المميز
if st.button("🔮 تشغيل محرك التوقع اللحظي", use_container_width=True):
    # تجميع المدخلات في DataFrame بنفس الترتيب الذي يحتاجه الموديل
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
        # حساب التوقع باستخدام الموديل الخاص بكِ
        prediction = model.predict(input_data)
        
        # تأثير الاحتفال بالنجاح
        st.balloons()
        
        # عرض النتيجة داخل كادر ملون رائع في منتصف الصفحة
        st.markdown(f"""
            <div class="result-box">
                <h2>نسبة الأكسجين المتوقعة بالدم SpO2</h2>
                <p>{prediction[0]:.2f} %</p>
            </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"حدث خطأ أثناء حساب التوقع: {e}")
