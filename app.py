import streamlit as st
import pandas as pd
import io

# ... (Kod load_data anda sebelumnya) ...

# Fungsi untuk menukar DF kepada Excel dengan warna
def to_excel_colored(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Jadual')
    
    workbook = writer.book
    worksheet = writer.sheets['Jadual']
    
    # Definisi warna untuk setiap hari
    colors = {
        'Senin': '#FFC0CB', 'Selasa': '#ADD8E6', 'Rabu': '#90EE90',
        'Kamis': '#FFFFE0', 'Jumat': '#D8BFD8', 'Sabtu': '#FFD700'
    }
    
    # Format sel
    for idx, row in df.iterrows():
        hari = row['Hari']
        color = colors.get(hari, '#FFFFFF')
        cell_format = workbook.add_format({'bg_color': color, 'border': 1})
        
        for col_num in range(len(df.columns)):
            worksheet.write(idx + 1, col_num, row[col_num], cell_format)
            
    writer.close()
    return output.getvalue()

# Di dalam bahagian paparan hasil:
if not filtered_df.empty:
    st.subheader(f"Jadual untuk Guru: {pilih_kode}")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Butang Download Excel
    excel_data = to_excel_colored(filtered_df)
    st.download_button(
        label="📥 Download Jadual (Excel Berwarna)",
        data=excel_data,
        file_name=f"Jadual_Guru_{pilih_kode}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.info("Silakan pilih kode guru Anda pada menu di sebelah kiri untuk melihat jadwal.")
