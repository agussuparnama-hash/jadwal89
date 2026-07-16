import streamlit as st
import pandas as pd
import io

# 1. DEFINISIKAN FUNGSI TERLEBIH DAHULU
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Master_Jadwal_Sekolah.csv")
        # Membersihkan data dari nilai kosong
        df['Kode_Guru'] = df['Kode_Guru'].fillna('0').astype(str)
        return df
    except FileNotFoundError:
        st.error("File 'Master_Jadwal_Sekolah.csv' tidak ditemukan! Pastikan file sudah di-upload ke GitHub.")
        return pd.DataFrame() # Return empty df jika error

# 2. PANGGIL FUNGSI SETELAH DEFINISI
df = load_data()

# 3. PASTIKAN df TIDAK KOSONG
if df.empty:
    st.stop() # Berhenti jika tidak ada data

st.title("📅 Jadwal Mengajar Guru")

# Sidebar
list_kode = sorted(df[df['Kode_Guru'] != '0']['Kode_Guru'].unique().tolist())
pilih_kode = st.sidebar.selectbox("Pilih Kode Guru:", ["-- Pilih Kode --"] + list_kode)

# Inisialisasi variabel untuk menghindari NameError
filtered_df = pd.DataFrame()

if pilih_kode != "-- Pilih Kode --":
    filtered_df = df[df['Kode_Guru'] == pilih_kode].copy()
    
    # Pengurutan
    hari_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    filtered_df['Hari'] = pd.Categorical(filtered_df['Hari'], categories=hari_order, ordered=True)
    filtered_df = filtered_df.sort_values(['Hari', 'Jam Ke'])

# 4. TAMPILKAN HASIL
if not filtered_df.empty:
    st.subheader(f"Jadwal Guru: {pilih_kode}")
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.info("Silakan pilih kode guru Anda di menu samping.")
