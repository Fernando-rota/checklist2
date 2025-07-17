from data_loader import load_checklist_data


def render_sidebar():
    st.sidebar.header("🔍 Filtros")

    uploaded_file = st.sidebar.file_uploader("Selecione o arquivo Excel do checklist", type=["xlsx"])
    
    if not uploaded_file:
        st.stop()

    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # Colunas inferidas
    col_data = 'Data'
    col_motorista = 'Motorista'
    col_placa = 'Placa'
    col_status = 'Status'
    col_fotos = [col for col in df.columns if 'http' in str(df[col].astype(str).values)]

    # Itens de verificação
    itens = [col for col in df.columns if col not in [col_data, col_motorista, col_placa, col_status] + col_fotos]

    # Filtros
    motoristas = st.sidebar.multiselect("Filtrar por motorista", df[col_motorista].dropna().unique())
    placas = st.sidebar.multiselect("Filtrar por placa", df[col_placa].dropna().unique())
    status = st
