import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from utils.functions import *
from utils.code import *
import pandas as pd
import numpy as np


global dataframes 
dataframes = []










class TabWidget(ttk.Frame):
    def __init__(self, parent, tab_names):
        super().__init__(parent)
        self.master = parent
        self.tabs = ttk.Notebook(parent)
        self.tabs.pack(fill="both", expand=True)
        self.tab_frames = []
        for tab_name in tab_names:
            tab_frame = ttk.Frame(self.tabs)
            self.tabs.add(tab_frame, text=tab_name)
            self.tab_frames.append(tab_frame)


class DataFrameListbox(ttk.Frame):
    def __init__(self, parent, dataframes):
        super().__init__(parent)
        self.master = parent
        self.dataframes = dataframes
        self.listbox = tk.Listbox(self, selectmode="single" )
        self.listbox.pack(fill="both", expand=True)
        if len(dataframes) > 0:
            for df in dataframes:
                self.listbox.insert("end", df[0] )
        self.listbox.bind('<<ListboxSelect>>', self.on_listbox_select)

    def update_listbox(self):
        if len(dataframes) > 0:
            self.listbox.delete(0, tk.END)
            for df in self.dataframes:
                self.listbox.insert(tk.END, df[0])
    
    def on_listbox_select(self, event):
        if self.listbox.curselection():
        
            selected_index = self.listbox.curselection()[0]
            tabs = main_tabs.tab_frames
            global current_dataframe
            current_dataframe = (dataframes[selected_index][0],dataframes[selected_index][1])
            table_widget(tabs[0], current_dataframe[1])
            
            show_data(dataframes[selected_index] , tabs)
        

class TopWidget(ttk.Frame):
    def __init__(self, parent, tab_names):
        super().__init__(parent)
        self.master = parent
        self.tabs = ttk.Notebook(parent)
        self.tabs.pack(fill="both", expand=True)
        self.tab_frames = []
        for tab_name in tab_names:
            tab_frame = ttk.Frame(self.tabs)
            self.tabs.add(tab_frame, text=tab_name)
            self.tab_frames.append(tab_frame)

    def add_button(self, tab_index, text, color, row, column, func=None):
        ttk.Button(self.tab_frames[tab_index], text=text, bootstyle=color, command=func).grid(row=row, column=column, sticky="new", pady=5, padx=5)

    def add_label(self, tab_index, text, row, column):
        ttk.Label(self.tab_frames[tab_index], text=text).grid(row=row, column=column, sticky="new", pady=5)

# Window setup
window = ttk.Window(themename="superhero")
window.title("Pivot")
window.geometry("1000x600")

# Frames setup
menu_frame = tk.Frame(window)
main_frame = tk.Frame(window)
tab_frame = tk.Frame(window)

menu_frame.place(x=0, y=100, relwidth=0.1, relheight=0.9)
main_frame.place(relx=0.1, y=100, relwidth=0.9, relheight=0.9)
tab_frame.place(x=0, y=0, relwidth=1, height=100)


# ttk.Label(menu_frame , background="red").pack(expand=True , fill="both")
# ttk.Label(main_frame , background="blue").pack(expand=True , fill="both")



# Grid configuration
menu_frame.columnconfigure(0, weight=1, uniform="a")
menu_frame.columnconfigure(1, weight=3, uniform="a")
menu_frame.columnconfigure(2, weight=1, uniform="a")
menu_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform="a")

# Dataframes listbox setup
dataframes_listbox = DataFrameListbox(menu_frame, dataframes)
dataframes_listbox.pack(fill="both", expand=True)

# Top tabs setup
top_tabs = TopWidget(tab_frame, ["File", "Edit", "View"])
top_tabs.add_label(tab_index=0, text="Create a new DataFrame", row=0, column=0)
top_tabs.add_button(tab_index=0, text="Csv file", color="success", row=1, column=0, func=lambda: (open_csv(dataframes), dataframes_listbox.update_listbox()))
top_tabs.add_button(tab_index=0, text="Existing DataFrame", color="primary", row=1, column=1)

# Top tabs edit setup
top_tabs.add_label(tab_index=1, text="Nan Values", row=0, column=0)
top_tabs.add_button(tab_index=1, text="Fill Nan Values", color="primary", row=1, column=0, func=lambda:    fill_nan(dataframes,current_dataframe , main_tabs))

top_tabs.add_label(tab_index=1, text="Nan Values", row=0, column=1)
top_tabs.add_button(tab_index=1, text="Replace", color="primary", row=1, column=1, func=lambda:  replace(window , dataframes , current_dataframe , main_tabs))


top_tabs.add_label(tab_index=1, text="Columns", row=0, column=2)
top_tabs.add_button(tab_index=1, text="Col To LowerCase", color="primary", row=1, column=2, func=lambda:  col_to_lowercase(window , dataframes , current_dataframe , main_tabs))


main_tabs = TabWidget(main_frame, ["Dataframe", "Description", "Info"  ])



# Run the application
window.mainloop()
