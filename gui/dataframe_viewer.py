import os
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
import pandas as pd
import pickle
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring
from data_processing.cleaner import DataCleaner
from utils.decorators import record_undo
from gui.widgets import DataFrameDisplay

class DataFrameViewer(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.dataframes = {}
        self.current_df_name = None
        self.undo_stack = []
        self.redo_stack = []
        self.setup_ui()

        # Bind Ctrl+Z to undo
        self.root.bind('<Control-z>', self.undo)
        # Bind Ctrl+Y to redo
        self.root.bind('<Control-y>', self.redo)

    def setup_ui(self):
        self.setup_left_frame()
        self.setup_dataframe_frame()
        self.setup_top_frame()

    def update_listbox(self):
        self.dataframe_listbox.delete(0, tk.END)
        for name in self.dataframes:
            self.dataframe_listbox.insert(tk.END, name)

    def save_dataframes(self):
        file_name = asksaveasfilename(filetypes=[("Pickle files", "*.pkl")])
        if file_name:
            with open(file_name, 'wb') as f:
                pickle.dump(self.dataframes, f)

    def open_dataframes(self):
        file_name = askopenfilename(filetypes=[("Pickle files", "*.pkl")])
        if file_name:
            with open(file_name, 'rb') as f:
                self.dataframes = pickle.load(f)
            self.update_listbox()

    def setup_left_frame(self):
        self.left_frame = ttk.Frame(self, padding=10)
        self.left_frame.pack(side='left', fill='y')

        self.file_picker = ttk.Button(self.left_frame, text="Choose CSV", command=self.get_csv, bootstyle="success")
        self.file_picker.pack(pady=10)
        
        undo_button = ttk.Button(self.left_frame, text="Undo", command=self.undo)
        undo_button.pack(pady=10)

        redo_button = ttk.Button(self.left_frame, text="Redo", command=self.redo)
        redo_button.pack(pady=10)

        self.dataframe_listbox = tk.Listbox(self.left_frame)
        self.dataframe_listbox.pack(expand=True, fill='both', pady=10, padx=10)
        self.dataframe_listbox.bind('<<ListboxSelect>>', self.on_listbox_select)

    def setup_top_frame(self):
        self.top_frame = ttk.Frame(self, padding=10)
        self.top_frame.pack(side='top', fill='x')

        self.column_dropdown = ttk.Combobox(self.top_frame)
        self.column_dropdown.pack(pady=10, side='left' , padx=5)

        self.fill_na_button = ttk.Button(self.top_frame, text="Fill NaN", command=self.fill_na, bootstyle="primary")
        self.fill_na_button.pack(pady=10, side='left' , padx=5)

        self.drop_na_button = ttk.Button(self.top_frame, text="Drop NaN", command=self.drop_na, bootstyle="danger")
        self.drop_na_button.pack(pady=10, side='left' , padx=5)

    def setup_dataframe_frame(self):
        self.dataframe_frame = DataFrameDisplay(self)
        self.dataframe_frame.pack(side='bottom', expand=True, fill='both')
       
    def get_csv(self):
        file_path = askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            df = pd.read_csv(file_path)
            file_name = os.path.basename(file_path)
            dataframename = askstring("Dataframe", f"Enter a name for the dataframe for: {file_name}", initialvalue=f"dataframe{len(self.dataframes) + 1}")
            if dataframename:
                self.dataframes[dataframename] = df
                self.current_df_name = dataframename
                self.update_listbox()
                self.update_top_frame()
                self.dataframe_frame.display_data(df.head(10))

    def on_listbox_select(self, event):
        selected_index = self.dataframe_listbox.curselection()
        if selected_index:
            self.current_df_name = self.dataframe_listbox.get(selected_index[0])
            df = self.dataframes[self.current_df_name]
            self.update_top_frame()
            self.dataframe_frame.display_data(df.head(10))

    def update_top_frame(self):
        if self.current_df_name:
            columns = self.dataframes[self.current_df_name].columns.tolist()
            self.column_dropdown['values'] = columns

    @record_undo
    def fill_na(self):
        if self.current_df_name is not None:
            option = askstring("Fill NaN", "Enter 'mean' to fill with mean value of a column, or type a specific value:")
            df = self.dataframes[self.current_df_name]

            if option == 'mean':
                column = self.column_dropdown.get()
                if column:
                    df[column].fillna(df[column].mean(), inplace=True)
            elif option is not None:
                try:
                    fill_value = float(option)
                except ValueError:
                    fill_value = option
                df.fillna(fill_value, inplace=True)

            self.dataframe_frame.display_data(df.head(10))

    @record_undo
    def drop_na(self):
        if self.current_df_name is not None:
            column = self.column_dropdown.get()
            df = self.dataframes[self.current_df_name]
            if column:
                df.dropna(subset=[column], inplace=True)
            else:
                df.dropna(inplace=True)
            self.dataframe_frame.display_data(df.head(10))

    def undo(self, event=None):
        if self.undo_stack:
            self.redo_stack.append(self.dataframes[self.current_df_name].copy())
            self.dataframes[self.current_df_name] = self.undo_stack.pop()
            self.dataframe_frame.display_data(self.dataframes[self.current_df_name].head(10))

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.dataframes[self.current_df_name].copy())
            self.dataframes[self.current_df_name] = self.redo_stack.pop()
            self.dataframe_frame.display_data(self.dataframes[self.current_df_name].head(10))
