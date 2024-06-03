import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
import pandas as pd
import pickle 
from tkinter.filedialog import *
from tkinter.simpledialog import askstring

class DataFrameViewer:
    def __init__(self, root):
        self.root = root
        self.dataframes = []
        self.current_df = None
        self.setup_ui()

    def setup_ui(self):
        self.setup_left_frame()
        self.setup_dataframe_frame()


    def update_listbox(self):
        self.dataframe_listbox.delete(0, tk.END)
        for df in self.dataframes:
            self.dataframe_listbox.insert(tk.END, f"Dataframe {df}")

    def save_dataframes(self):
        file_name = asksaveasfilename( filetypes=[("Pickle files", "*.pkl")])
        
        with open(file_name, 'wb') as f:
            pickle.dump((self.dataframes, self.current_df), f)

    def open_dataframes(self):
        file_name = askopenfilename( filetypes=[("Pickle files", "*.pkl")])
        if file_name:
            with open(file_name, 'rb') as f:
                self.dataframes, self.current_df = pickle.load(f)
                
            self.update_listbox()

    def setup_left_frame(self):
        self.left_frame = ttk.Frame(self.root, padding=10)
        self.left_frame.pack(side='left', fill='y')

        self.file_picker = ttk.Button(self.left_frame, text="Choose CSV", command=self.get_csv, bootstyle="success")
        self.file_picker.pack(pady=10)



        self.dataframe_listbox = tk.Listbox(self.left_frame)
        self.dataframe_listbox.pack(expand=True, fill='both', pady=10, padx=10)
        self.dataframe_listbox.bind('<<ListboxSelect>>', self.on_listbox_select)

        self.menubar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menubar)
        self.file_menu.add_command(label="Open", command=self.open_dataframes)
        self.file_menu.add_command(label="Save", command=self.save_dataframes)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.root.config(menu=self.menubar)
    
    def setup_dataframe_frame(self):


        self.dataframe_frame = ttk.Frame(self.root, padding=10)
        self.dataframe_frame.pack(side='right', expand=True, fill='both')


    def get_csv(self):
        file_path = askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            df = pd.read_csv(file_path)
            self.dataframes.append(df)
            self.current_df = df
            
            # datframename = askstring("Fill NaN", "Enter 'mean' to fill with mean value of a column, or type a specific value:")

            self.dataframe_listbox.insert(tk.END, f"Dataframe {len(self.dataframes)}")
            self.show_dataframe(df.head(10))

    def on_listbox_select(self, event):
        selected_index = self.dataframe_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            df = self.dataframes[index]
            self.current_df = df
            self.show_dataframe(df.head(10))

    def show_dataframe(self, df, full=False):
        for widget in self.dataframe_frame.winfo_children():
            widget.destroy()

        self.create_view_options_menu()

        tree = ttk.Treeview(self.dataframe_frame, show='headings')
        tree.pack(expand=True, fill='both')

        tree["columns"] = list(df.columns)
        for column in df.columns:
            tree.heading(column, text=column)
            max_width = max(df[column].astype(str).map(len).max(), len(column)) * 10
            tree.column(column, width=max_width, anchor='w')

        rows = df.itertuples(index=False) if full else df.head(10).itertuples(index=False)
        for row in rows:
            tree.insert("", "end", values=row)

        vsb = ttk.Scrollbar(self.dataframe_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')

        hsb = ttk.Scrollbar(self.dataframe_frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=hsb.set)
        hsb.pack(side='bottom', fill='x')

    def create_view_options_menu(self):

        columns = self.current_df.columns.tolist()
        self.column_dropdown = ttk.Combobox(self.dataframe_frame, values=columns)
        self.column_dropdown.pack()
        selected_column = self.column_dropdown.get()
        
        
        self.fill_na_button = ttk.Button(self.dataframe_frame, text="Fill NaN", command=lambda: self.fill_na(selected_column), bootstyle="primary")
        self.fill_na_button.pack(pady=10)

       


        menu_button = ttk.Menubutton(self.dataframe_frame, text="View Options", bootstyle="secondary")
        menu_button.pack(anchor='ne', padx=10, pady=10)

        view_menu = tk.Menu(menu_button, tearoff=0)
        view_menu.add_command(label="Show Head", command=self.show_head)
        view_menu.add_command(label="Show Full", command=self.show_full)
        menu_button.config(menu=view_menu)

    def show_head(self):
        if self.current_df is not None:
            self.show_dataframe(self.current_df, full=False)

    def show_full(self):
        if self.current_df is not None:
            self.show_dataframe(self.current_df, full=True)


    def center_window(self, window):
        window.update_idletasks()
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        main_window_x = self.root.winfo_x()
        main_window_y = self.root.winfo_y()
        main_window_width = self.root.winfo_width()
        main_window_height = self.root.winfo_height()
        position_right = main_window_x + int(main_window_width/2 - window_width/2)
        position_down = main_window_y + int(main_window_height/2 - window_height/2)
        window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

    def fill_na(self, selected_column=None):
        if self.current_df is not None:
            option = askstring("Fill NaN", "Enter 'mean' to fill with mean value of a column, or type a specific value:")
            
            if option == 'mean':
                # Create a new window to select the column
                column_window = tk.Toplevel(self.root)
                column_window.title("Select Column for Mean Value")

                ttk.Label(column_window, text="Select Column:").pack(pady=10)
                mean_column = ttk.Combobox(column_window, values=list(self.current_df.columns))
                mean_column.pack(pady=10)
                mean_column.focus_set()

                def on_select():
                    column = mean_column.get()
                    if column in self.current_df.columns:
                        if selected_column:
                            self.current_df[selected_column].fillna(value=self.current_df[column].mean(), inplace=True)
                        else:
                            self.current_df.fillna(value=self.current_df[column].mean(), inplace=True)
                        self.show_dataframe(self.current_df.head(10))
                        column_window.destroy()
                    else:
                        tk.messagebox.showerror("Error", f"Column '{column}' not found!")
                        column_window.destroy()

                ttk.Button(column_window, text="OK", command=on_select).pack(pady=10)
                
                self.center_window(column_window)
                column_window.transient(self.root)
                column_window.grab_set()
                self.root.wait_window(column_window)
            elif option is not None:
                try:
                    fill_value = float(option)
                except ValueError:
                    fill_value = option

                if selected_column:
                    self.current_df[selected_column].fillna(value=fill_value, inplace=True)
                else:
                    self.current_df.fillna(value=fill_value, inplace=True)
                self.show_dataframe(self.current_df.head(10))
def main():
    root = ttk.Window(title="DataFrame Viewer", themename="superhero" , size=(1000, 600))
    app = DataFrameViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
