
import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('Master_Jadwal_Sekolah.csv')

df = load_data()

st.title("Sistem Informasi Jadwal Guru")
st.write("Masukkan Kode Guru Anda untuk melihat jadwal mengajar.")

# Input Kode Guru
kode_guru = st.text_input("Masukkan Kode Guru (Contoh: 14):")

if kode_guru:
    # Filter data
    hasil = df[df['Kode_Guru'].astype(str) == str(kode_guru)]
    
    if not hasil.empty:
        st.success(f"Jadwal untuk Guru dengan Kode: {kode_guru}")
        st.table(hasil[['Hari', 'Jam Ke', 'Waktu', 'Tingkat', 'Kelas', 'Mapel']])
    else:
        st.error("Kode tidak ditemukan atau tidak ada jadwal.")
