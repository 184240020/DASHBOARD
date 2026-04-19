import streamlit as st
import pandas as pd

def load_data():
    # sesuai csv
    df = pd.read_csv("dataset/covid_19_indonesia_time_series_all.csv")
    return df

def show_data():
    df = load_data()
    
    # TUGAS 1: Footer Copyright
    st.markdown("---")
    st.caption("Copyright © Arman Maulana - 184240020")
    
    st.subheader("📌 Data COVID-19 Indonesia")
    
    # TUGAS 2: Total Kasus Keseluruhan
    total_kasus = df['Total Cases'].sum()
    st.metric(label="Total Kasus Keseluruhan", value=f"{total_kasus:,}")
    
    # TUGAS 3: Menampilkan kolom spesifik
    columns_to_show = ['Location', 'New Cases', 'Total Cases', 'Total Deaths', 'Total Recovered']
    
    st.dataframe(df[columns_to_show].head(10)) 
    
    # Menampilkan statistik deskriptif
    st.subheader("📊 Statistik Deskriptif Dataset")
    st.write(df.describe())

if __name__ == "__main__":
    show_data()