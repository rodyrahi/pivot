import io
import pandas as pd
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *



tree , tree_describe = None , None

def show_data(df, tabs):
    
    global tree 
    global tree_describe
    
    
    if tree_describe is not None:
        tree.destroy()
        tree_describe.destroy()

    
    df_duplicates = df[df.duplicated(keep=False)]
    duplicated_sums = df_duplicates.sum()
    print(duplicated_sums)
    data_info = {
        "Sno.": range(len(df.columns)),
        "Count": df.count(),
        "Column": df.columns,
        "Null Count": df.isnull().sum(),
        "Data Type": df.dtypes,
        "Duplicates": duplicated_sums
    }
    info_df = pd.DataFrame(data_info)

    # Create a Treeview widget
    tree = ttk.Treeview(tabs[1], columns=("Sno.", "Count" , "Column", "Null Count", "Data Type" , "Duplicates"), show="headings")
    
    tree.heading("Sno.", text="Sno.")
    tree.heading("Count", text="Count")
    tree.heading("Column", text="Column")
    tree.heading("Null Count", text="Null Count")
    tree.heading("Data Type", text="Data Type")
    tree.heading("Duplicates", text="Duplicates")
    # Insert data into the Treeview
    for index, row in info_df.iterrows():
        tree.insert("", "end", values=( row["Sno."] , row["Count"] ,row["Column"], row["Null Count"], row["Data Type"] , row["Duplicates"]))

    # Pack the Treeview into the tab
    tree.pack(expand=True, fill="both")



    describe_df = df.describe().transpose()
    describe_df['Column'] = describe_df.index

    # Create a Treeview widget for describe() summary
    tree_describe = ttk.Treeview(tabs[2], columns=list(describe_df.columns), show="headings")
    for col in describe_df.columns:
        tree_describe.heading(col, text=col)

    # Insert describe() data into the Treeview
    for index, row in describe_df.iterrows():
        tree_describe.insert("", "end", values=list(row))

    # Pack the Treeview for describe() summary
    tree_describe.pack(expand=True, fill="both" , padx=10, pady=10)


def open_csv(dataframes):
    file_name = askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_name:
        dataframename = askstring("Dataframe", f"Enter a name for the dataframe for: {file_name}", initialvalue=f"dataframe{len(dataframes) + 1}")
        dataframe = pd.read_csv(file_name)
       
        dataframes.append((dataframename, dataframe))
