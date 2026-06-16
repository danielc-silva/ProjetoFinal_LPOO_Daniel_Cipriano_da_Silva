import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from model.raca import Raca

# Presumindo que você criará o AnimalController seguindo o mesmo padrão do PessoaController
from controller.animais_controller import AnimalController

class TelaAnimais:
    def __init__(self, master):
        self.controller = AnimalController()
        
        self.master = master
        self.master.title("Gerenciar Animais")
        self.master.geometry("900x650") # Ajustado para o mesmo tamanho da tela de Pessoas

        tk.Label(self.master, text="Cadastro de Animais (Matrizes e Reprodutores)", font=("Arial", 14, "bold")).pack(pady=15)

        # --- Formulário de Cadastro ---
        frame_form = tk.Frame(self.master)
        frame_form.pack(pady=10)

        largura_entry = 40

        tk.Label(frame_form, text="Brinco:").grid(row=0, column=0, padx=5, sticky="e")
        self.ent_brinco = tk.Entry(frame_form, width=largura_entry)
        self.ent_brinco.grid(row=0, column=1, pady=5, sticky="w")

        tk.Label(frame_form, text="Raça:").grid(row=1, column=0, padx=5, sticky="e")
        # Ajustei a largura do Combobox para alinhar melhor com os Entries de largura 40
        self.cb_raca = ttk.Combobox(frame_form, values=[r.value for r in Raca], width=37, state="readonly")
        self.cb_raca.grid(row=1, column=1, pady=5, sticky="w")

        tk.Label(frame_form, text="Nascimento (DD/MM/YYYY):").grid(row=2, column=0, padx=5, sticky="e")
        self.ent_nasc = tk.Entry(frame_form, width=largura_entry)
        self.ent_nasc.grid(row=2, column=1, pady=5, sticky="w")

        self.var_tipo = tk.StringVar(value="Femea")
        tk.Label(frame_form, text="Tipo:").grid(row=3, column=0, padx=5, sticky="e")
        
        frame_radios = tk.Frame(frame_form)
        frame_radios.grid(row=3, column=1, sticky="w")
        
        # O comando 'atualizar_campos' é chamado ao trocar a bolinha, igualzinho na TelaPessoas
        tk.Radiobutton(frame_radios, text="Fêmea", variable=self.var_tipo, value="Femea", command=self.atualizar_campos).pack(side="left")
        tk.Radiobutton(frame_radios, text="Macho", variable=self.var_tipo, value="Macho", command=self.atualizar_campos).pack(side="left", padx=10)

        # Campo exclusivo de FÊMEA
        self.lbl_estado = tk.Label(frame_form, text="Estado Reprodutivo:")
        self.lbl_estado.grid(row=4, column=0, padx=5, sticky="e")
        self.cb_estado = ttk.Combobox(frame_form, values=["Vazia", "Inseminada", "Prenha"], width=37, state="readonly")
        self.cb_estado.grid(row=4, column=1, pady=5, sticky="w")

        # Campo exclusivo de MACHO
        self.lbl_castrado = tk.Label(frame_form, text="Castrado:", state="disabled")
        self.lbl_castrado.grid(row=5, column=0, padx=5, sticky="e")
        self.cb_castrado = ttk.Combobox(frame_form, values=["Sim", "Não"], width=37, state="disabled")
        self.cb_castrado.grid(row=5, column=1, pady=5, sticky="w")

        # --- Botões (Idênticos aos da TelaPessoas) ---
        frame_btns = tk.Frame(self.master)
        frame_btns.pack(pady=15)
        tk.Button(frame_btns, text="Salvar Novo", width=12, bg="#017951", fg="white", command=self.acao_salvar).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Atualizar", width=12, bg="#f0ad4e", fg="white", command=self.acao_atualizar).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Remover", width=12, bg="#d9534f", fg="white", command=self.acao_remover).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Limpar", width=12, command=self.limpar_campos).pack(side="left", padx=5)

        # --- Lista de Animais Cadastrados (Treeview) ---
        self.tree = ttk.Treeview(self.master, columns=("brinco", "raca", "nascimento", "tipo", "estado", "castrado"), show="headings")
        self.tree.heading("brinco", text="Brinco")
        self.tree.heading("raca", text="Raça")
        self.tree.heading("nascimento", text="Nascimento")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("estado", text="Estado Reprod.")
        self.tree.heading("castrado", text="Castrado")
        
        self.tree.column("brinco", width=80, anchor="center")
        self.tree.column("raca", width=150)
        self.tree.column("nascimento", width=100, anchor="center")
        self.tree.column("tipo", width=80, anchor="center")
        self.tree.column("estado", width=120, anchor="center")
        self.tree.column("castrado", width=80, anchor="center")
        
        self.tree.pack(pady=10, fill="both", expand=True, padx=20)

        # Clicou na linha, preenche o form
        self.tree.bind("<<TreeviewSelect>>", self.preencher_formulario)

        # Inicia a tela atualizando os campos e a tabela
        self.atualizar_campos()
        self.atualizar_tabela()

    def atualizar_campos(self):
        """Ativa/Desativa campos dependendo se é Macho ou Fêmea"""
        if self.var_tipo.get() == "Macho":
            self.lbl_castrado.config(state="normal")
            self.cb_castrado.config(state="readonly")
            
            self.lbl_estado.config(state="disabled")
            self.cb_estado.set("")
            self.cb_estado.config(state="disabled")
        else:
            self.lbl_estado.config(state="normal")
            self.cb_estado.config(state="readonly")
            
            self.lbl_castrado.config(state="disabled")
            self.cb_castrado.set("")
            self.cb_castrado.config(state="disabled")

    def limpar_campos(self):
        self.ent_brinco.config(state="normal")
        self.cb_estado.config(state="normal")
        self.cb_castrado.config(state="normal")
        
        self.ent_brinco.delete(0, tk.END)
        self.cb_raca.set("")
        self.ent_nasc.delete(0, tk.END)
        self.cb_estado.set("")
        self.cb_castrado.set("")
        
        self.var_tipo.set("Femea")
        self.atualizar_campos()

    def preencher_formulario(self, event):
        selecionado = self.tree.selection()
        if not selecionado:
            return
            
        valores = self.tree.item(selecionado[0], "values")
        brinco, raca, nascimento, tipo, estado, castrado = valores
        
        tipo = str(tipo).strip()
        
        self.limpar_campos()
        
        self.var_tipo.set(tipo)
        self.atualizar_campos()
        
        self.ent_brinco.insert(0, brinco)
        self.cb_raca.set(raca)
        self.ent_nasc.insert(0, nascimento)
        
        # Bloqueia a Chave Primária (Brinco)
        self.ent_brinco.config(state="disabled")
        
        if tipo == "Femea":
            self.cb_estado.set("" if estado in ("N/A", "None") else estado)
        elif tipo == "Macho":
            self.cb_castrado.set("" if castrado in ("N/A", "None") else castrado)

    def atualizar_tabela(self):
        self.tree.delete(*self.tree.get_children())

        lista_animais = self.controller.listar_animais()

        if not lista_animais:
            return

        for a in lista_animais:
            brinco = getattr(a, 'brinco', '')
            
            raca_obj = getattr(a, 'raca', '')
            raca = raca_obj.value if hasattr(raca_obj, 'value') else raca_obj
            
            nascimento_cru = getattr(a, 'data_nascimento', '')
            if hasattr(nascimento_cru, 'strftime'):
                nascimento = nascimento_cru.strftime('%d/%m/%Y')
            else:
                nascimento = nascimento_cru
                
            tipo = getattr(a, 'tipo_animal', a.__class__.__name__)
            estado = getattr(a, 'estado_reprodutivo', '') or 'N/A'
            
            castrado = getattr(a, 'castrado', None) 
            
            if castrado is True or castrado == "Sim":
                str_castrado = "Sim"
            elif castrado is False or castrado == "Não":
                str_castrado = "Não"
            else:
                str_castrado = "N/A"

            self.tree.insert("", tk.END, values=(brinco, raca, nascimento, tipo, estado, str_castrado))


    def acao_salvar(self):
        brinco_str = self.ent_brinco.get().strip()
        raca = self.cb_raca.get().strip()
        nasc = self.ent_nasc.get().strip()
        tipo = self.var_tipo.get()
        estado = self.cb_estado.get().strip()
        castrado = self.cb_castrado.get().strip()

        try:
            brinco_int = int(brinco_str)
        except ValueError:
            messagebox.showwarning("Aviso", "O campo Brinco precisa ser um número inteiro válido!")
            return

        sucesso, msg = self.controller.salvar_animal(brinco_int, raca, nasc, tipo, estado, castrado)

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self.atualizar_tabela() 
        else:
            messagebox.showwarning("Erro", msg)


    def acao_atualizar(self):
        self.ent_brinco.config(state="normal")
        brinco_str = self.ent_brinco.get().strip()
        self.ent_brinco.config(state="disabled")
        
        if not brinco_str:
            messagebox.showwarning("Aviso", "Clique em um animal na tabela antes de atualizar!")
            return

        try:
            brinco_int = int(brinco_str)
        except ValueError:
            messagebox.showwarning("Aviso", "O campo Brinco precisa ser um número inteiro válido!")
            return

        raca = self.cb_raca.get().strip()
        nasc = self.ent_nasc.get().strip()
        tipo = self.var_tipo.get()
        estado = self.cb_estado.get().strip()
        castrado = self.cb_castrado.get().strip()

        sucesso, msg = self.controller.atualizar_animal(brinco_int, raca, nasc, tipo, estado, castrado)
        
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self.atualizar_tabela()
        else:
            messagebox.showerror("Erro", msg)

    def acao_remover(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um animal na tabela clicando nele primeiro!")
            return
            
        valores = self.tree.item(selecionado[0], "values")
        brinco = valores[0]
        raca = valores[1]

        resposta = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja remover o animal {raca} (Brinco: {brinco})?")
        if resposta:
            sucesso, msg = self.controller.remover_animal(brinco)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.limpar_campos()
                self.atualizar_tabela()
            else:
                messagebox.showerror("Erro", msg)