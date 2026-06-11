import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from view.tela_pessoas import TelaPessoas
from view.tela_animais import TelaAnimais

class TelaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão Reprodutiva Bovino")
        self.root.geometry("500x350")
        self.root.eval('tk::PlaceWindow . center') # Centraliza na tela

        tk.Label(self.root, text="Gestão da Fazenda", font=("Arial", 18, "bold")).pack(pady=30)

        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack()

        btn_pessoas = tk.Button(frame_botoes, text="Gerenciar Pessoas", width=25, height=2, command=self.abrir_tela_pessoas)
        btn_pessoas.grid(row=0, column=0, pady=10)

        btn_animais = tk.Button(frame_botoes, text="Gerenciar Animais", width=25, height=2, command=self.abrir_tela_animais)
        btn_animais.grid(row=1, column=0, pady=10)

    def abrir_tela_pessoas(self):
        janela_pessoas = tk.Toplevel(self.root)
        app_pessoas = TelaPessoas(janela_pessoas) # Correto e seguro
        janela_pessoas.grab_set()

    def abrir_tela_animais(self):
        janela_animais = tk.Toplevel(self.root)
        app_animais = TelaAnimais(janela_animais) # Padronizado e seguro!
        janela_animais.grab_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = TelaPrincipal(root)
    root.mainloop()