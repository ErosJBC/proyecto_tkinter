from tkinter import *
from app import *

def main():
    root = Tk()
    root.wm_title("Sistema de Bonos")
    root.wm_resizable(0, 0)
    app = Application(root)
    app.mainloop()

if __name__ == '__main__':
    main()