"""Step 1: read both department CSV files and print their contents."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"

# show every row and column instead of the "..." summary
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

drivers = pd.read_csv(DATA_DIR / "drivers.csv", parse_dates=["join_date"])
rides = pd.read_csv(DATA_DIR / "rides.csv", parse_dates=["ride_datetime"])

for title, df in [("DRIVER PARTNERSHIPS - drivers.csv", drivers),
                  ("RIDE OPERATIONS - rides.csv", rides)]:
    print("=" * 80)
    print(f"{title}   ({df.shape[0]} rows x {df.shape[1]} columns)")
    print("=" * 80)
    print("Column data types:")
    print(df.dtypes.to_string())
    print()
    print(df.to_string(index=False))
    print()
