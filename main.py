import os
from src import upload, clean, visualize, report


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

def main():
    uploaded_filename = upload.upload_file(UPLOAD_DIR)
    if not uploaded_filename:
        print("Upload file not found.")
        return
    if not os.path.exists(DATA_DIR):
        print(f"Error: '{DATA_DIR}' folder not found. Create it and try again.")
        return

    clean.clean_data(uploaded_filename, UPLOAD_DIR, DATA_DIR)
    cleaned_file_name = f"cleaned_{uploaded_filename}"

    visualize.visualize(cleaned_file_name, DATA_DIR, OUTPUT_DIR)
    report.create_pdf_report(OUTPUT_DIR, REPORT_DIR)

    print("/n All tasks completed successfully. You can find the cleaned data, visualizations, and report in the 'data', 'output', and'reports' folders respectively.")

if __name__ == "__main__":
    main()
