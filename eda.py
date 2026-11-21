import numpy as np
import pandas as pd

def outlier_bounds(values):
    q1, q3 = np.percentile(values.dropna(), [25, 75])
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr

def outlier_summary(df):
    rows = []
    for col in df.select_dtypes(include="number").columns:
        values = df[col].dropna()
        if values.empty:
            continue
        low, high = outlier_bounds(values)
        count = int(((values < low) | (values > high)).sum())
        rows.append({"column": col, "outliers": count,
                     "lower_bound": round(float(low), 2),
                     "upper_bound": round(float(high), 2)})
    return pd.DataFrame(rows)