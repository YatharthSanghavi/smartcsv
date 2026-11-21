import plotly.express as px

def histogram(df, col):
    return px.histogram(df, x=col, nbins=30, title=f"Distribution of {col}")

def boxplot(df, col):
    return px.box(df, y=col, points="outliers", title=f"Box plot of {col}")

def category_counts(df, col, top=15):
    counts = df[col].value_counts().head(top).reset_index()
    counts.columns = ["value", "count"]
    return px.bar(counts, x="value", y="count",
                  title=f"Most common values in {col}")

def correlation_heatmap(df):
    corr = df.corr(numeric_only=True)
    return px.imshow(corr, text_auto=".2f", zmin=-1, zmax=1,
                     color_continuous_scale="RdBu_r",
                     title="Correlation heatmap")

def scatter(df, x, y, color=None):
    return px.scatter(df, x=x, y=y, color=color, title=f"{y} vs {x}")

def group_bar(result, by, value, how):
    return px.bar(result.head(15), x=by, y=value,
                  title=f"{how} of {value} by {by}")