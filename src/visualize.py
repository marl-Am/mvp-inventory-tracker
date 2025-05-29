import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

DATA_DIR = "../data"
OUTPUT_DIR = "../output"

def visualize(file_name):
    input_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    try:
        df = pd.read_excel(input_path)
    except Exception as e:
        print(f"Error loading cleaned file: {e}")
        return
    
    df['date'] = pd.to_datetime(df['date'])

    plt.figure(figsize=(10, 6))
    sns.barplot(x="item", y="stock", data=df)
    plt.title("Stock Levels by Item")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "stock_by_item.png"))
    plt.clf()

    if 'expenses' in df.columns:
        df_grouped = df.gruoupby('date')[['income', 'expenses']].sum().reset_index()
    else:
        df_grouped = df.groupby('date')[['income']].sum().reset_index()
        df_grouped['expenses'] = 0

    plt.figure(figsize=(10, 6))
    sns.lineplot(x="date", y="income", data=df_grouped, label="Income")
    sns.lineplot(x="date", y="expenses", data=df_grouped, label="Expenses")
    plt.title("Income and Expenses Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "revenue_by_item.png"))
    plt.clf()

    print(f"Charts saved to {OUTPUT_DIR} directory.")

    if __name__ == "__main__":
        visualize("cleaned_file.xlsx")