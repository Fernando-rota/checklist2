import streamlit as st
from utils.data_loader import load_data

def render_sidebar():
    st.sidebar.title("📥 Dados do Checklist")
    uploaded_file = st.sidebar.file_uploader("Envie o arquivo de checklist (.xlsx ou .xls)", type=["xlsx", "xls"])
    df = load_data(uploaded_file)

    filters = {}
    if df is not None:
        df.columns = df.columns.str.strip()
        col_data = [col for col in df.columns if "data" in col.lower()][0]
        col_motorista = [col for col in df.columns if "motorista" in col.lower()][0]
        col_placa = [col for col in df.columns if "placa" in col.lower()][0]
        col_status = [col for col in df.columns if "status" in col.lower()][0]

        df[col_data] = pd.to_datetime(df[col_data], errors='coerce')
        df.dropna(subset=[col_data], inplace=True)

        st.sidebar.markdown("### 🎯 Filtros")
        filters["data_ini"] = st.sidebar.date_input("Data inicial", df[col_data].min().date())
        filters["data_fim"] = st.sidebar.date_input("Data final", df[col_data].max().date())
        filters["motoristas"] = st.sidebar.multiselect("Motorista", sorted(df[col_motorista].dropna().unique()), default=list(df[col_motorista].dropna().unique()))
        filters["placas"] = st.sidebar.multiselect("Placa", sorted(df[col_placa].dropna().unique()), default=list(df[col_placa].dropna().unique()))
        filters["status"] = st.sidebar.multiselect("Status NC", sorted(df[col_status].dropna().unique()), default=list(df[col_status].dropna().unique()))

        filters["df"] = df
        filters["colunas"] = {
            "data": col_data,
            "motorista": col_motorista,
            "placa": col_placa,
            "status": col_status
        }

    return filters
