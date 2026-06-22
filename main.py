import tkinter as tk
from view.tela_principal import TelaPrincipal

def main():
    root = tk.Tk()
    
    app = TelaPrincipal(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()