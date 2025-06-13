# scripts/streamlit_app/frontend.py

from PIL import Image
import streamlit as st
import requests
import pandas as pd
import os
import tempfile
import math

# 📁 Excel veri yolu (Docker uyumlu)
EXCEL_PATH = "outputs/filtered_for_final_m_filled.xlsx"

# 🌐 API adresi (Docker ortamında 'api' host adı kullanılabilir)
API_URL = os.environ.get("API_URL", "http://api:8000/predict")

# 🛑 Dışlanacak kolonlar
EXCLUDED_COLS = {"US_Number", "Diagnosis", "Appendix_Diameter", "Appendix_Diameter_Categorized"}

# 👇 Sayısal değişkenler
expected_numerical = [
    'Age', 'BMI', 'Height', 'Weight', 'Length_of_Stay', 'Body_Temperature',
    'WBC_Count', 'Neutrophil_Percentage', 'RBC_Count', 'Hemoglobin', 'RDW',
    'Thrombocyte_Count', 'CRP'
]

def sanitize_features(features_dict):
    safe_dict = {}
    for k, v in features_dict.items():
        if not k or v is None or k.strip() == "":
            continue
        try:
            if k in expected_numerical:
                v = float(str(v).replace(",", ".")) if not isinstance(v, (float, int)) else v
                if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                    v = 0.0
                safe_dict[k] = float(v)
            else:
                safe_dict[k] = str(v).strip().lower()
        except Exception as e:
            print(f"⚠️ Atlanan özellik: {k} → {v} ({e})")
            continue
    return safe_dict


# 🎛️ Streamlit Arayüz
st.set_page_config(page_title="Apandisit Teşhis Sistemi", layout="centered")
st.title("📈 Apandisit Teşhis Yardımcısı")
st.markdown("Lütfen hasta bilgilerini ve ultrason görüntüsünü giriniz:")

uploaded_file = st.file_uploader("Ultrason Görüntüsü (.jpg, .png, .bmp)", type=["jpg", "png", "bmp"])

# 📄 Excel verisini yükle
try:
    df = pd.read_excel(EXCEL_PATH)
    feature_cols = [col for col in df.columns if col not in EXCLUDED_COLS]
    default_row = df[df["US_Number"] == 904].iloc[0].to_dict()

    categorical_features = []
    numerical_features = []

    for col in feature_cols:
        series = df[col].dropna()
        unique_vals = series.unique()
        if series.dtype == "object" or len(unique_vals) <= 10:
            categorical_features.append((col, sorted(unique_vals.tolist())))
        else:
            numerical_features.append((col, series.dtype))

except Exception as e:
    st.error(f"Excel okunamadı: {e}")
    st.stop()

# 📝 Özellik girişi formu
st.subheader("🧾 Hasta Özellikleri")
features = {}

# Kategorik
for col, options in categorical_features:
    default_val = default_row.get(col)
    if default_val not in options:
        default_val = options[0]
    features[col] = st.selectbox(f"{col}:", options, index=options.index(default_val))

# Sayısal
for col, dtype in numerical_features:
    default_val = default_row.get(col, 0)
    if "int" in str(dtype):
        features[col] = st.number_input(f"{col}:", step=1, value=int(default_val))
    else:
        features[col] = st.number_input(f"{col}:", format="%.2f", value=float(default_val))

# 🔮 Tahmin
if uploaded_file and st.button("Teşhisi Al"):
    original_name = uploaded_file.name
    extension = os.path.splitext(original_name)[1].lower()
    UPLOAD_DIR = "uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    tmp_path = os.path.join(UPLOAD_DIR, original_name)


    try:
        image = Image.open(uploaded_file).convert("L")
        image.save(tmp_path)
    except Exception as e:
        st.error(f"Görsel kaydedilirken hata: {e}")
        st.stop()

    features = sanitize_features(features)

    payload = {
        "image_path": tmp_path,
        "features": features
    }

    with st.spinner("Model tahmin yapıyor..."):
        try:
            res = requests.post(API_URL, json=payload)
            res.raise_for_status()
            result = res.json()

            print("🖥️ API Yanıtı:", result)

            st.success("✅ Tahmin Başarılı!")
            st.markdown(f"**Apandis Çapı:** `{result['Appendix_Diameter']} mm`")
            kategori = ">6mm" if result['Appendix_Diameter_Categorized'] == 'yes' else "≤6mm"
            st.markdown(f"**Çap Kategorisi:** `{kategori}`")
            st.markdown(f"**Teşhis:** 🩺 `{result['Diagnosis'].upper()}`")
            st.markdown(f"**Güven Skoru:** `{round(result['Confidence'], 3)}`")
        except Exception as e:
            st.error(f"Hata oluştu: {e}")
