import ttkbootstrap as ttk
from gui.main_window import MainWindow

def main():
    root = ttk.Window(title="Pivot", themename="superhero", size=(1000, 600))
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
