import re
from pathlib import Path

import pandas as pd

from .config import HOUSING_DIR

# TODO: ggf. anpassen – Name der Preisspalte im Parquet
PRICE_COLUMN = "price_per_m2"

def extract_year_from_filename(path: Path) -> int:
    """
    Extract year from filenames like:
    - flats_2017.parquet
    - flats.parquet (ignored)
    """
    match = re.search(r"_(\d{4})\.parquet$", path.name)
    if not match:
        raise ValueError(f"Could not extract year from filename: {path.name}")
    return int(match.group(1))


def load_real_estate_index(base_year: int = 2015) -> pd.DataFrame:
    """
    Load real estate snapshots and compute a price index (base_year = 100).

    Output:
        year | price_index
    """

    records = []

    files = sorted(HOUSING_DIR.glob("flats_*.parquet"))

    if not files:
        raise FileNotFoundError(f"No parquet files found in {HOUSING_DIR}")

    for file in files:
        year = extract_year_from_filename(file)

        df = pd.read_parquet(file)

        if PRICE_COLUMN not in df.columns:
            raise KeyError(
                f"Column '{PRICE_COLUMN}' not found in {file.name}. "
                f"Available columns: {list(df.columns)}"
            )

        median_price = df[PRICE_COLUMN].median()

        records.append(
            {
                "year": year,
                "price_median": median_price,
            }
        )

    price_df = pd.DataFrame(records).sort_values("year")

    # restrict to analysis window
    price_df = price_df.query("2015 <= year <= 2023")

    # determine base year dynamically if needed
    if base_year not in price_df["year"].values:
        base_year = price_df["year"].min()

    base_value = price_df.loc[
        price_df["year"] == base_year, "price_median"
    ].iloc[0]

    price_df["price_index"] = price_df["price_median"] / base_value * 100

    print(f"Using base year for housing index: {base_year}")


    return price_df[["year", "price_index"]]

if __name__ == "__main__":
    df = load_real_estate_index()
    print(df)
