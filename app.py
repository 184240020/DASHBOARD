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
    #pilih tahun
    year = select_year()
    #load & filter data
    df = load_data()
    df_filtered = filter_data(df, year)
    kolom(df_filtered)
    pie_chart(df_filtered)
    
elif menu == "Halaman Data":
    judul()
    year = select_year()
    # load & filter data
    df = load_data()
    df_filtered = filter_data(df, year)
    show_data(df_filtered)