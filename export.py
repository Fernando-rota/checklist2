import pandas as pd
from io import BytesIO

def get_excel_download_link(df):
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    return buffer.getvalue()
