import io
import pandas as pd
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from utils.code import *


tree , tree_describe = None , None

dt = None

def open_popup(win):
    top= tk.Toplevel(win)
    top.geometry("400x200+%d+%d" % ((win.winfo_screenwidth()/2)-(500/2), (win.winfo_screenheight()/2)-(250/2)))
    top.title("Child Window")
    top.focus_set()
    top.grab_set()

    return top





def table_widget(parent, df):
    global dt
    if dt is not None:
        dt.destroy()

    dt = Tableview(
        master=parent,
        coldata=list(df),
        rowdata=df.to_numpy().tolist(),
        paginated=True,
        searchable=True,
        bootstyle=PRIMARY,
        pagesize=40
    )

    dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)


def show_data(dataframe, tabs ):
    
    df = dataframe[1]
    df_name = dataframe[0]
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

    code = ["import pandas as pd\n",f"df = pd.read_csv('{df_name}.csv')\n","df.duplicated(keep=False)"]

    for c in code:

        code_to_notebook(c)





def open_csv(dataframes):
    file_name = askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_name:
        dataframename = askstring("Dataframe", f"Enter a name for the dataframe for: {file_name}", initialvalue=f"dataframe{len(dataframes) + 1}")
        dataframe = pd.read_csv(file_name)
       
        dataframes.append((dataframename, dataframe))

def fill_nan(dataframes , current_dataframe , main_tabs):
    for index, df in enumerate(dataframes):
        if df[0] == current_dataframe[0]:
            value = askstring("Dataframe", f"Enter a value to fill NaN with: ", initialvalue="0")
            print(current_dataframe[1].fillna(value))

            current_dataframe = (df[0] , current_dataframe[1].fillna(value))
            dataframes[index] = current_dataframe
            table_widget(main_tabs.tab_frames[0], current_dataframe[1])

def replace(win , dataframes , current_dataframe , main_tabs):
    popup = open_popup(win)

    ttk.Label(popup , text="select or enter values to replace").pack(side="top" , padx=10 , pady=10)

    ttk.Entry(popup).pack(side="top" , padx=10 , pady=10)
    ttk.Entry(popup).pack(side="top" , padx=10 , pady=10)
    ttk.Button(popup , text="Appy Changes").pack(side="bottom" , padx=10 , pady=10)

    # open_popup(win , current_dataframe[1])
    # for index, df in enumerate(dataframes):
    #     if df[0] == current_dataframe[0]:
    #         value = askstring("Dataframe", f"Enter a value to fill NaN with: ", initialvalue="0")
            

    #         current_dataframe = (df[0] , current_dataframe[1].fillna(value))
    #         dataframes[index] = current_dataframe
    #         table_widget(main_tabs.tab_frames[0], current_dataframe[1])

def col_to_lowercase( win , dataframes , current_dataframe , main_tabs):

    popup = open_popup(win)
    cb = ttk.Combobox(popup)
    ttk.Label(popup , text="select columns to change to lowercase").pack(side="top" , padx=10 , pady=10)
    
    values = current_dataframe[1].columns.tolist() + ['All']
    
    cb["values"] =  values
    cb.current(len(values)-1)
    cb.pack(side="top" , padx=10 , pady=10)

    def change( current_dataframe , dataframes):
        for index, df in enumerate(dataframes):
            if df[0] == current_dataframe[0]:
                if cb.get() == 'All':
                           
                    current_dataframe = (
                        df[0],
                        current_dataframe[1].rename(columns=str.lower)
                    )

                    
                    dataframes[index] = current_dataframe

                    print(current_dataframe[1])
                    table_widget(main_tabs.tab_frames[0], current_dataframe[1])

                else:
                    current_dataframe = (
                        df[0],
                        current_dataframe[1].rename(columns={cb.get(): cb.get().lower()})
                    )

                    # current_dataframe = (current_dataframe[0] , current_dataframe[1][cb.get()].applymap(lambda x: x.lower() if isinstance(x, str) else x))
                    dataframes[index] = current_dataframe
                    table_widget(main_tabs.tab_frames[0], current_dataframe[1])
        popup.destroy()


    ttk.Button(popup , text="Appy Changes" , command=lambda : change(current_dataframe , dataframes)).pack(side="bottom" , padx=10 , pady=10)


