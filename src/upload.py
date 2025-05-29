import tkinter as tk
from tkinter import filedialog
import shutil
import os


def upload_file(UPLOAD_DIR):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(UPLOAD_DIR, file_name)
        shutil.copy(file_path, dest_path)
        print(f"File uploaded to: {dest_path}")
        return file_name
    else:
        print("No file selected.")
        return None
