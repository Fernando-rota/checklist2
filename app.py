# 📦 checklist_dashboard/app.py

import streamlit as st
from utils.sidebar import render_sidebar
from utils.tabs import render_tabs

st.set_page_config(
    page_title="📋 Checklist Veicular",
    layout="wide",
    page_icon="🚚"
)

# Renderiza a barra lateral e retorna os filtros aplicados
filters, df, itens, col_data, col_motorista, col_placa, col_status, col_fotos = render_sidebar()

# Renderiza as abas principais com base nos filtros e dados
render_tabs(filters, df, itens, col_data, col_motorista, col_placa, col_status, col_fotos)
