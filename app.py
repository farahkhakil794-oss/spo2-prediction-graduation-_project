import streamlit as st
import pickle
import pandas as pd

# تحميل الموديل
model = pickle.load(open('best_spo2_model (3).pkl', 'rb'))

st.title("المنظومة الطبية الذكية")

# --- هذا الجزء للتشخيص (عشان نعرف الأسماء بالظبط) ---
if hasattr(model, 'feature_names_in_'):
    st.write("أسماء الأعمدة التي يتوقعها الموديل هي:")
    st.write(model.feature_names_in_)
# ----------------------------------------------------

# (ضعي مدخلاتك هنا كالعادة...)
# ... (نفس كود المدخلات السابق) ...

if st.button("توقع"):
    # عند الضغط، الكود سيطبع الخطأ الحقيقي في الـ UI
    try:
        # هنا سنقوم بإنشاء الـ DataFrame
        # **ملاحظة:** تأكدي أن الأسماء في القاموس (Dict) مطابقة تماماً للأسماء التي ستظهر لكِ على الشاشة بعد تشغيل الكود
        input_data = pd.DataFrame({
            'age': [age],
            'family_history_cad': [family_history_cad],
            # ... أكملي باقي الأعمدة بالأسماء التي ستظهر لكِ ...
        })
        
        # ترتيب الأعمدة (مهم جداً)
        input_data = input_data[model.feature_names_in_]
        
        prediction = model.predict(input_data)
        st.success(f"النتيجة: {prediction[0]}")
    except Exception as e:
        st.error(f"الخطأ هو: {e}")
