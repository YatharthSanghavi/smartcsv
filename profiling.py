import pandas as pd

def profile_summary(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isna().sum().sum()),
    }

def column_types(df):
    numeric = df.select_dtypes(include="number").columns.tolist()
    categorical = [c for c in df.columns if c not in numeric]
    return {"numeric": numeric, "categorical": categorical}

def missing_report(df):
    missing = df.isna().sum()
    report = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "missing": missing,
        "missing_%": (missing / len(df) * 100).round(2),
        "unique_values": df.nunique(),
    })
    return report.sort_values("missing", ascending=False)