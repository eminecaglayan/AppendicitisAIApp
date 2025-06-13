# scripts/streamlit_app/gecmis.py

import os
import streamlit as st
import pandas as pd
import requests

# API adresi
API_URL = os.environ.get("API_URL", "http://api:8000")


def show_history():
    st.header("Geçmiş Kayıtlar")
    st.markdown("Geçmiş hastalar ve tanılar listesi:")
    try:
        res = requests.get(f"{API_URL}/history")
        res.raise_for_status()
        data = res.json()
        hastalar = pd.DataFrame(data.get("gecmis_hastalar", []))
        tanilar = pd.DataFrame(data.get("gecmis_tanilar", []))

        st.subheader("Geçmiş Hastalar")
        st.dataframe(hastalar)

        st.subheader("Geçmiş Tanılar")
        st.dataframe(tanilar)
    except Exception as e:
        st.error(f"Geçmiş veriler alınırken hata: {e}")
