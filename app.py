import streamlit as st
import pickle
import numpy as np

# تحميل الموديل
model = pickle.load(open('best_spo2_model (3).pkl', 'rb'))

st.title("لوحة تحكم SpO2 الطبية")

# المدخلات - استخدمي Selectbox للبيانات النصية
site_mapping = {'Fingertip': 0, 'Wrist': 1} # إذا لم تعمل، جربي عكسها (Fingertip: 1, Wrist: 0)
site_input = st.selectbox("مكان القياس (Measurement Site)", list(site_mapping.keys()))
measurement_site_encoded = site_mapping[site_input]

# باقي المدخلات (يجب أن تكون بنفس ترتيب أعمدة التدريب)
# سأضع لكِ مثالاً، ويجب أن تضيفي باقي الأعمدة الموجودة في ملف الـ CSV الخاص بكِ
age = st.number_input("Age", value=50)
pulse_rate = st.number_input("Pulse Rate", value=75)
perfusion_index = st.number_input("Perfusion Index", value=4.0)

if st.button("توقع النتيجة"):
    # تجميع البيانات في مصفوفة (يجب أن يكون بنفس ترتيب أعمدة الـ X_train في تدريبك)
    # ملاحظة: إذا كان الموديل يتوقع عدداً محدداً من الأعمدة، يجب إضافتها هنا بالترتيب
    features = np.array([[age, pulse_rate, perfusion_index, measurement_site_encoded]])
    
    prediction = model.predict(features)
    st.success(f"نسبة الأكسجين المتوقعة: {prediction[0]:.2f}%")
