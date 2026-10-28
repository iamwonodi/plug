import pandas as pd
#  -------------------------------
# Patch for pandas 3.x compatibility with lightweight charts
# -------------------------------
def patched_df_datetime_format(self, df, exclude_lowercase=None):
    df = df.copy()

    df.columns = self._format_labels(
        df,
        df.columns,
        df.index,
        exclude_lowercase
    )

    self._set_interval(df)

    if not pd.api.types.is_datetime64_any_dtype(df["time"]):
        df["time"] = pd.to_datetime(df["time"], utc=True)

    dtype = str(df["time"].dtype)

    if "[us" in dtype:
        divisor = 10**6
    elif "[ms" in dtype:
        divisor = 10**3
    else:               # datetime64[ns]
        divisor = 10**9

    df["time"] = df["time"].astype("int64") // divisor

    return df
