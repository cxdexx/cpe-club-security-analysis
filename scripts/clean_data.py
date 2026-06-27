import pandas as pd

INPUT_PATH = "data/raw_nigeria_acled.csv"
OUTPUT_PATH = "data/cleaned_nigeria_conflict.csv"


def load_data():
    df = pd.read_csv(INPUT_PATH)
    print(f"Loaded {len(df)} records from {INPUT_PATH}")
    return df


def clean_data(df):
    # Step 4a - Drop records missing State (admin1) or LGA (admin2)
    # Added .copy() to eliminate downstream SettingWithCopyWarnings
    df = df.dropna(subset=["admin1", "admin2"]).copy()
    print(f"Records after dropping missing admin1/admin2: {len(df)}")

    # Step 4b - Convert data types
    df["fatalities"] = (
        pd.to_numeric(df["fatalities"], errors="coerce").fillna(0).astype(int)
    )

    # CRITICAL FIX: Convert string column to actual Datetime objects
    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")

    # Step 4c - Standardize state names
    df["admin1"] = (
        df["admin1"]
        .str.strip()      # Remove leading/trailing spaces
        .str.title()      # Standardize capitalization (e.g., "BORNO", "borno" -> "Borno")
    )

    # Step 4d - Create Month_Year column (Now safe to execute)
    # errors="coerce" in 4b means invalid dates become NaT; we drop them or handle them safely here
    df = df.dropna(subset=["event_date"]) 
    df["Month_Year"] = df["event_date"].dt.to_period("M").astype(str)

    # Diagnostic print statement
    print("\n--- Admin1 Value Counts ---")
    print(df["admin1"].value_counts())

    return df


if __name__ == "__main__":
    raw_df = load_data()
    cleaned_df = clean_data(raw_df)
    
    cleaned_df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSuccessfully saved cleaned data to {OUTPUT_PATH}")