import streamlit as st
import pandas as pd
import io

@st.cache_data
def load_data():
    try:
        # Memuat CSV
        df = pd.read_csv("Master_Jadwal_Sekolah.csv")
        df.columns = df.columns.str.strip() # Menghapus spasi di header
        
        # Rename agar sesuai dengan logika kode program
        df = df.rename(columns={'Kode Guru': 'Kode_Guru'})
        
        # Membersihkan data
        df['Kode_Guru'] = df['Kode_Guru'].fillna('0').astype(str)
        df['Kode_Guru'] = df['Kode_Guru'].str.replace('.0', '', regex=False).str.replace('-', '0')
        
        # Hapus duplikat
        df = df.drop_duplicates()
        return df
    except Exception as e:
        return None, str(e)

df, error_msg = load_data()

if error_msg:
    st.error(f"Gagal memuat file: {error_msg}")
    st.stop()

st.title("📅 Jadwal Mengajar Guru")

# Sidebar: Filter Kode Guru
list_kode = sorted(df[~df['Kode_Guru'].isin(['0', 'nan']) ]['Kode_Guru'].unique().tolist())
pilih_kode = st.sidebar.selectbox("Pilih Kode Guru:", ["-- Pilih Kode --"] + list_kode)

if pilih_kode != "-- Pilih Kode --":
    filtered_df = df[df['Kode_Guru'] == pilih_kode].copy()
    
    # Urutkan berdasarkan hari
    hari_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    filtered_df['Hari'] = pd.Categorical(filtered_df['Hari'], categories=hari_order, ordered=True)
    filtered_df = filtered_df.sort_values(['Hari', 'Jam Ke'])

    st.subheader(f"Jadwal Guru Kode: {pilih_kode}")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download Excel Berwarna
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
else:
    st.info("Silakan pilih kode guru di menu samping untuk melihat jadwal.")
