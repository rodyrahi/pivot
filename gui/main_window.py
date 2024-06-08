import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.simpledialog import askstring
from gui.dataframe_viewer import DataFrameViewer
from data_processing.cleaner import DataCleaner

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.dataframe_viewer = DataFrameViewer(self.root)
        self.setup_ui()

    def setup_ui(self):
        self.menubar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.dataframe_viewer.open_dataframes)
        self.file_menu.add_command(label="Save", command=self.dataframe_viewer.save_dataframes)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.root.config(menu=self.menubar)

        self.dataframe_viewer.pack(fill=tk.BOTH, expand=True)
