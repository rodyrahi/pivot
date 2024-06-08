import tkinter as tk
from tkinter import ttk
import pandas as pd

class DataFrameDisplay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.treeview = ttk.Treeview(self, show='headings')
        self.treeview.pack(expand=True, fill='both')

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')

        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(xscrollcommand=hsb.set)
        hsb.pack(side='bottom', fill='x')

    def display_data(self, data: pd.DataFrame):
        self.treeview.delete(*self.treeview.get_children())
        self.treeview["columns"] = list(data.columns)
        for col in data.columns:
            self.treeview.heading(col, text=col)
            max_width = max(data[col].astype(str).map(len).max(), len(col)) * 10
            self.treeview.column(col, width=max_width, anchor='w')

        for row in data.itertuples(index=False):
            self.treeview.insert("", "end", values=row)
