import streamlit as st
import os
import pandas as pd
from src import clean, visualize, report
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

for folder in [UPLOAD_DIR, DATA_DIR, OUTPUT_DIR, REPORT_DIR]:
    os.makedirs(folder, exist_ok=True)

st.set_page_config(page_title="Inventory Tracker", layout="wide")
st.title("Inventory & Revenue Dashboard")

uploaded_file = st.file_uploader("Upload your excel file", type=["xlsx", "xls"])
st.markdown("### Don't have a file?")
with open("sample.xlsx", "rb") as f:
    st.download_button("Download Sample Excel Template", f, file_name="sample.xlsx")

if uploaded_file:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File uploaded: {uploaded_file.name}")

    cleaned_filename = f"cleaned_{uploaded_file.name}"
    clean.clean_data(uploaded_file.name, UPLOAD_DIR, DATA_DIR)
    cleaned_path = os.path.join(DATA_DIR, cleaned_filename)

    if os.path.exists(cleaned_path):
        df = pd.read_excel(cleaned_path)
        st.subheader("Cleaned Data:")
        st.dataframe(df, use_container_width=True)

        visualize.visualize(cleaned_filename, DATA_DIR, OUTPUT_DIR)

        st.subheader("Charts")
        charts = [
            ("Stock by Item", "stock_by_item.png"),
            ("Income vs Expenses", "income_vs_expenses.png"),
            ("Revenue by Item", "revenue_by_item.png"),
            ("Shipping Cost Over Time", "shipping_cost_over_time.png"),
        ]
        for title, chart in charts:
            chart_path = os.path.join(OUTPUT_DIR, chart)
            if os.path.exists(chart_path):
                st.image(chart_path, caption=title, use_container_width=True)
            else:
                st.warning(f"Chart not found: {chart}")

        report.create_pdf_report(OUTPUT_DIR, REPORT_DIR)

        st.subheader("Download Reports")

        pdf_path = os.path.join(REPORT_DIR, "business_report.pdf")

        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "Download PDF Report", f, file_name="business_report.pdf"
                )

    else:
        st.error("Cleaned file was not created.")
