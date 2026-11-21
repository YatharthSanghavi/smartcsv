def group_summary(df, by, value, how):
    """Same idea as SQL: SELECT by, how(value) FROM table GROUP BY by."""
    result = df.groupby(by)[value].agg(how).reset_index()
    return result.sort_values(value, ascending=False).reset_index(drop=True)