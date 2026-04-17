import streamlit as st
from data import *


def judul():
    # Judul dashboard
    st.title("📊 Dashboard COVID-19")
    st.write("Selamat datang di dashboard interaktif untuk menganalisis data COVID-19.")

st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman", ["Home","Halaman Data"])

if menu == "Home":
    judul()
elif menu == "Halaman Data":
    judul()
    show_data()