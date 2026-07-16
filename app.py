import streamlit as st
import pandas as pd
import io

# 1. Pastikan fungsi load_data didefinisikan dengan benar
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Master_Jadwal_Sekolah.csv")
        
        # 1. Bersihkan spasi berlebih pada semua teks
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        # 2. Hapus baris yang Mapel atau Kode_Guru-nya kosong (nan)
        df = df.dropna(subset=['Mapel', 'Kode_Guru'])
        
        # 3. Konversi Kode_Guru ke string dan hapus kode '0' atau 'nan'
        df['Kode_Guru'] = df['Kode_Guru'].astype(str).str.replace('.0', '', regex=False)
        df = df[df['Kode_Guru'] != 'nan']
        df = df[df['Kode_Guru'] != '0']
        
        # 4. HAPUS BARIS GANDA (Kunci utama masalah Anda)
        df = df.drop_duplicates()
        
        return df
    except Exception as e:
        st.error(f"Gagal memuat file: {e}")
        return pd.DataFrame()

# 2. Muat data
df = load_data()

# 3. Inisialisasi awal filtered_df agar tidak terjadi NameError
filtered_df = pd.DataFrame() 

if not df.empty:
    st.title("📅 Jadwal Mengajar Guru")
    
    # Ambil list kode guru yang unik, hapus yang bernilai '0' atau kosong
    list_kode = sorted(df[df['Kode_Guru'] != '0']['Kode_Guru'].unique().tolist())
    pilih_kode = st.sidebar.selectbox("Pilih Kode Guru:", ["-- Pilih Kode --"] + list_kode)

    if pilih_kode != "-- Pilih Kode --":
        # Filter berdasarkan kode yang dipilih
        filtered_df = df[df['Kode_Guru'] == pilih_kode].copy()
        
        # Urutkan berdasarkan hari
        hari_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
        filtered_df['Hari'] = pd.Categorical(filtered_df['Hari'], categories=hari_order, ordered=True)
        filtered_df = filtered_df.sort_values(['Hari', 'Jam Ke'])

# 4. Pengecekan aman setelah proses filter
if not filtered_df.empty:
    st.subheader(f"Jadwal Guru: {pilih_kode}")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Fungsi Download Excel Berwarna
    def to_excel_colored(df):
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Jadwal')
        
        workbook = writer.book
        worksheet = writer.sheets['Jadwal']
        colors = {'Senin': '#FFC0CB', 'Selasa': '#ADD8E6', 'Rabu': '#90EE90', 
                  'Kamis': '#FFFFE0', 'Jumat': '#D8BFD8', 'Sabtu': '#FFD700'}
        
        for idx, row in df.iterrows():
            color = colors.get(row['Hari'], '#FFFFFF')
            fmt = workbook.add_format({'bg_color': color, 'border': 1})
            for col_num, value in enumerate(row):
                worksheet.write(idx + 1, col_num, value, fmt)
        writer.close()
        return output.getvalue()

    st.download_button(
        label="📥 Download Excel Berwarna",
        data=to_excel_colored(filtered_df),
        file_name=f"Jadwal_Guru_{pilih_kode}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
elif "pilih_kode" in locals() and pilih_kode != "-- Pilih Kode --":
    st.warning("Data untuk kode guru tersebut tidak ditemukan.")
else:
    st.info("Silakan pilih kode guru di menu samping untuk melihat jadwal.")
