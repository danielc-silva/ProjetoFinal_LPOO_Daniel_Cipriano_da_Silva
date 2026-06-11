import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk

class TelaPessoas:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerenciar Pessoas")
        self.master.geometry("800x600")

        tk.Label(self.master, text="Cadastro de Proprietários e Veterinários", font=("Arial", 14, "bold")).pack(pady=15)

        # form de cadstro de pessoas
        frame_form = tk.Frame(self.master)
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, padx=5, sticky="e")
        self.ent_nome = tk.Entry(frame_form, width=35)
        self.ent_nome.grid(row=0, column=1, pady=5)

        tk.Label(frame_form, text="CPF:").grid(row=1, column=0, padx=5, sticky="e")
        self.ent_cpf = tk.Entry(frame_form, width=35)
        self.ent_cpf.grid(row=1, column=1, pady=5)

        # bolinhas selct para tipos de pessoa
        self.var_tipo = tk.StringVar(value="Proprietario")
        tk.Label(frame_form, text="Tipo:").grid(row=2, column=0, padx=5, sticky="e")
        
        # pra ficar a bolinha selecionavel uma ao lado da outra
        frame_radios = tk.Frame(frame_form)
        frame_radios.grid(row=2, column=1, sticky="w")
        
        tk.Radiobutton(frame_radios, text="Proprietário", variable=self.var_tipo, value="Proprietario", 
                       command=self.atualizar_campos).pack(side="left")
        tk.Radiobutton(frame_radios, text="Veterinário", variable=self.var_tipo, value="Veterinario", 
                       command=self.atualizar_campos).pack(side="left")

        # o campo do identif de vet inicia destivado
        self.lbl_crmv = tk.Label(frame_form, text="CRMV:", state="disabled")
        self.lbl_crmv.grid(row=3, column=0, padx=5, sticky="e")
        self.ent_crmv = tk.Entry(frame_form, width=35, state="disabled")
        self.ent_crmv.grid(row=3, column=1, pady=5)

        frame_btns = tk.Frame(self.master)
        frame_btns.pack(pady=15)
        tk.Button(frame_btns, text="Salvar Pessoa", width=15, bg="#017951", fg="white").pack(side="left", padx=5)
        tk.Button(frame_btns, text="Limpar", width=15).pack(side="left", padx=5)

        # lista de pessoas cadastradas no sist
        self.tree = ttk.Treeview(self.master, columns=("nome", "cpf", "tipo", "crmv"), show="headings")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("crmv", text="CRMV")
        
        # Ajustando a largura das colunas
        self.tree.column("nome", width=250)
        self.tree.column("cpf", width=150)
        self.tree.column("tipo", width=100)
        self.tree.column("crmv", width=150)
        
        self.tree.pack(pady=10, fill="both", expand=True, padx=20)

    # faz a ativação ou desativação do campo do CrMV dependendo da pessoa select
    def atualizar_campos(self):
        """
        Ativa ou desativa o campo CRMV dependendo do tipo de pessoa selecionado.
        """
        if self.var_tipo.get() == "Veterinario":
            self.lbl_crmv.config(state="normal")
            self.ent_crmv.config(state="normal")
        else:
            self.lbl_crmv.config(state="disabled")
            self.ent_crmv.delete(0, tk.END)
            self.ent_crmv.config(state="disabled")
