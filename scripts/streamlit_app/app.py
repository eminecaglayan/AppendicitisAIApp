# scripts/streamlit_app/app.py

from gelistiriciler import show_developers
from veri_bilgisi import show_data_info
from gecmis import show_history
from teshis import show_diagnosis
from anasayfa import show_home
import streamlit as st

# Sayfa ayarları
st.set_page_config(page_title="Apandisit Tanısında Yapay Zeka Destekli Karar Sistemi",
                   page_icon="📈", layout="centered")

# Oturum durumunda page değişkenini başlat
if "page" not in st.session_state:
    st.session_state.page = "Anasayfa"

# Kenar çubuğunda menü
pages = ["Anasayfa", "Teşhis", "Geçmiş", "Veri Bilgisi", "Geliştiriciler"]
st.sidebar.title("Menü")
# Radio seçimini al ve state'e ata
selection = st.sidebar.radio(
    "", pages, index=pages.index(st.session_state.page))
st.session_state.page = selection

# Sayfa modüllerini yükle

# Seçilen sayfayı göster
if st.session_state.page == "Anasayfa":
    show_home()
elif st.session_state.page == "Teşhis":
    show_diagnosis()
elif st.session_state.page == "Geçmiş":
    show_history()
elif st.session_state.page == "Veri Bilgisi":
    show_data_info()
elif st.session_state.page == "Geliştiriciler":
    show_developers()
