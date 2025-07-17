import pandas as pd
import plotly.express as px
import streamlit as st

def plot_overview(df, itens, col_data, col_placa, col_status):
    st.markdown("### 📈 Visão Geral de Não Conformidades")

    # Garante que estamos lidando com um DataFrame e colunas válidas
    df_nc = df.copy()
    df_nc["qtd_nc"] = df_nc[itens].apply(
        lambda row: sum(str(x).strip().lower() != "ok" and str(x).strip() != "" for x in row),
        axis=1
    )

    df_grouped = df_nc.groupby(col_data)["qtd_nc"].sum().reset_index()
    df_grouped[col_data] = pd.to_datetime(df_grouped[col_data])

    fig = px.line(df_grouped, x=col_data, y="qtd_nc", title="Evolução de Não Conformidades")
    fig.update_traces(mode="lines+markers")
    st.plotly_chart(fig, use_container_width=True)
