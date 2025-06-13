# scripts/streamlit_app/anasayfa.py

import streamlit as st

# Anasayfa sayfası: proje açıklaması ve teşhise yönlendirme


def show_home():
    st.title("📈 Apandisit Teşhis Yardımcısı")
    st.markdown(
        "Bu uygulama apandisit teşhisine yardımcı olmak amacıyla geliştirilmiştir.")

    def go_to_teshis():
        # Sayfayı Teşhis olarak ayarla
        st.session_state.page = "Teşhis"

    st.button("Teşhise Git", on_click=go_to_teshis)
