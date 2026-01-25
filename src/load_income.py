import pandas as pd

from .config import INCOME_FILE, INCOME_SHEET


def load_income_index(base_year: int = 2015) -> pd.DataFrame:
    """
    Load inflation-adjusted net income indices from Statistik Austria (.ods).

    Returns a long-format DataFrame:
        year | group | quantile | income_index
    Quantiles: p10, median, p90
    Groups: "Frauen und Männer", "Frauen", "Männer"
    Base year = 100
    """

    # --- Load sheet ---
    df = pd.read_excel(
        INCOME_FILE,
        engine="odf",
        sheet_name=INCOME_SHEET,
        header=1  # use second row as column names
    )

    # --- Define quantile mapping ---
    quantile_map = {
        "10%-Quantil": "p10",
        "Median": "median",
        "90%-Quantil": "p90",
    }

    # --- Keep only rows where first column is a quantile ---
    df = df[df.iloc[:, 0].isin(quantile_map.keys())].copy()

    # --- Fix group column (forward fill NaNs from merged cells) ---
    df["group"] = df.iloc[:, 1].ffill()
    df["group"] = df["group"].astype(str).str.strip()

    # --- Map quantile labels ---
    df["quantile"] = df.iloc[:, 0].map(quantile_map)

    # --- Keep only year columns ---
    year_cols = [c for c in df.columns if str(c).isdigit()]
    df = df[["group", "quantile"] + year_cols]

    # --- Convert wide → long ---
    df_long = df.melt(
        id_vars=["group", "quantile"],
        var_name="year",
        value_name="income_index_raw"
    )
    df_long["year"] = df_long["year"].astype(int)

    # --- Restrict analysis window ---
    df_long = df_long.query("2015 <= year <= 2023").reset_index(drop=True)

    # --- Rebase to base_year ---
    base_values = df_long[df_long["year"] == base_year].set_index(["group", "quantile"])["income_index_raw"]
    base_map = base_values.to_dict()

    df_long["income_index"] = df_long.apply(
        lambda row: row["income_index_raw"] / base_map[(row["group"], row["quantile"])] * 100,
        axis=1
    )

    # --- Final columns ---
    df_long = df_long[["year", "group", "quantile", "income_index"]].sort_values(["group","quantile","year"]).reset_index(drop=True)

    return df_long


# --- Sanity check ---
if __name__ == "__main__":
    df = load_income_index()
    print(df.head(12))
    print(df.tail(12))
