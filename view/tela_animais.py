import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk
from model.raca import Raca

class TelaAnimais:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerenciar Animais")
        self.master.geometry("800x600")

        tk.Label(self.master, text="Cadastro de Animais (Matrizes e Reprodutores)", font=("Arial", 14, "bold")).pack(pady=15)

        # form de cadastro do animal
        frame_form = tk.Frame(self.master)
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="Brinco:").grid(row=0, column=0, padx=5, sticky="e")
        self.ent_brinco = tk.Entry(frame_form, width=35)
        self.ent_brinco.grid(row=0, column=1, pady=5, sticky="w")

        tk.Label(frame_form, text="Raça:").grid(row=1, column=0, padx=5, sticky="e")
        self.cb_raca = ttk.Combobox(frame_form, values=[r.value for r in Raca], width=32, state="readonly")
        self.cb_raca.grid(row=1, column=1, pady=5, sticky="w")

        tk.Label(frame_form, text="Nascimento (DD-MM-YYYY):").grid(row=2, column=0, padx=5, sticky="e")
        self.ent_nasc = tk.Entry(frame_form, width=35)
        self.ent_nasc.grid(row=2, column=1, pady=5, sticky="w")

        # bolinhas select para tipos de animal (Exatamente igual a tela de pessoas)
        self.var_tipo = tk.StringVar(value="Femea")
        tk.Label(frame_form, text="Tipo:").grid(row=3, column=0, padx=5, sticky="e")
        
        # pra ficar a bolinha selecionavel uma ao lado da outra
        frame_radios = tk.Frame(frame_form)
        frame_radios.grid(row=3, column=1, sticky="w")
        
        tk.Radiobutton(frame_radios, text="Fêmea", variable=self.var_tipo, value="Femea").pack(side="left")
        tk.Radiobutton(frame_radios, text="Macho", variable=self.var_tipo, value="Macho").pack(side="left", padx=10)

        # botoes
        frame_btns = tk.Frame(self.master)
        frame_btns.pack(pady=15)
        tk.Button(frame_btns, text="Salvar Animal", width=15, bg="#017951", fg="white").pack(side="left", padx=5)
        tk.Button(frame_btns, text="Limpar", width=15).pack(side="left", padx=5)

        # lista de animais cadastrados no sistema
        self.tree = ttk.Treeview(self.master, columns=("brinco", "raca", "tipo", "estado"), show="headings")
        self.tree.heading("brinco", text="Brinco")
        self.tree.heading("raca", text="Raça")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("estado", text="Estado/Status")
        
        # detalhe da largura das coluns
        self.tree.column("brinco", width=100, anchor="center")
        self.tree.column("raca", width=200)
        self.tree.column("tipo", width=100, anchor="center")
        self.tree.column("estado", width=200)
        
        self.tree.pack(pady=10, fill="both", expand=True, padx=20)