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
        self.root.geometry("500x380")
        self.root.eval('tk::PlaceWindow . center') # só pra centralizar na tela

        tk.Label(self.root, text="Gestão da Fazenda", font=("Arial", 18, "bold")).pack(pady=12)
        
        tk.Label(self.root, text="Funções Exclusivas dos Proprietários", font=("Arial", 10, "bold")).pack(pady=10)

        frame_proprietario = tk.Frame(self.root)
        frame_proprietario.pack()

        btn_pessoas = tk.Button(frame_proprietario, text="Gerenciar Pessoas", width=25, height=2, command=self.abrir_tela_pessoas)
        btn_pessoas.grid(row=0, column=0, pady=10)

        btn_animais = tk.Button(frame_proprietario, text="Gerenciar Animais", width=25, height=2, command=self.abrir_tela_animais)
        btn_animais.grid(row=1, column=0, pady=10)

        tk.Label(self.root, text="Funções Gerais", font=("Arial", 10, "bold")).pack(pady=10)
    
        frame_gerais = tk.Frame(self.root)
        frame_gerais.pack()

        btn_manejos = tk.Button(frame_gerais, text="Cadastrar Manejo", width=25, height=2, command=self.abrir_tela_manejos)
        btn_manejos.grid(row=0, column=0, pady=10)

    def abrir_tela_pessoas(self):
        janela_pessoas = tk.Toplevel(self.root)
        app_pessoas = TelaPessoas(janela_pessoas)
        janela_pessoas.grab_set()

    def abrir_tela_animais(self):
        janela_animais = tk.Toplevel(self.root)
        app_animais = TelaAnimais(janela_animais)
        janela_animais.grab_set()

    def abrir_tela_manejos(self):
        janela_manejos = tk.Toplevel(self.root)
        app_manejos = TelaManejos(janela_manejos)
        janela_manejos.grab_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = TelaPrincipal(root)
    root.mainloop()