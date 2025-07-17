import streamlit as st
from data import load_checklist_data, preprocess_checklist
from filters import apply_filters
from plots import plot_overview, plot_critical_items
from utils import extract_drive_links
from export import get_excel_download_link

st.set_page_config(page_title="Painel de Não Conformidades", layout="wide")

st.title("✅ Painel de Não Conformidades - Checklist Veicular")

uploaded_file = st.sidebar.file_uploader("📤 Envie o arquivo de checklist (.xlsx ou .xls)", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = load_checklist_data(uploaded_file)
        df, col_data, col_motorista, col_placa, col_status, col_fotos, itens = preprocess_checklist(df)
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        st.stop()

    filters = apply_filters(df, col_data, col_motorista, col_placa, col_status)
    df_filtered = filters["df_filtrado"]

    tabs = st.tabs(["📊 Visão Geral", "📌 Itens Críticos", "📋 Checklist Completo", "📁 Checklist Filtrado", "📸 Fotos de NC", "⬇️ Exportar Dados"])

    with tabs[0]:
        plot_overview(df_filtered, itens, col_data, col_placa, col_status)

    with tabs[1]:
        plot_critical_items(df_filtered, itens)

    with tabs[2]:
        st.dataframe(df)

    with tabs[3]:
        st.dataframe(df_filtered)

    with tabs[4]:
        fotos_df = df_filtered.dropna(subset=[col_fotos])
        placas_disp = sorted(fotos_df[col_placa].unique())
        sel_placa = st.selectbox("Filtrar por Placa", ["Todas"] + placas_disp)
        if sel_placa != "Todas":
            fotos_df = fotos_df[fotos_df[col_placa] == sel_placa]
        if fotos_df.empty:
            st.info("Nenhuma foto encontrada.")
        else:
            for _, row in fotos_df.iterrows():
                nc_itens = [i for i in itens if str(row[i]).strip().lower() != "ok"]
                links = extract_drive_links(row[col_fotos])
                st.markdown(f"**Data:** {row[col_data].date()}  \n**Motorista:** {row[col_motorista]}  \n**Placa:** {row[col_placa]}  \n**Status:** {row[col_status]}  \n**Itens Não Conformes:** {', '.join(nc_itens)}")
                for i, link in enumerate(links, 1):
                    st.markdown(f"[🔗 Foto {i}]({link})")
                st.markdown("---")

    with tabs[5]:
        st.download_button(
            label="📥 Baixar Checklist Filtrado (Excel)",
            data=get_excel_download_link(df_filtered),
            file_name="checklist_filtrado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Envie o arquivo de checklist no menu lateral para começar.")
