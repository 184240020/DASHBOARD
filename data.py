import streamlit as st
import pandas as pd

def load_data():
    # Pastikan path file csv sudah benar sesuai di laptop kamu
    df = pd.read_csv("dataset/covid_19_indonesia_time_series_all.csv")
    return df

def show_data():
    df = load_data()
    st.subheader("📌 Data COVID-19 Indonesia")
    st.dataframe(df.head(10))  # Menampilkan 10 data pertama

    # Menampilkan statistik deskriptif dataset
    st.subheader("📊 Statistik Deskriptif Dataset")
    st.write(df.describe())  # Menampilkan statistik deskriptif