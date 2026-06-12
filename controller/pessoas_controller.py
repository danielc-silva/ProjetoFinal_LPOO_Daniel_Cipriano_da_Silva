import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.pessoa_factory import PessoaFactory
from dao.pessoa_dao import PessoaDAO

class PessoaController:
    def __init__(self):
        self.pessoa_dao = PessoaDAO()

    def salvar_pessoa(self, nome_str: str, cpf_str: str, tipo_str: str, inscricao_str: str, fazenda_str: str, crmv_str: str):
        if not nome_str or not cpf_str:
            return False, "Os campos Nome e CPF são obrigatórios!"

        if tipo_str == "Veterinario" and not crmv_str:
            return False, "Para Veterinários, o CRMV é obrigatório!"

        try:
            if tipo_str == "Proprietario":
                nova_pessoa = PessoaFactory.criar_pessoa(
                    tipo_pessoa="Proprietario", 
                    nome=nome_str, 
                    cpf=cpf_str,
                    inscricao_estadual=inscricao_str,
                    nome_fazenda=fazenda_str
                )
            elif tipo_str == "Veterinario":
                nova_pessoa = PessoaFactory.criar_pessoa(
                    tipo_pessoa="Veterinario", 
                    nome=nome_str, 
                    cpf=cpf_str, 
                    crmv=crmv_str
                )
            else:
                return False, "Erro: O tipo de pessoa selecionado é inválido!"

            self.pessoa_dao.salvar(nova_pessoa)
            return True, f"{tipo_str} salvo com sucesso!"

        except Exception as e:
            return False, f"Falha ao salvar no banco de dados: {e}"

    def atualizar_pessoa(self, nome_str: str, cpf_str: str, tipo_str: str, inscricao_str: str, fazenda_str: str, crmv_str: str):
        if not nome_str or not cpf_str:
            return False, "Os campos Nome e CPF são obrigatórios!"

        if tipo_str == "Veterinario" and not crmv_str:
            return False, "Para Veterinários, o CRMV é obrigatório!"

        try:
            if tipo_str == "Proprietario":
                pessoa_editada = PessoaFactory.criar_pessoa(
                    tipo_pessoa="Proprietario", 
                    nome=nome_str, 
                    cpf=cpf_str,
                    inscricao_estadual=inscricao_str,
                    nome_fazenda=fazenda_str
                )
            elif tipo_str == "Veterinario": # <-- AGORA É ELIF
                pessoa_editada = PessoaFactory.criar_pessoa(
                    tipo_pessoa="Veterinario", 
                    nome=nome_str, 
                    cpf=cpf_str, 
                    crmv=crmv_str
                )
            else:
                return False, "Erro: Selecione se a pessoa é Proprietário ou Veterinário!"

            sucesso, msg = self.pessoa_dao.atualizar(pessoa_editada)
            return sucesso, msg

        except Exception as e:
            return False, f"Falha ao processar atualização: {e}"

    def listar_pessoas(self):
        try:
            return self.pessoa_dao.listar_todas()
        except Exception as e:
            print(f"Erro ao listar pessoas: {e}")
            return []
            
    def remover_pessoa(self, cpf_str: str):
        if not cpf_str:
            return False, "CPF não informado para remoção."
        try:
            sucesso, msg = self.pessoa_dao.remover(cpf_str.strip())
            return sucesso, msg
        except Exception as e:
            return False, f"Erro ao remover: {e}"