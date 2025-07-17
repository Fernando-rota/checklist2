import re
import pandas as pd
import plotly.express as px
import streamlit as st

def generate_charts(df, itens, col_data, col_placa, col_status):
    df["qtd_nc"] = df[itens].apply(lambda row: sum(str(x).strip().lower() != "ok" for x in row), axis=1)
    
    nc_por_placa = df.groupby(col_placa)["qtd_nc"].sum().reset_index().sort_values("qtd_nc", ascending=False)
    st.plotly_chart(px.bar(nc_por_placa, x="qtd_nc", y=col_placa, orientation="h", title="Total de NC por Veículo"), use_container_width=True)

    nc_por_data = df.groupby(col_data)["qtd_nc"].sum().reset_index()
    st.plotly_chart(px.line(nc_por_data, x=col_data, y="qtd_nc", markers=True, title="Tendência ao Longo do Tempo"), use_container_width=True)

    status_count = df[col_status].value_counts().reset_index()
    status_count.columns = ["Status", "Quantidade"]
    st.plotly_chart(px.pie(status_count, names="Status", values="Quantidade", title="Distribuição por Status"), use_container_width=True)

    df["dia_semana"] = df[col_data].dt.day_name()
    heatmap_data = df.groupby(["dia_semana", col_placa])["qtd_nc"].sum().reset_index()
    pivot = heatmap_data.pivot(index="dia_semana", columns=col_placa, values="qtd_nc").fillna(0)
    st.plotly_chart(px.imshow(pivot, text_auto=True, aspect="auto", title="Heatmap por Dia e Veículo"), use_container_width=True)

def show_item_criticos(df, itens):
    item_counts = {item: (df[item].astype(str).str.lower() != "ok").sum() for item in itens}
    item_df = pd.Series(item_counts).sort_values(ascending=False).reset_index()
    item_df.columns = ["Item", "Não Conformidades"]
    st.plotly_chart(px.bar(item_df, x="Não Conformidades", y="Item", orientation="h", title="NC por Item"), use_container_width=True)
    st.plotly_chart(px.treemap(item_df, path=["Item"], values="Não Conformidades", title="Treemap de NC por Item"), use_container_width=True)

def show_photos(df, itens, col_data, col_motorista, col_placa, col_fotos, col_status):
    fotos_df = df[[col_data, col_motorista, col_placa, col_fotos, col_status] + list(itens)].dropna(subset=[col_fotos])
    placas_disp = sorted(fotos_df[col_placa].unique())
    sel_foto = st.selectbox("Filtrar por Placa", ["Todas"] + placas_disp)

    if sel_foto != "Todas":
        fotos_df = fotos_df[fotos_df[col_placa] == sel_foto]

    if fotos_df.empty:
        st.info("Nenhuma foto encontrada.")
    else:
        for _, row in fotos_df.iterrows():
            nc_itens = [col for col in itens if str(row[col]).strip().lower() != "ok"]
            links = re.findall(r"https://drive.google.com/[^\s,]+", str(row[col_fotos]))
            st.markdown(f"""
**📅 {row[col_data].date()}**  
👨‍✈️ **Motorista:** {row[col_motorista]}  
🚚 **Placa:** {row[col_placa]}  
📍 **Status:** {row[col_status]}  
🔧 **Itens Não Conformes:** {', '.join(nc_itens)}
""")
            for i, link in enumerate(links, 1):
                st.markdown(f"[🔗 Foto {i}]({link})")
            st.markdown("---")
