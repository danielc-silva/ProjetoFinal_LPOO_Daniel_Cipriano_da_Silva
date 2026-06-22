import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

from controller.pessoas_controller import PessoaController

class TelaPessoas:
    def __init__(self, master):
        self.controller = PessoaController()
        
        self.master = master
        self.master.title("Gerenciar Pessoas")
        self.master.geometry("900x650")

        tk.Label(self.master, text="Cadastro de Proprietários e Veterinários", font=("Arial", 14, "bold")).pack(pady=15)

        # formulario de cadastro de pessoas
        frame_form = tk.Frame(self.master)
        frame_form.pack(pady=10)

        largura_entry = 40

        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, padx=5, sticky="e")
        self.ent_nome = tk.Entry(frame_form, width=largura_entry)
        self.ent_nome.grid(row=0, column=1, pady=5, sticky="w")

        tk.Label(frame_form, text="CPF:").grid(row=1, column=0, padx=5, sticky="e")
        self.ent_cpf = tk.Entry(frame_form, width=largura_entry)
        self.ent_cpf.grid(row=1, column=1, pady=5, sticky="w")

        self.var_tipo = tk.StringVar(value="Proprietario")
        tk.Label(frame_form, text="Tipo:").grid(row=2, column=0, padx=5, sticky="e")
        
        frame_radios = tk.Frame(frame_form)
        frame_radios.grid(row=2, column=1, sticky="w")
        
        tk.Radiobutton(frame_radios, text="Proprietário", variable=self.var_tipo, value="Proprietario", command=self.atualizar_campos).pack(side="left")
        tk.Radiobutton(frame_radios, text="Veterinário", variable=self.var_tipo, value="Veterinario", command=self.atualizar_campos).pack(side="left")

        self.lbl_inscricao = tk.Label(frame_form, text="Inscrição Estadual:")
        self.lbl_inscricao.grid(row=3, column=0, padx=5, sticky="e")
        self.ent_inscricao = tk.Entry(frame_form, width=largura_entry)
        self.ent_inscricao.grid(row=3, column=1, pady=5, sticky="w")

        self.lbl_fazenda = tk.Label(frame_form, text="Nome da Fazenda:")
        self.lbl_fazenda.grid(row=4, column=0, padx=5, sticky="e")
        self.ent_fazenda = tk.Entry(frame_form, width=largura_entry)
        self.ent_fazenda.grid(row=4, column=1, pady=5, sticky="w")

        self.lbl_crmv = tk.Label(frame_form, text="CRMV:", state="disabled")
        self.lbl_crmv.grid(row=5, column=0, padx=5, sticky="e")
        self.ent_crmv = tk.Entry(frame_form, width=largura_entry, state="disabled")
        self.ent_crmv.grid(row=5, column=1, pady=5, sticky="w")

        frame_btns = tk.Frame(self.master)
        frame_btns.pack(pady=15)
        tk.Button(frame_btns, text="Salvar Novo", width=12, bg="#017951", fg="white", command=self.acao_salvar).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Atualizar", width=12, bg="#f0ad4e", fg="white", command=self.acao_atualizar).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Remover", width=12, bg="#d9534f", fg="white", command=self.acao_remover).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Limpar", width=12, command=self.limpar_campos).pack(side="left", padx=5)

        # lista de pessoas cadastradas
        self.tree = ttk.Treeview(self.master, columns=("nome", "cpf", "tipo", "inscricao", "fazenda", "crmv"), show="headings")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("inscricao", text="Inscrição Est.")
        self.tree.heading("fazenda", text="Fazenda")
        self.tree.heading("crmv", text="CRMV")
        
        self.tree.column("nome", width=180, anchor="center")
        self.tree.column("cpf", width=120, anchor="center")
        self.tree.column("tipo", width=100, anchor="center")
        self.tree.column("inscricao", width=120, anchor="center")
        self.tree.column("fazenda", width=150, anchor="center")
        self.tree.column("crmv", width=100, anchor="center")
        
        self.tree.pack(pady=10, fill="both", expand=True, padx=20)

        #clicou a linha da pessoa preenche o form
        self.tree.bind("<<TreeviewSelect>>", self.preencher_formulario)

        # Atualizar sempre
        self.atualizar_tabela()




    def atualizar_campos(self):
        if self.var_tipo.get() == "Veterinario":
            self.lbl_crmv.config(state="normal")
            self.ent_crmv.config(state="normal")
            self.lbl_inscricao.config(state="disabled")
            self.ent_inscricao.delete(0, tk.END)
            self.ent_inscricao.config(state="disabled")
            self.lbl_fazenda.config(state="disabled")
            self.ent_fazenda.delete(0, tk.END)
            self.ent_fazenda.config(state="disabled")
        else:
            self.lbl_crmv.config(state="disabled")
            self.ent_crmv.delete(0, tk.END)
            self.ent_crmv.config(state="disabled")
            self.lbl_inscricao.config(state="normal")
            self.ent_inscricao.config(state="normal")
            self.lbl_fazenda.config(state="normal")
            self.ent_fazenda.config(state="normal")

    def limpar_campos(self):
        self.ent_cpf.config(state="normal") 
        self.ent_inscricao.config(state="normal")
        self.ent_fazenda.config(state="normal")
        self.ent_crmv.config(state="normal")
        
        self.ent_nome.delete(0, tk.END)
        self.ent_cpf.delete(0, tk.END)
        self.ent_inscricao.delete(0, tk.END)
        self.ent_fazenda.delete(0, tk.END)
        self.ent_crmv.delete(0, tk.END)
        
        self.var_tipo.set("Proprietario")
        self.atualizar_campos()

    def preencher_formulario(self, event):
        selecionado = self.tree.selection()
        if not selecionado:
            return
            
        valores = self.tree.item(selecionado[0], "values")
        nome, cpf, tipo, inscricao, fazenda, crmv = valores
        
        tipo = str(tipo).strip()
        
        self.limpar_campos()
        
        self.var_tipo.set(tipo)
        self.atualizar_campos()
        
        self.ent_nome.insert(0, nome)
        self.ent_cpf.insert(0, cpf)
        
        self.ent_cpf.config(state="disabled")
        
        if tipo == "Proprietario":
            self.ent_inscricao.insert(0, "" if inscricao in ("N/A", "None") else inscricao)
            self.ent_fazenda.insert(0, "" if fazenda in ("N/A", "None") else fazenda)
        elif tipo == "Veterinario":
            self.ent_crmv.insert(0, "" if crmv in ("N/A", "None") else crmv)

    def atualizar_tabela(self):
        self.tree.delete(*self.tree.get_children())

        lista_pessoas = self.controller.listar_pessoas()

        if not lista_pessoas:
            return

        for p in lista_pessoas:
            nome = getattr(p, 'nome', '')
            cpf = getattr(p, 'cpf', '')
            tipo = getattr(p, 'tipo_pessoa', p.__class__.__name__)
            inscricao = getattr(p, 'inscricao_estadual', '') or 'N/A'
            fazenda = getattr(p, 'nome_fazenda', '') or 'N/A'
            crmv = getattr(p, 'crmv', '') or 'N/A'

            self.tree.insert("", tk.END, values=(nome, cpf, tipo, inscricao, fazenda, crmv))

    def acao_salvar(self):
        nome = self.ent_nome.get().strip().title()
        cpf = self.ent_cpf.get().strip()
        tipo = self.var_tipo.get()
        inscricao = self.ent_inscricao.get().strip()
        fazenda = self.ent_fazenda.get().strip()
        crmv = self.ent_crmv.get().strip()

        sucesso, msg = self.controller.salvar_pessoa(nome, cpf, tipo, inscricao, fazenda, crmv)

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self.atualizar_tabela() 
        else:
            messagebox.showwarning("Erro", msg)

    def acao_atualizar(self):
        nome = self.ent_nome.get().strip()
        self.ent_cpf.config(state="normal")
        cpf = self.ent_cpf.get().strip()
        self.ent_cpf.config(state="disabled")
        
        tipo = self.var_tipo.get()
        inscricao = self.ent_inscricao.get().strip()
        fazenda = self.ent_fazenda.get().strip()
        crmv = self.ent_crmv.get().strip()

        if not cpf:
            messagebox.showwarning("Aviso", "clique na pessoa antes de atualizar")
            return

        sucesso, msg = self.controller.atualizar_pessoa(nome, cpf, tipo, inscricao, fazenda, crmv)
        
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self.atualizar_tabela()
        else:
            messagebox.showerror("Erro", msg)

    def acao_remover(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma pessoa na tabela clicando nela primeiro!")
            return
            
        valores = self.tree.item(selecionado[0], "values")
        cpf = valores[1]
        nome = valores[0]

        resposta = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja remover {nome} (CPF: {cpf})?")
        if resposta:
            sucesso, msg = self.controller.remover_pessoa(cpf)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.limpar_campos()
                self.atualizar_tabela()
            else:
                messagebox.showerror("Erro", msg)