import re
import pandas as pd

def extract_drive_links(text):
    if not text or pd.isna(text):
        return []
    return re.findall(r"https://drive.google.com/[^\s,]+", str(text))
