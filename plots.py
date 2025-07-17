# checklist2/plots.py

import streamlit as st
import plotly.express as px
import pandas as pd

def plot_overview(df_filtrado, col_placa, col_data, col_status, itens):
    st.markdown("### 📊 Gráficos de Não Conformidades")

    df_nc = df_filtrado.copy()
    df_nc["qtd_nc"] = df_nc[itens].apply(lambda row: sum(str(x).strip().lower() != "ok" for x in row), axis=1)
    nc_por_placa = df_nc.groupby(col_placa)["qtd_nc"].sum().reset_index().sort_values("qtd_nc", ascending=False)

    fig1 = px.bar(nc_por_placa, x="qtd_nc", y=col_placa, orientation="h", title="Total de Não Conformidades por Veículo")
    st.plotly_chart(fig1, use_container_width=True)

    nc_por_data = df_nc.groupby(col_data)["qtd_nc"].sum().reset_index()
    fig2 = px.line(nc_por_data, x=col_data, y="qtd_nc", markers=True, title="Tendência de Não Conformidades ao longo do tempo")
    st.plotly_chart(fig2, use_container_width=True)

    status_count = df_filtrado[col_status].value_counts().reset_index()
    status_count.columns = ["Status", "Quantidade"]
    fig3 = px.pie(status_count, names="Status", values="Quantidade", title="Distribuição por Status")
    st.plotly_chart(fig3, use_container_width=True)

    df_nc["dia_semana"] = df_nc[col_data].dt.day_name()
    heatmap_data = df_nc.groupby(["dia_semana", col_placa])["qtd_nc"].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index="dia_semana", columns=col_placa, values="qtd_nc").fillna(0)
    fig4 = px.imshow(heatmap_pivot, text_auto=True, aspect="auto", title="Frequência de NCs por Dia e Veículo")
    st.plotly_chart(fig4, use_container_width=True)

def plot_critical_items(df_filtrado, itens):
    st.markdown("### 📌 Itens com Mais Não Conformidades")
    item_counts = {item: (df_filtrado[item].astype(str).str.lower() != "ok").sum() for item in itens}
    item_df = pd.DataFrame(list(item_counts.items()), columns=["Item", "Não Conformidades"])
    item_df = item_df.sort_values("Não Conformidades", ascending=False)

    fig = px.bar(item_df, x="Não Conformidades", y="Item", orientation="h", title="Frequência de NC por Item")
    st.plotly_chart(fig, use_container_width=True)

    fig_treemap = px.treemap(item_df, path=["Item"], values="Não Conformidades", title="Treemap de Itens com NC")
    st.plotly_chart(fig_treemap, use_container_width=True)
