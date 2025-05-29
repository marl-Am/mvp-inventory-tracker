import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

os.makedirs("../output", exist_ok=True)

def visualize(file_name, DATA_DIR, OUTPUT_DIR):
    input_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    try:
        df = pd.read_excel(input_path)
        df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    except Exception as e:
        print(f"Error loading cleaned file: {e}")
        return

    # Stock by Item png
    plt.figure(figsize=(10, 6))
    sns.barplot(x="item", y="stock", data=df)
    plt.title("Stock by Item")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "stock_by_item.png"))
    plt.clf()

    # Income vs. Expenses Over Time png
    if 'expenses' in df.columns:
        df_grouped = df.groupby('date')[['income', 'expenses']].sum().reset_index()
    else:
        df_grouped = df.groupby('date')[['income']].sum().reset_index()
        df_grouped['expenses'] = 0

    plt.figure(figsize=(10, 6))
    sns.lineplot(x="date", y="income", data=df_grouped, label="Income")
    sns.lineplot(x="date", y="expenses", data=df_grouped, label="Expenses")
    plt.title("Income vs. Expenses Over Time")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "income_vs_expenses.png"))
    plt.clf()

    # Revenue by Item png
    df["revenue"] = (
        df["income"] - df["expenses"] if "expenses" in df.columns else df["income"]
    )

    item_revenue = df.groupby('item')['revenue'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    sns.lineplot(x="item", y="revenue", data=item_revenue)
    plt.title("Revenue by Item")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "revenue_by_item.png"))
    plt.clf()

    print(f"Charts saved to {OUTPUT_DIR} directory.")
