import pandas as pd

def load_checklist_data(file) -> pd.DataFrame:
    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

def preprocess_checklist(df: pd.DataFrame):
    col_data = next(c for c in df.columns if "data" in c.lower())
    col_motorista = next(c for c in df.columns if "motorista" in c.lower())
    col_placa = next(c for c in df.columns if "placa" in c.lower() and "caminh" in c.lower())
    col_status = next(c for c in df.columns if "status" in c.lower() and "nc" in c.lower())
    col_fotos = next(c for c in df.columns if "foto" in c.lower())

    df[col_data] = pd.to_datetime(df[col_data], errors='coerce')
    df = df.dropna(subset=[col_data])

    idx_motorista = df.columns.get_loc(col_motorista)
    idx_status = df.columns.get_loc(col_status)
    itens = df.columns[(idx_motorista + 1):idx_status]

    return df, col_data, col_motorista, col_placa, col_status, col_fotos, itens
