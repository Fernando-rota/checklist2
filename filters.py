import pandas as pd

def apply_filters(filters):
    df = filters["df"].copy()
    col_data = filters["colunas"]["data"]
    col_motorista = filters["colunas"]["motorista"]
    col_placa = filters["colunas"]["placa"]
    col_status = filters["colunas"]["status"]
    col_fotos = [col for col in df.columns if "foto" in col.lower()][0]

    idx_motorista = df.columns.get_loc(col_motorista)
    idx_status = df.columns.get_loc(col_status)
    itens = df.columns[(idx_motorista + 1):idx_status]

    df_filtered = df[
        (df[col_data] >= pd.to_datetime(filters["data_ini"])) &
        (df[col_data] <= pd.to_datetime(filters["data_fim"])) &
        (df[col_motorista].isin(filters["motoristas"])) &
        (df[col_placa].isin(filters["placas"])) &
        (df[col_status].isin(filters["status"]))
    ]

    return df_filtered, itens, col_data, col_motorista, col_placa, col_status, col_fotos
