import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Jadwal Mengajar Guru", layout="wide")
st.title("📅 Jadwal Mengajar Guru")

# Memuat data
@st.cache_data
def load_data():
    # Pastikan file Master_Jadwal_Sekolah.csv ada di folder yang sama
    df = pd.read_csv("Master_Jadwal_Sekolah.csv")
    # Membersihkan data: hapus spasi, isi yang kosong, dan ubah kode guru ke string
    df['Kode_Guru'] = df['Kode_Guru'].fillna(0).astype(int).astype(str)
    return df

df = load_data()

# Sidebar untuk Pemilihan Kode Guru
st.sidebar.header("Pilih Kode Guru Anda")

# Mengambil daftar kode guru yang unik dan mengurutkannya
list_kode = sorted(df[df['Kode_Guru'] != '0']['Kode_Guru'].unique().tolist())

pilih_kode = st.sidebar.selectbox("Pilih Kode Guru:", ["-- Pilih Kode --"] + list_kode)

# Logika Filter
if pilih_kode != "-- Pilih Kode --":
    # Filter data berdasarkan kode guru
    filtered_df = df[df['Kode_Guru'] == pilih_kode].copy()
    
    # Mengurutkan berdasarkan Hari dan Jam Ke
    hari_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    filtered_df['Hari'] = pd.Categorical(filtered_df['Hari'], categories=hari_order, ordered=True)
    filtered_df = filtered_df.sort_values(['Hari', 'Jam Ke'])
    
    # Menampilkan hasil
    st.subheader(f"Jadwal Mengajar untuk Guru Kode: {pilih_kode}")
    
    # Menampilkan tabel yang sudah rapi
    st.dataframe(filtered_df[['Hari', 'Jam Ke', 'Waktu', 'Tingkat', 'Kelas', 'Mapel']], 
                 use_container_width=True, 
                 hide_index=True)
else:
    st.info("Silakan pilih kode guru Anda pada menu di sebelah kiri untuk melihat jadwal.")
