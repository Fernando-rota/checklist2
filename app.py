# 📦 checklist_dashboard/app.py

import streamlit as st
from components.sidebar import render_sidebar
from components.tabs import render_tabs

st.set_page_config(
    page_title="✅ Painel de Não Conformidades - Checklist Veicular",
    layout="wide",
    page_icon="✅"
)

# Barra lateral com filtros
filters = render_sidebar()

# Renderiza as abas principais
render_tabs(filters)