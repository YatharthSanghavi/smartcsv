# SmartCSV

A Streamlit app to profile, clean, explore and report on any CSV file, built with Pandas, NumPy and Plotly.

## Features
1. **Upload any CSV** (handles empty files and non-UTF-8 text).
2. **Profile it:** rows, columns, duplicate rows, missing cells, column types, and a per-column missing-value report.
3. **Clean it:** remove duplicates, fill missing numbers (median / mean / zero), fill missing text (most common value / "Unknown"), or drop rows. Shows before -> after counts and downloads the cleaned CSV.
4. **Explore it:** histograms and box plots with IQR outlier detection, category counts, a correlation heatmap, scatter plots, and a Group by tab (like SQL `GROUP BY`).
5. **Report it:** download a Markdown report with the overview, missing values, cleaning applied, outliers and strongest correlations.

## Run it
```
pip install -r requirements.txt
streamlit run app.py
```
Try it with `sample.csv`, a made-up (synthetic) housing dataset with missing values, 8 duplicate rows and one outlier. `make_sample.py` recreates it.

## Files
| File | Job |
|---|---|
| `app.py` | The Streamlit page |
| `profiling.py` | Summary, column types, missing-value report |
| `cleaning.py` | Duplicate and missing-value cleaning |
| `eda.py` | IQR outlier detection |
| `charts.py` | Plotly charts |
| `grouping.py` | Group-by summary |
| `report.py` | Markdown report builder |

## Limits
- Reads the whole CSV into memory, so very large files will be slow.
- A column is "numeric" only if Pandas reads it as numbers; numbers stored as text are treated as text.
- Outliers are flagged, never removed automatically.