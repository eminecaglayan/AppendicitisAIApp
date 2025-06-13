# scripts/streamlit_app/veri_bilgisi.py

import streamlit as st
import pandas as pd

# Veri seti hakkında bilgi sayfası


def show_data_info():
    st.header("Veri Bilgisi")
    st.markdown("Kullanılan veri seti hakkında bilgiler:")
    try:
        df = pd.read_excel("outputs/filtered_for_final_m_filled.xlsx")
        st.write(
            f"⏳ Veri seti boyutu: {df.shape[0]} satır, {df.shape[1]} sütun")
        st.write("📑 Sütunlar:")
        st.write(df.columns.tolist())
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Veri okunurken hata: {e}")
