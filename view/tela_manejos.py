import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

from controller.manejos_controller import ManejoController
from controller.pessoas_controller import PessoaController
from controller.animais_controller import AnimalController

class TelaManejos:
    def __init__(self, master):
        self.controller = ManejoController()
        self.pessoa_ctrl = PessoaController()
        self.animal_ctrl = AnimalController()
        
        self.id_selecionado = None 
        
        self._timer_animais = None
        self._timer_pessoas = None
        
        self.master = master
        self.master.title("Gerenciar Manejos")
        self.master.geometry("900x650")

        tk.Label(self.master, text="Registro de Manejos e Procedimentos", font=("Arial", 14, "bold")).pack(pady=15)

        frame_form = tk.Frame(self.master)
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="Animal:").grid(row=0, column=0, padx=5, sticky="e")
        self.cb_brinco = ttk.Combobox(frame_form, width=47)
        self.cb_brinco.grid(row=0, column=1, pady=5, sticky="w")
        self.cb_brinco.bind("<KeyRelease>", self.agendar_filtro_animais)

        tk.Label(frame_form, text="Responsável:").grid(row=1, column=0, padx=5, sticky="e")
        self.cb_cpf = ttk.Combobox(frame_form, width=47)
        self.cb_cpf.grid(row=1, column=1, pady=5, sticky="w")
        self.cb_cpf.bind("<KeyRelease>", self.agendar_filtro_pessoas)
        self.cb_cpf.bind("<<ComboboxSelected>>", self.avaliar_regras_tela)

        tk.Label(frame_form, text="Data (DD/MM/YYYY):").grid(row=2, column=0, padx=5, sticky="e")
        self.ent_data = tk.Entry(frame_form, width=50)
        self.ent_data.grid(row=2, column=1, pady=5, sticky="w")

        tk.Label(frame_form, text="Tipo de Evento:").grid(row=3, column=0, padx=5, sticky="e")
        self.cb_evento = ttk.Combobox(frame_form, values=["Inseminação", "Diagnóstico", "Parto", "Aborto"], width=47, state="readonly")
        self.cb_evento.grid(row=3, column=1, pady=5, sticky="w")
        self.cb_evento.bind("<<ComboboxSelected>>", self.avaliar_regras_tela)

        self.lbl_diag = tk.Label(frame_form, text="Resultado Diagnóstico:")
        self.lbl_diag.grid(row=4, column=0, padx=5, sticky="e")
        self.cb_diag = ttk.Combobox(frame_form, values=["Positivo", "Negativo", "N/A"], width=47, state="readonly")
        self.cb_diag.grid(row=4, column=1, pady=5, sticky="w")

        tk.Label(frame_form, text="Observação:").grid(row=5, column=0, padx=5, sticky="e")
        self.ent_obs = tk.Entry(frame_form, width=50)
        self.ent_obs.grid(row=5, column=1, pady=5, sticky="w")

        # Botoes
        frame_btns = tk.Frame(self.master)
        frame_btns.pack(pady=15)
        tk.Button(frame_btns, text="Salvar Novo", width=12, bg="#017951", fg="white", command=self.acao_salvar).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Atualizar", width=12, bg="#f0ad4e", fg="white", command=self.acao_atualizar).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Remover", width=12, bg="#d9534f", fg="white", command=self.acao_remover).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Limpar", width=12, command=self.limpar_campos).pack(side="left", padx=5)

        # Tabela
        self.tree = ttk.Treeview(self.master, columns=("id", "brinco", "cpf", "data", "evento", "diagnostico", "obs"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("brinco", text="Brinco")
        self.tree.heading("cpf", text="CPF Resp.")
        self.tree.heading("data", text="Data")
        self.tree.heading("evento", text="Evento")
        self.tree.heading("diagnostico", text="Diagnóstico")
        self.tree.heading("obs", text="Observação")
        
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("brinco", width=70, anchor="center")
        self.tree.column("cpf", width=100, anchor="center")
        self.tree.column("data", width=90, anchor="center")
        self.tree.column("evento", width=130)
        self.tree.column("diagnostico", width=100, anchor="center")
        self.tree.column("obs", width=180)
        
        self.tree.pack(pady=10, fill="both", expand=True, padx=20)
        self.tree.bind("<<TreeviewSelect>>", self.preencher_formulario)

        self.carregar_listas_pesquisa()
        self.atualizar_tabela()
        
        self.avaliar_regras_tela()

    def carregar_listas_pesquisa(self):
        lista_pessoas = self.pessoa_ctrl.listar_pessoas()
        lista_animais = self.animal_ctrl.listar_animais()

        self.str_pessoas = []
        for p in lista_pessoas:
            cpf = getattr(p, 'cpf', '')
            nome = getattr(p, 'nome', '')
            tipo = p.__class__.__name__
            self.str_pessoas.append(f"{cpf} - {nome} ({tipo})")

        self.str_animais = []
        for a in lista_animais:
            brinco = getattr(a, 'brinco', '')
            raca_obj = getattr(a, 'raca', '')
            raca = raca_obj.value if hasattr(raca_obj, 'value') else raca_obj
            self.str_animais.append(f"{brinco} - {raca}")

        self.cb_cpf['values'] = self.str_pessoas
        self.cb_brinco['values'] = self.str_animais

    def agendar_filtro_pessoas(self, event):
        if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Return', 'Escape'):
            return

        if self._timer_pessoas is not None:
            self.master.after_cancel(self._timer_pessoas)
        
        self._timer_pessoas = self.master.after(400, self.executar_filtro_pessoas)

    def executar_filtro_pessoas(self):
        digitado = self.cb_cpf.get()
        
        if digitado.strip() == "":
            self.cb_cpf['values'] = self.str_pessoas
            self.cb_cpf.event_generate('<Escape>')
        else:
            filtrado = [p for p in self.str_pessoas if digitado.lower() in p.lower()]
            self.cb_cpf['values'] = filtrado
            self.cb_cpf.tk.call('ttk::combobox::Post', self.cb_cpf)
            
        self.cb_cpf.set(digitado)
        self.cb_cpf.icursor(tk.END)
        self.avaliar_regras_tela()

    def agendar_filtro_animais(self, event):
        if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Return', 'Escape'):
            return

        if self._timer_animais is not None:
            self.master.after_cancel(self._timer_animais)
        
        self._timer_animais = self.master.after(400, self.executar_filtro_animais)

    def executar_filtro_animais(self):
        digitado = self.cb_brinco.get()
        
        if digitado.strip() == "":
            self.cb_brinco['values'] = self.str_animais
            self.cb_brinco.event_generate('<Escape>')
        else:
            filtrado = [a for a in self.str_animais if digitado.lower() in a.lower()]
            self.cb_brinco['values'] = filtrado
            self.cb_brinco.tk.call('ttk::combobox::Post', self.cb_brinco)
            
        self.cb_brinco.set(digitado)
        self.cb_brinco.icursor(tk.END)

    def avaliar_regras_tela(self, event=None):
        selecao_pessoa = self.cb_cpf.get()
        selecao_evento = self.cb_evento.get()
        
        eventos_completos = ["Inseminação", "Diagnóstico", "Parto", "Aborto"]
        eventos_restritos = ["Inseminação", "Parto", "Aborto"]

        is_proprietario = "(Proprietario)" in selecao_pessoa

        if is_proprietario:
            self.cb_evento['values'] = eventos_restritos
            if selecao_evento == "Diagnóstico":
                self.cb_evento.set("")
                selecao_evento = "" 
        else:
            self.cb_evento['values'] = eventos_completos

        if not is_proprietario and selecao_evento == "Diagnóstico":
            self.lbl_diag.config(state="normal")
            self.cb_diag.config(state="readonly")
        else:
            self.lbl_diag.config(state="disabled")
            self.cb_diag.config(state="normal") 
            self.cb_diag.set("")
            self.cb_diag.config(state="disabled")

    def limpar_campos(self):
        if self._timer_animais:
            self.master.after_cancel(self._timer_animais)
            self._timer_animais = None
        if self._timer_pessoas:
            self.master.after_cancel(self._timer_pessoas)
            self._timer_pessoas = None
            
        self.id_selecionado = None
        
        self.cb_brinco.set("")
        self.cb_cpf.set("")
        self.ent_data.delete(0, tk.END)
        self.cb_evento.set("")
        self.ent_obs.delete(0, tk.END)
        
        # Reseta as opções e recarrega as listas
        self.cb_evento['values'] = ["Inseminação", "Diagnóstico", "Parto", "Aborto"]
        self.carregar_listas_pesquisa() 
        
        self.avaliar_regras_tela()

    def preencher_formulario(self, event):
        selecionado = self.tree.selection()
        if not selecionado:
            return
            
        valores = self.tree.item(selecionado[0], "values")
        id_m, brinco, cpf, data, evento, diag, obs = valores
        
        self.limpar_campos()
        self.id_selecionado = int(id_m) 
        
        for p in self.str_pessoas:
            if p.startswith(str(cpf)):
                self.cb_cpf.set(p)
                break
        
        for a in self.str_animais:
            if a.startswith(str(brinco)):
                self.cb_brinco.set(a)
                break
                
        self.ent_data.insert(0, data)
        self.cb_evento.set(evento)
        
        self.avaliar_regras_tela()
        
        if str(self.cb_diag.cget('state')) != 'disabled':
            self.cb_diag.set(diag if diag not in ("N/A", "None", "") else "")
            
        self.ent_obs.insert(0, obs if obs != "None" else "")

    def atualizar_tabela(self):
        self.tree.delete(*self.tree.get_children())
        lista_manejos = self.controller.listar_manejos()

        if not lista_manejos:
            return

        for m in lista_manejos:
            id_m = getattr(m, 'id_manejo', '')
            brinco = getattr(m, 'brinco_animal', '')
            cpf = getattr(m, 'cpf_responsavel', '')
            
            data_cru = getattr(m, 'data_evento', '')
            if hasattr(data_cru, 'strftime'):
                data = data_cru.strftime('%d/%m/%Y')
            else:
                data = data_cru
                
            evento = getattr(m, 'tipo_evento', '')
            diag = getattr(m, 'resultado_diagnostico', '') or 'N/A'
            obs = getattr(m, 'observacao', '') or ''

            self.tree.insert("", tk.END, values=(id_m, brinco, cpf, data, evento, diag, obs))

    def extrair_dados_form(self):
        brinco_texto = self.cb_brinco.get().split(" - ")[0].strip()
        cpf_texto = self.cb_cpf.get().split(" - ")[0].strip()
        tipo_resp = "Proprietario" if "(Proprietario)" in self.cb_cpf.get() else "Veterinario"
        return brinco_texto, cpf_texto, tipo_resp

    def acao_salvar(self):
        brinco_str, cpf, tipo_resp = self.extrair_dados_form()
        data = self.ent_data.get().strip().replace('/', '-')
        evento = self.cb_evento.get().strip()
        diag = self.cb_diag.get().strip()
        obs = self.ent_obs.get().strip()

        try:
            brinco_int = int(brinco_str)
        except ValueError:
            messagebox.showwarning("Aviso", "Por favor, pesquise e selecione um animal válido na lista!")
            return

        sucesso, msg = self.controller.salvar_manejo(brinco_int, cpf, data, tipo_resp, evento, diag, obs)

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self.atualizar_tabela() 
        else:
            messagebox.showwarning("Erro", msg)

    def acao_atualizar(self):
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Clique em um manejo na tabela antes de atualizar!")
            return

        brinco_str, cpf, tipo_resp = self.extrair_dados_form()
        data = self.ent_data.get().strip().replace('/', '-')
        evento = self.cb_evento.get().strip()
        diag = self.cb_diag.get().strip()
        obs = self.ent_obs.get().strip()

        try:
            brinco_int = int(brinco_str)
        except ValueError:
            messagebox.showwarning("Aviso", "Por favor, pesquise e selecione um animal válido na lista!")
            return

        sucesso, msg = self.controller.atualizar_manejo(self.id_selecionado, brinco_int, cpf, data, tipo_resp, evento, diag, obs)
        
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self.atualizar_tabela()
        else:
            messagebox.showerror("Erro", msg)

    def acao_remover(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um manejo na tabela clicando nele primeiro!")
            return
            
        valores = self.tree.item(selecionado[0], "values")
        id_m = int(valores[0])

        resposta = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja remover o manejo de ID {id_m}?")
        if resposta:
            sucesso, msg = self.controller.remover_manejo(id_m)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.limpar_campos()
                self.atualizar_tabela()
            else:
                messagebox.showerror("Erro", msg)