import streamlit as st
from utils.filters import apply_filters
from utils.helpers import generate_charts, show_photos, show_dataframes

def render_tabs(filters):
    if not filters:
        st.info("Envie o arquivo de checklist no menu lateral para começar.")
        return

    df_filtered, itens, col_data, col_motorista, col_placa, col_status, col_fotos = apply_filters(filters)
    
    aba1, aba2, aba3, aba4, aba5 = st.tabs([
        "📊 Visão Geral", 
        "📌 Itens Críticos", 
        "📋 Checklist Completo", 
        "📁 Checklist Filtrado", 
        "📸 Fotos de NC"
    ])

    with aba1:
        generate_charts(df_filtered, itens, col_data, col_placa, col_status)

    with aba2:
        from utils.helpers import show_item_criticos
        show_item_criticos(df_filtered, itens)

    with aba3:
        st.dataframe(filters['df'])

    with aba4:
        st.dataframe(df_filtered)

    with aba5:
        show_photos(filters['df'], itens, col_data, col_motorista, col_placa, col_fotos, col_status)
