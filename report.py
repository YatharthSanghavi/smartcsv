from datetime import datetime
from eda import outlier_summary
from profiling import missing_report, profile_summary


def top_correlations(df, n=3):
    """The n strongest pairs of numeric columns (ignoring the sign)."""
    corr = df.corr(numeric_only=True)
    cols = list(corr.columns)
    pairs = []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            value = corr.iloc[i, j]
            if value == value:  # skips NaN (NaN is never equal to itself)
                pairs.append((cols[i], cols[j], float(value)))
    pairs.sort(key=lambda p: abs(p[2]), reverse=True)
    return pairs[:n]


def build_report(original, cleaned, steps, file_name):
    """One readable Markdown report about the dataset."""
    before = profile_summary(original)
    after = profile_summary(cleaned)
    lines = [
        "# SmartCSV Data Report",
        f"File: {file_name}  ",
        f"Created: {datetime.now():%d %b %Y, %H:%M}",
        "",
        "## 1. Overview (original file)",
        f"- Rows: {before['rows']}",
        f"- Columns: {before['columns']}",
        f"- Duplicate rows: {before['duplicate_rows']}",
        f"- Missing cells: {before['missing_cells']}",
        "",
        "## 2. Columns with missing values",
    ]
    missing = missing_report(original)
    missing = missing[missing["missing"] > 0]
    if missing.empty:
        lines.append("- None")
    for col, row in missing.iterrows():
        lines.append(f"- {col}: {int(row['missing'])} missing ({row['missing_%']}%)")

    lines += ["", "## 3. Cleaning applied"]
    lines += [f"- {s}" for s in steps] or ["- None (data left as is)"]
    lines += [
        f"- Rows: {before['rows']} -> {after['rows']}",
        f"- Duplicate rows: {before['duplicate_rows']} -> {after['duplicate_rows']}",
        f"- Missing cells: {before['missing_cells']} -> {after['missing_cells']}",
        "",
        "## 4. Outliers in the cleaned data (IQR rule)",
    ]
    out = outlier_summary(cleaned)
    out = out[out["outliers"] > 0] if not out.empty else out
    if out.empty:
        lines.append("- No outliers found")
    else:
        for _, r in out.iterrows():
            lines.append(f"- {r['column']}: {int(r['outliers'])} outlier(s), "
                         f"normal range {r['lower_bound']} to {r['upper_bound']}")

    lines += ["", "## 5. Strongest relationships between numeric columns"]
    pairs = top_correlations(cleaned)
    if not pairs:
        lines.append("- Not enough numeric columns")
    for a, b, v in pairs:
        lines.append(f"- {a} and {b}: correlation {v:.2f}")
    return "\n".join(lines) + "\n"