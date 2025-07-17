import pandas as pd

def load_checklist_data(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            return df
        except Exception as e:
            raise ValueError(f"Erro ao ler o arquivo: {e}")
    return pd.DataFrame()

