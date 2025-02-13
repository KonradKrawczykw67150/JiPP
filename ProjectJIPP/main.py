import tkinter as tk
from ProjectJIPP.SystemRezerwacji import SystemRezerwacji

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemRezerwacji(root)
    root.geometry("300x300")
    root.mainloop()
