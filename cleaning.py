import pandas as pd

def remove_duplicates(df):
    return df.drop_duplicates().reset_index(drop=True)

def fill_numeric(df, method):
    out = df.copy()
    for col in out.select_dtypes(include="number").columns:
        if out[col].isna().any():
            if method == "median":
                value = out[col].median()
            elif method == "mean":
                value = out[col].mean()
            else:
                value = 0
            out[col] = out[col].fillna(value)
    return out

def fill_text(df, method):
    out = df.copy()
    numeric_cols = out.select_dtypes(include="number").columns
    for col in out.columns:
        if col in numeric_cols or not out[col].isna().any():
            continue
        value = "Unknown"
        if method == "most common value":
            modes = out[col].mode()
            if len(modes) > 0:
                value = modes.iloc[0]
        out[col] = out[col].fillna(value)
    return out

def drop_missing_rows(df):
    return df.dropna().reset_index(drop=True)