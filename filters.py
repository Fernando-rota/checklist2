import streamlit as st
import pandas as pd

def apply_filters(df, col_data, col_motorista, col_placa, col_status):
    st.sidebar.markdown("### 🎯 Filtros")
    data_ini = st.sidebar.date_input("Data inicial", value=df[col_data].min().date())
    data_fim = st.sidebar.date_input("Data final", value=df[col_data].max().date())
    motoristas = sorted(df[col_motorista].dropna().unique())
    placas = sorted(df[col_placa].dropna().unique())
    status_nc = sorted(df[col_status].dropna().unique())

    sel_motorista = st.sidebar.multiselect("Motorista", motoristas, default=motoristas)
    sel_placa = st.sidebar.multiselect("Placa do Caminhão", placas, default=placas)
    sel_status = st.sidebar.multiselect("Status NC", status_nc, default=status_nc)

    df_filtrado = df[
        (df[col_data] >= pd.to_datetime(data_ini)) &
        (df[col_data] <= pd.to_datetime(data_fim)) &
        (df[col_motorista].isin(sel_motorista)) &
        (df[col_placa].isin(sel_placa)) &
        (df[col_status].isin(sel_status))
    ]

    return {
        "df_filtrado": df_filtrado,
        "data_ini": data_ini,
        "data_fim": data_fim,
        "sel_motorista": sel_motorista,
        "sel_placa": sel_placa,
        "sel_status": sel_status,
    }
