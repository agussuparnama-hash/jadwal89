import streamlit as st
import pandas as pd
import io

# Konfigurasi Halaman
st.set_page_config(page_title="Jadwal Guru", layout="wide")

@st.cache_data
def load_data():
    try:
        # Memuat file CSV
        df = pd.read_csv("Master_Jadwal_Sekolah.csv")
        df.columns = df.columns.str.strip() 
        
        # Penanganan nama kolom
        if 'Kode Guru' in df.columns:
            df = df.rename(columns={'Kode Guru': 'Kode_Guru'})
            
        # --- PEMBENTENGAN DATA (Pembersihan Otomatis) ---
        # 1. Hapus baris yang semua selnya kosong
        df = df.dropna(how='all')
        # 2. Hapus baris yang tidak memiliki informasi Hari
        df = df.dropna(subset=['Hari'])
        # 3. Hapus duplikat persis di tingkat sumber
        df = df.drop_duplicates()
        
        # 4. Bersihkan spasi di semua teks (agar "26" dan "26 " dianggap sama)
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()
            
        return df, None
    except Exception as e:
        return None, str(e)

# Muat data
df, error_msg = load_data()

if error_msg:
    st.error(f"Gagal memuat: {error_msg}")
    st.stop()

st.title("📅 Jadwal Mengajar Guru")

# Sidebar Filter: Hanya tampilkan kode yang valid
list_kode = sorted([str(k) for k in df['Kode_Guru'].unique() if str(k) not in ['0', '-', 'nan', '']])
pilih_kode = st.sidebar.selectbox("Pilih Kode Guru:", ["-- Pilih Kode --"] + list_kode)

if pilih_kode != "-- Pilih Kode --":
    # Filter data
    filtered_df = df[df['Kode_Guru'] == pilih_kode].copy()
    
    # Sorting berdasarkan Hari dan Jam
    hari_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    filtered_df['Hari'] = pd.Categorical(filtered_df['Hari'], categories=hari_order, ordered=True)
    filtered_df = filtered_df.sort_values(['Hari', 'Jam Ke'])

    st.subheader(f"Jadwal Guru: {pilih_kode}")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    
    # Fungsi Download Excel (Dilapisi pembersihan duplikat lagi di sini)
    def to_excel_colored(df_input):
        # Pembersihan tambahan sebelum file dibuat
        df_clean = df_input.drop_duplicates()
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_clean.to_excel(writer, index=False, sheet_name='Jadwal')
            workbook = writer.book
            worksheet = writer.sheets['Jadwal']
            
            colors = {'Senin': '#FFC0CB', 'Selasa': '#ADD8E6', 'Rabu': '#90EE90', 
                      'Kamis': '#FFFFE0', 'Jumat': '#D8BFD8', 'Sabtu': '#FFD700'}
            
            for idx, row in df_clean.iterrows():
                color = colors.get(row['Hari'], '#FFFFFF')
                fmt = workbook.add_format({'bg_color': color, 'border': 1})
                for col_num, value in enumerate(row):
                    worksheet.write(idx + 1, col_num, value, fmt)
        return output.getvalue()

    st.download_button(
        label="📥 Download Excel Berwarna",
        data=to_excel_colored(filtered_df),
        file_name=f"Jadwal_Guru_{pilih_kode}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Silakan pilih kode guru di menu samping.")
