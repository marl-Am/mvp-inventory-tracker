import pandas as pd
import os

UPLOAD_DIR = "../uploads"
CLEANED_DIR = "../data"

REQUIRED_COLUMNS = [
    "date",
    "item",
    "stock",
    "price",
    "income", 
    "revenue"]
OPTIONAL_NUMERIC_COLUMNS = ["shipping_cost", "expenses"]


def clean_data(file_name, upload_dir, cleaned_dir):
    input_path = os.path.join(upload_dir, file_name)
    output_path = os.path.join(cleaned_dir, f"cleaned_{file_name}")

    if not os.path.exists(CLEANED_DIR):
        os.makedirs(CLEANED_DIR)

    try:
        df = pd.read_excel(input_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    if "item" in df.columns:
        df["item"] = df["item"].astype(str).str.strip()

    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_columns:
        print(f"Error: Missing required columns: {missing_columns}")
        return

    # remove empty rows
    df.dropna(how="all", inplace=True) 

    df.fillna(0, inplace=True)

    for col in REQUIRED_COLUMNS:
        if col == "item":
            df[col] = df[col].astype(str).str.strip()
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    for col in OPTIONAL_NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    try:
        df["date"] = pd.to_datetime(df["date"]).dt.date  # Truncate to date only
    except Exception as e:
        print(f"Warning: Could not parse 'date' column. {e}")

    try:
        df.to_excel(output_path, index=False)
        print(f"File cleaned and saved to {output_path}")
    except Exception as e:
        print(f"Error saving cleaned file: {e}")
