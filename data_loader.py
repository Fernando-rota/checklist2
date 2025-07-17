import pandas as pd

def load_data(uploaded_file):
    if uploaded_file:
        return pd.read_excel(uploaded_file)
    return None
