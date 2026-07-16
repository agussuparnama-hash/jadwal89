import streamlit as st
import pandas as pd
import io

# ... (fungsi load_data Anda sebelumnya) ...

# Fungsi untuk membuat Excel Berwarna
def to_excel_colored(df):
    output = io.BytesIO()
    # Gunakan engine xlsxwriter untuk memberi warna
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Jadwal')
    
    workbook = writer.book
    worksheet = writer.sheets['Jadwal']
    
    # Definisi warna per hari (Hex Color)
    colors = {
        'Senin': '#FFC0CB', 'Selasa': '#ADD8E6', 'Rabu': '#90EE90',
        'Kamis': '#FFFFE0', 'Jumat': '#D8BFD8', 'Sabtu': '#FFD700'
    }
    
    # Terapkan format warna ke baris
    for idx, row in df.iterrows():
        hari = row['Hari']
        color = colors.get(hari, '#FFFFFF')
        cell_format = workbook.add_format({'bg_color': color, 'border': 1})
        
        # Tulis ulang setiap sel dengan format warna
        for col_num, value in enumerate(row):
            worksheet.write(idx + 1, col_num, value, cell_format)
            
    writer.close()
    return output.getvalue()

# ... (setelah filter filtered_df berhasil) ...

if not filtered_df.empty:
    st.subheader(f"Jadwal Guru: {pilih_kode}")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Proses Download Excel
    excel_data = to_excel_colored(filtered_df)
    
    st.download_button(
        label="📥 Download Jadwal (Excel Berwarna)",
        data=excel_data,
        file_name=f"Jadwal_Guru_{pilih_kode}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
