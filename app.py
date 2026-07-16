import streamlit as st
import pandas as pd

# Judul Aplikasi
st.title("Sistem Informasi Jadwal Mengajar")

# Memuat data
@st.cache_data
def load_data():
    # Pastikan file Master_Jadwal_Sekolah.csv berada di folder yang sama
    df = pd.read_csv("Master_Jadwal_Sekolah.csv")
    return df

df = load_data()

# Input Pencarian
st.sidebar.header("Pencarian Jadwal")
mapel_input = st.sidebar.text_input("Masukkan Mata Pelajaran:")
kode_guru_input = st.sidebar.text_input("Masukkan Kode Guru:")

if mapel_input or kode_guru_input:
    # Filter data
    filtered_df = df.copy()
    
    if mapel_input:
        filtered_df = filtered_df[filtered_df['Mapel'].str.contains(mapel_input, case=False, na=False)]
    
    if kode_guru_input:
        filtered_df = filtered_df[filtered_df['Kode_Guru'].astype(str) == kode_guru_input]

    # Mengurutkan berdasarkan Hari dan Jam Ke
    hari_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    filtered_df['Hari'] = pd.Categorical(filtered_df['Hari'], categories=hari_order, ordered=True)
    filtered_df = filtered_df.sort_values(['Hari', 'Jam Ke'])

    if not filtered_df.empty:
        st.write(f"Jadwal untuk {mapel_input} (Kode: {kode_guru_input}):")
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.warning("Jadwal tidak ditemukan. Periksa kembali input Anda.")
else:
    st.info("Silakan masukkan Mata Pelajaran atau Kode Guru di sidebar untuk melihat jadwal.")
