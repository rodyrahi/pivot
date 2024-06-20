import pandas as pd
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring



def open_csv(dataframes):
    file_name = askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_name:
        dataframename = askstring("Dataframe", f"Enter a name for the dataframe for: {file_name}", initialvalue=f"dataframe{len(dataframes) + 1}")
        dataframe = pd.read_csv(file_name)
       
        dataframes.append((dataframename, dataframe))
