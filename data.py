import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    # sesuai csv
    df = pd.read_csv("dataset/covid_19_indonesia_time_series_all.csv")
    return df

def filter_data(df, year=None):
    if year:
        df = df[df['Date'].str.contains(str(year))]
    return df
def select_year():
    return st.sidebar.selectbox(
    "Pilih Tahun 📅", 
    options=[None, 2020, 2021, 2022], 
    format_func=lambda x: "Semua Tahun" if x is None else str(x)
)
def show_data(df):
        selected_columns = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns)
        df_selected = df[selected_columns]
        st.subheader("Data COVID-19 Indonesia 🇮🇩")
        st.dataframe(df_selected.head(10))
    
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

#Total Kasus
def total_case(df) :
    total_kasus = df['Total Cases'].sum()
    return total_kasus

#Total Kematian
def total_death(df) :
    total_mati = df['New Deaths'].sum()
    return total_mati

#Total Sembuh
def total_recovery(df) :
    df = load_data()
    total_sembuh = df['New Recovered'].sum()
    return total_sembuh

#Kolom
def kolom(df) :
    kasus = total_case(df)
    kematian = total_death(df)
    sembuh = total_recovery(df)
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Kasus 📈", value=kasus, border=True)
    col2.metric(label="Total Kematian ☠️", value=kematian, border=True)
    col3.metric(label="Total Sembuh 🏋", value=sembuh, border=True)
    
#piechart1
def pie_chart(df):
    #panggi data
    total_mati = total_death(df)
    total_sembuh = total_recovery(df)
    
    #dataframe
    data = {
        'Status': ['Meninggal', 'Sembuh'],
        'Jumlah': [total_mati, total_sembuh]
    }
    
    fig = px.pie(data, names='Status', values='Jumlah', title='Perbandingan Total Kematian VS Total Kesembuhan', hole=0.5, color_discrete_sequence=['#4de89f', '#ff6459'])
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    show_data()