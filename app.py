import pandas as pd
import streamlit as st
from profiling import column_types, missing_report, profile_summary
from cleaning import drop_missing_rows, fill_numeric, fill_text, remove_duplicates
from charts import (boxplot, category_counts, correlation_heatmap,
                    group_bar, histogram, scatter)
from eda import outlier_bounds, outlier_summary
from grouping import group_summary
from report import build_report

st.set_page_config(page_title="SmartCSV", layout="wide")
st.title("SmartCSV")
st.caption("Upload a CSV file to profile, clean, explore and report on it.")

file = st.file_uploader("Upload a CSV file", type="csv")
if file is None:
    st.info("Upload a CSV file to begin.")
    st.stop()

try:
    df = pd.read_csv(file)
except pd.errors.EmptyDataError:
    st.error("This file is empty.")
    st.stop()
except UnicodeDecodeError:
    file.seek(0)
    df = pd.read_csv(file, encoding="latin-1")

if df.empty:
    st.error("The file has no rows.")
    st.stop()

st.subheader("1. Preview")
st.dataframe(df.head(20), width="stretch")

st.subheader("2. Dataset summary")
s = profile_summary(df)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", s["rows"])
c2.metric("Columns", s["columns"])
c3.metric("Duplicate rows", s["duplicate_rows"])
c4.metric("Missing cells", s["missing_cells"])

st.subheader("3. Column types")
t = column_types(df)
st.write("Numeric:", t["numeric"] or "none")
st.write("Categorical:", t["categorical"] or "none")

st.subheader("4. Missing values")
st.dataframe(missing_report(df), width="stretch")

st.subheader("5. Statistics")
st.dataframe(df.describe(include="all").T, width="stretch")

st.subheader("6. Clean the data")
left, right = st.columns(2)
with left:
    do_dupes = st.checkbox("Remove duplicate rows", value=True)
    num_method = st.selectbox(
        "Missing numbers", ["Leave as is", "median", "mean", "zero"])
    text_method = st.selectbox(
        "Missing text", ["Leave as is", "most common value", "Unknown"])
    do_drop = st.checkbox("Drop rows that still have missing values")

clean_df = df.copy()
steps = []
if do_dupes:
    clean_df = remove_duplicates(clean_df)
    steps.append("Removed duplicate rows")
if num_method != "Leave as is":
    clean_df = fill_numeric(clean_df, num_method)
    steps.append(f"Filled missing numbers with {num_method}")
if text_method != "Leave as is":
    clean_df = fill_text(clean_df, text_method)
    steps.append(f"Filled missing text with {text_method}")
if do_drop:
    clean_df = drop_missing_rows(clean_df)
    steps.append("Dropped rows that still had missing values")

with right:
    before = profile_summary(df)
    after = profile_summary(clean_df)
    st.write("**Before -> After**")
    st.write(f"Rows: {before['rows']} -> {after['rows']}")
    st.write(f"Duplicate rows: {before['duplicate_rows']} -> {after['duplicate_rows']}")
    st.write(f"Missing cells: {before['missing_cells']} -> {after['missing_cells']}")

st.dataframe(clean_df.head(20), width="stretch")
st.download_button(
    "Download cleaned CSV",
    data=clean_df.to_csv(index=False).encode("utf-8"),
    file_name="cleaned.csv",
    mime="text/csv",
)


st.subheader("7. Explore the cleaned data")
types = column_types(clean_df)
num_cols, cat_cols = types["numeric"], types["categorical"]

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Distributions", "Categories", "Correlation", "Scatter", "Group by"])

with tab1:
    if not num_cols:
        st.info("No numeric columns found.")
    else:
        col = st.selectbox("Numeric column", num_cols, key="dist_col")
        a, b = st.columns(2)
        a.pyplot(histogram(clean_df, col))
        b.pyplot(boxplot(clean_df, col))
        st.write("**Outliers (IQR rule)**")
        st.dataframe(outlier_summary(clean_df), width="stretch")
        low, high = outlier_bounds(clean_df[col])
        mask = (clean_df[col] < low) | (clean_df[col] > high)
        if mask.any():
            st.write(f"Rows with outliers in **{col}**:")
            st.dataframe(clean_df[mask].head(20), width="stretch")

with tab2:
    if not cat_cols:
        st.info("No categorical columns found.")
    else:
        cat = st.selectbox("Categorical column", cat_cols, key="cat_col")
        st.pyplot(category_counts(clean_df, cat))

with tab3:
    if len(num_cols) < 2:
        st.info("Need at least two numeric columns.")
    else:
        st.pyplot(correlation_heatmap(clean_df))

with tab4:
    if len(num_cols) < 2:
        st.info("Need at least two numeric columns.")
    else:
        x = st.selectbox("X axis", num_cols, key="x_col")
        y = st.selectbox("Y axis", num_cols, index=1, key="y_col")
        few = [c for c in cat_cols if clean_df[c].nunique() <= 10]
        color = st.selectbox("Colour by (optional)", ["None"] + few,
                             key="c_col")
        st.pyplot(scatter(clean_df, x, y, None if color == "None" else color))

with tab5:
    if not cat_cols or not num_cols:
        st.info("Need at least one text column and one numeric column.")
    else:
        g1, g2, g3 = st.columns(3)
        by = g1.selectbox("Group by", cat_cols, key="g_by")
        value = g2.selectbox("Value column", num_cols, key="g_val")
        how = g3.selectbox("Calculate", ["mean", "sum", "count", "median", "min", "max"],
                           key="g_how")
        result = group_summary(clean_df, by, value, how)
        st.dataframe(result, width="stretch")
        st.pyplot(group_bar(result, by, value, how))

st.subheader("8. Download a report")
report_text = build_report(df, clean_df, steps, file.name)
with st.expander("Preview the report"):
    st.markdown(report_text)
st.download_button("Download report (.md)", data=report_text.encode("utf-8"),
                   file_name="smartcsv_report.md", mime="text/markdown")