import tkinter as tk
import ttkbootstrap as ttk


dataframes = ['raj' , 'raj' , 'raj' ]

class DataFrameListbox(ttk.Frame):
     def __init__(self, parent, dataframes):
            super().__init__(parent)
            self.master = parent
            self.dataframes = dataframes
            self.listbox = tk.Listbox(self, selectmode="single")
            self.listbox.pack(fill="both", expand=True)
            for df_name in dataframes:
                self.listbox.insert("end", df_name)

            

class top_widget(ttk.Frame):
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

    def add_button(self, tab_index , text , color , row , column):
            ttk.Button(self.tab_frames[tab_index], text=text , bootstyle=color).grid(row=row, column=column, sticky="new" , pady=5 , padx=5 )
         




# Window setup
window = ttk.Window(themename="superhero")
window.title("Pivot")
window.geometry("1000x600")

# Frames setup
menu_frame = tk.Frame(window)
main_frame = tk.Frame(window)
tab_frame = tk.Frame(window)

menu_frame.place(x=0, y=100, relwidth=0.1, relheight=0.9)
main_frame.place(relx=0.3, y=100, relwidth=0.9, relheight=0.9)
tab_frame.place(x=0, y=0, relwidth=1, height=100 )


# Grid configuration
menu_frame.columnconfigure(0, weight=1, uniform="a")  
menu_frame.columnconfigure(1, weight=3, uniform="a")  
menu_frame.columnconfigure(2, weight=1, uniform="a")
menu_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform="a")

top_tabs = top_widget(tab_frame , ["File", "Edit", "View"])
top_tabs.add_button(tab_index=0 , text="Open" , color="success" , row=0, column=0)
top_tabs.add_button(tab_index=0 , text="Create DataFrame" , color="primary" , row=0, column=1)

dataframes_listbox = DataFrameListbox(menu_frame, dataframes).pack(fill="both", expand=True )


# Run the application
window.mainloop()
