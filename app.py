import streamlit as st
import pandas as pd
import io

# Konfigurasi Halaman
st.set_page_config(page_title="Jadwal Guru", layout="wide")

@st.cache_data
def load_data():
    try:
        # Memuat CSV
        df = pd.read_csv("Master_Jadwal_Sekolah.csv")
        df.columns = df.columns.str.strip() # Menghapus spasi di header
        
        # Rename kolom agar konsisten di kode
        df = df.rename(columns={'Kode Guru': 'Kode_Guru'})
        
        # Membersihkan data
        # Mengubah '-' atau kosong menjadi string '0'
        df['Kode_Guru'] = df['Kode_Guru'].replace(['-', 'nan', ''], '0').fillna('0').astype(str)
        
        # Hapus baris duplikat agar jadwal tidak ganda
        df = df.drop_duplicates()
        
        return df, None
    except Exception as e:
        return None, str(e)

# Muat data
result = load_data()
if isinstance(result, tuple):
    df, error_msg = result
else:
    df, error_msg = None, "Terjadi kesalahan pada struktur data."

if error_msg:
    st.error(f"Gagal memuat file: {error_msg}")
    st.stop()

st.title("📅 Sistem Jadwal Mengajar Guru")

# Sidebar Filter
# Filter kode unik, hapus yang bernilai '0'
list_kode = sorted([str(k) for k in df['Kode_Guru'].unique() if str(k) != '0'])
pilih_kode = st.sidebar.selectbox("Pilih Kode Guru Anda:", ["-- Pilih Kode --"] + list_kode)

if pilih_kode != "-- Pilih Kode --":
    # Filter data
    filtered_df = df[df['Kode_Guru'] == pilih_kode].copy()
    
    # Urutkan berdasarkan hari
    hari_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    filtered_df['Hari'] = pd.Categorical(filtered_df['Hari'], categories=hari_order, ordered=True)
    filtered_df = filtered_df.sort_values(['Hari', 'Jam Ke'])

    st.subheader(f"Jadwal Mengajar untuk Guru Kode: {pilih_kode}")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    
    # Fungsi Download Excel Berwarna
  # Fungsi Download Excel Berwarna dengan pembersihan ganda
    def to_excel_colored(df):
        # 1. Bersihkan duplikat tepat sebelum dibuat file excel
        df_clean = df.drop_duplicates()
        
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df_clean.to_excel(writer, index=False, sheet_name='Jadwal')
        
        workbook = writer.book
        worksheet = writer.sheets['Jadwal']
        
        # ... (kode warna Anda tetap sama) ...
        colors = {'Senin': '#FFC0CB', 'Selasa': '#ADD8E6', 'Rabu': '#90EE90', 
                  'Kamis': '#FFFFE0', 'Jumat': '#D8BFD8', 'Sabtu': '#FFD700'}
        
        for idx, row in df_clean.iterrows():
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
else:
    st.info("Silakan pilih kode guru di menu samping untuk melihat jadwal Anda.")
