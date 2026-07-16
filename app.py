import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('Master_Jadwal_Sekolah.csv')

df = load_data()

st.title("Sistem Informasi Jadwal Guru")
st.write("Masukkan Kode Guru Anda untuk melihat jadwal mengajar.")

# Menampilkan daftar kode yang tersedia untuk pengecekan
st.write("Kode guru yang tersedia dalam sistem:")
st.write(df['Kode_Guru'].unique())

# Input Kode Guru
kode_guru = st.text_input("Masukkan Kode Guru (Contoh: 14):")

if kode_guru:
    # Perbaikan: Membersihkan data dan melakukan pencarian dengan aman
    df['Kode_Guru_Str'] = df['Kode_Guru'].astype(str).str.strip().replace('\.0$', '', regex=True)
    input_kode = str(kode_guru).strip()
    
    # Filter data
    hasil = df[df['Kode_Guru_Str'] == input_kode]
    
    if not hasil.empty:
        st.success(f"Jadwal untuk Guru dengan Kode: {kode_guru}")
        st.table(hasil[['Hari', 'Jam Ke', 'Waktu', 'Tingkat', 'Kelas', 'Mapel']])
    else:
        st.error("Kode tidak ditemukan. Pastikan kode sesuai dengan daftar di atas.")
