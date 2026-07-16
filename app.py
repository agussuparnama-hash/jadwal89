import streamlit as st
import pandas as pd
import io

# ... (fungsi load_data Anda sebelumnya) ...

# 1. Pastikan df sudah dimuat
df = load_data()

st.sidebar.header("Pilih Kode Guru Anda")
list_kode = sorted(df[df['Kode_Guru'].notna() & (df['Kode_Guru'] != '0')]['Kode_Guru'].unique().tolist())
pilih_kode = st.sidebar.selectbox("Pilih Kode Guru:", ["-- Pilih Kode --"] + list_kode)

# 2. DEFINISIKAN filtered_df SEBELUM DIGUNAKAN
# Inisialisasi awal agar variabel selalu ada
filtered_df = pd.DataFrame() 

if pilih_kode != "-- Pilih Kode --":
    # Filter data
    filtered_df = df[df['Kode_Guru'] == pilih_kode].copy()
    
    # Pengurutan
    hari_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    filtered_df['Hari'] = pd.Categorical(filtered_df['Hari'], categories=hari_order, ordered=True)
    filtered_df = filtered_df.sort_values(['Hari', 'Jam Ke'])

# 3. BARU CEK DENGAN AMAN
if not filtered_df.empty:
    st.subheader(f"Jadwal Mengajar Guru: {pilih_kode}")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Tambahkan fungsi download excel di sini
    # ...
else:
    st.info("Silakan pilih kode guru Anda untuk melihat jadwal.")
