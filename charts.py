from matplotlib.figure import Figure


def _new_figure(width=6, height=4):
    fig = Figure(figsize=(width, height))
    ax = fig.subplots()
    return fig, ax


def histogram(df, col):
    fig, ax = _new_figure()
    ax.hist(df[col].dropna(), bins=30, color="#4C78A8", edgecolor="white")
    ax.set_title(f"Distribution of {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("Count")
    fig.tight_layout()
    return fig


def boxplot(df, col):
    fig, ax = _new_figure()
    ax.boxplot(df[col].dropna(), flierprops={"marker": "o", "markerfacecolor": "red"})
    ax.set_title(f"Box plot of {col}")
    ax.set_ylabel(col)
    ax.set_xticks([])
    fig.tight_layout()
    return fig


def _bar(labels, values, title, xlabel, ylabel):
    fig, ax = _new_figure(7, 4)
    ax.bar([str(x) for x in labels], values, color="#4C78A8")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


def category_counts(df, col, top=15):
    counts = df[col].value_counts().head(top)
    return _bar(counts.index, counts.values,
                f"Most common values in {col}", col, "Count")


def correlation_heatmap(df):
    corr = df.corr(numeric_only=True)
    fig, ax = _new_figure(6, 5)
    image = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    names = list(corr.columns)
    ax.set_xticks(range(len(names)), labels=names, rotation=45, ha="right")
    ax.set_yticks(range(len(names)), labels=names)
    for i in range(len(names)):
        for j in range(len(names)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
    fig.colorbar(image, ax=ax)
    ax.set_title("Correlation heatmap")
    fig.tight_layout()
    return fig


def scatter(df, x, y, color=None):
    fig, ax = _new_figure()
    if color is None:
        ax.scatter(df[x], df[y], alpha=0.6, color="#4C78A8")
    else:
        for name, part in df.groupby(color):
            ax.scatter(part[x], part[y], alpha=0.6, label=str(name))
        ax.legend(title=color)
    ax.set_title(f"{y} vs {x}")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    fig.tight_layout()
    return fig


def group_bar(result, by, value, how):
    top = result.head(15)
    return _bar(top[by], top[value], f"{how} of {value} by {by}", by, f"{how} of {value}")