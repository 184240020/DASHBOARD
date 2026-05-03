import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    # sesuai csv
    df = pd.read_csv("dataset/covid_19_indonesia_time_series_all.csv")
    df = df[df["Location"] != "Indonesia"]
    return df

def filter_data(df, year=None, location=None):
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]
    if location and location != 'Semua Provinsi':
        df = df[df['Location'] == location]
    return df

def select_location(df):
    locations = ['Semua Provinsi'] + sorted (df['Location'].unique())
    return st.sidebar.selectbox(
        "Pilih Provinsi",
        options= locations)

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
    total_kasus = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_kasus['Total Cases'].sum()

#Total Kematian
def total_death(df) :
    total_mati = df['Total Deaths'].sum()
    return total_mati

#Total Sembuh
def total_recovery(df):
    total_sembuh = df['Total Recovered'].sum()
    return total_sembuh

#Kolom1
def kolom1(df) :
    kasus = total_case(df)
    kematian = total_death(df)
    sembuh = total_recovery(df)
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Kasus 📈", value=kasus, border=True)
    col2.metric(label="Total Kematian ☠️", value=kematian, border=True)
    col3.metric(label="Total Sembuh 🏋", value=sembuh, border=True)
    
#piechart1
def pie_chart1(df):
    #panggi data
    total_mati = total_death(df)
    total_sembuh = total_recovery(df)
    
    data = {
        'Status': ['Sembuh', 'meninggal'],
        'Jumlah': [total_sembuh, total_mati]
    }
    
    fig = px.pie(
        data, 
        names='Status', 
        values='Jumlah', 
        title='Perbandingan Total Kematian VS Total Kesembuhan', 
        hole=0.5, 
        color_discrete_sequence=['#ff6459', '#4de89f']
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
#Barchart1
def bar_chart1(df):
    #mengambil data terakhir per provinsi
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    
    # Ambil 5 provinsi dengan kematian terbanyak
    top5 = df_last.nlargest(5, 'Total Deaths')
    
    fig = px.bar(
        top5,
        x='Location',
        y='Total Deaths',
        color='Total Deaths',
        color_continuous_scale='Reds',
        title='🔝 5 Provinsi dengan Kematian Tertinggi',
        labels={'Total Deaths': 'Total Kematian', 'Location': 'Provinsi'}
    )
    
    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kematian', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
    
#barchart2
def bar_chart2(df):
    #mengambil data terakhir per provinsi (group by location ambil baris terakhir)
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    # Ambil 5 provinsi dengan kesembuhan terbanyak
    top5 = df_last.nlargest(5, 'Total Recovered')
    
    #buat bar chart
    fig = px.bar(
        top5,
        x='Location',
        y='Total Recovered',
        color='Total Recovered',
        color_continuous_scale='Greens',
        title='🔝 5 Provinsi dengan Kesembuhan Tertinggi',
        labels={'Total Recovered': 'Total Kesembuhan', 'Location': 'Provinsi'}
    )
    
    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kesembuhan', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
    
#map chart
def map_chart(df, year=None):
    #konversi kolom date
    df['Date'] = pd.to_datetime(df['Date'])
    
    #filter data berdasarkan tahun
    if year:
        df = df[df['Date'].dt.year == year]
    
    #agregasi data per lokasi
    df_agg = df.groupby('location', 'latitude', 'longitude', as_index=False)['New Cases'].sum()
    df_map = df_agg.dropna(subset=['latitude', 'longitude', 'New Cases'])
    
    #Validasi Data
    if df_map.empty:
        st.info("⚠️ Tidak ada data untuk ditampilkan di peta.")
        return
    
    fig = px.scatter_mapbox(
        df_map,
        lat='latitude',
        lon='longitude',
        size='New Cases',
        color='New Cases',
        hover_name='location',
        color_continuous_scale='OrRd',
        size_max=20,
        zoom=3,
        center={'lat': -2.5, 'lon': 118}, #fokus indonesia
        opacity=0.7,
        mapbox_style='carto-positron',
        title=f"Sebaran Kasus Baru COVID-19 di Indonesia ({year if year else 'Semua Tahun'})"
    )
    
    #gunakan style default mapbox
    fig.update_layout(
        mapbox_style="carto-positron",
        height=600,
        margin={"r":0,"t":50,"l":0,"b":0},
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    #dataframe
    data = {
        'Status': ['Meninggal', 'Sembuh'],
        'Jumlah': [total_death, total_recovery]
    }
    
    fig = px.pie(data, names='Status', values='Jumlah', title='Perbandingan Total Kematian VS Total Kesembuhan', hole=0.5, color_discrete_sequence=['#4de89f', '#ff6459'])
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    show_data()
