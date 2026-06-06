import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.proprietario import Proprietario
from model.veterinario import Veterinario
from model.pessoa_factory import PessoaFactory
from dao.db_config import DatabaseConfig

class PessoaDAO:
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def salvar(self, pessoa):
        if not self.conexao:
            raise Exception("Sem conexão com o Banco de Dados")
        
        try:
            cursor = self.conexao.cursor()
            
            tipo_pessoa = pessoa.__class__.__name__
            
            if isinstance(pessoa, Proprietario):
                inscricao_estadual = pessoa.inscricao_estadual
                nome_fazenda = pessoa.nome_fazenda
                crmv = None
            elif isinstance(pessoa, Veterinario):
                inscricao_estadual = None
                nome_fazenda = None
                crmv = pessoa.crmv
            else:
                raise ValueError("Tipo de pessoa desconhecido.")

            query = """
                INSERT INTO pessoas (cpf, nome, telefone, tipo_pessoa, inscricao_estadual, nome_fazenda, crmv) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """            
            valores = (
                pessoa.cpf, 
                pessoa.nome, 
                pessoa.telefone, 
                tipo_pessoa, 
                inscricao_estadual, 
                nome_fazenda, 
                crmv
            )
            
            cursor.execute(query, valores)            
            self.conexao.commit()
            return True, "Pessoa cadastrada com sucesso!"

        except Exception as e:
            print(f"Erro ao inserir pessoa com CPF ({pessoa.cpf}): {e}")
            self.conexao.rollback()
            return False, str(e)
        
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, pessoa):
        if not self.conexao:
            return False, "Sem conexão com o Banco de Dados"
        
        try:
            cursor = self.conexao.cursor()
            
            tipo_pessoa = pessoa.__class__.__name__
            
            if isinstance(pessoa, Proprietario):
                inscricao_estadual = pessoa.inscricao_estadual
                nome_fazenda = pessoa.nome_fazenda
                crmv = None
            elif isinstance(pessoa, Veterinario):
                inscricao_estadual = None
                nome_fazenda = None
                crmv = pessoa.crmv
            else:
                raise ValueError("Tipo de pessoa desconhecido.")

            query = """
                UPDATE pessoas
                SET nome = %s, 
                    telefone = %s,
                    tipo_pessoa = %s, 
                    inscricao_estadual = %s,
                    nome_fazenda = %s,
                    crmv = %s
                WHERE cpf = %s
            """
            
            valores = (
                pessoa.nome,
                pessoa.telefone,
                tipo_pessoa, 
                inscricao_estadual,
                nome_fazenda,
                crmv,
                pessoa.cpf 
            )
            
            cursor.execute(query, valores)
            self.conexao.commit()
            
            if cursor.rowcount > 0:
                return True, f"Pessoa de CPF {pessoa.cpf} atualizada com sucesso!"
            else:
                return False, "Pessoa não encontrada no banco de dados para atualização."

        except Exception as e:
            print(f"Erro ao atualizar pessoa de CPF ({pessoa.cpf}): {e}")
            self.conexao.rollback()
            return False, f"Erro ao atualizar: {e}"
        
        finally:
            if cursor:
                cursor.close()

    def remover(self, cpf):
        if not self.conexao:
            return False, "Sem conexão com o banco."
            
        try:
            cursor = self.conexao.cursor()

            query = "DELETE FROM pessoas WHERE cpf = %s"
            
            cursor.execute(query, (cpf,))
            self.conexao.commit()
            
            if cursor.rowcount > 0:
                return True, f"Pessoa com CPF {cpf} removida com sucesso!"
            else:
                return False, "Pessoa não encontrada no banco de dados."

        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover: {e}"
            
        finally:
            if cursor:
                cursor.close()

    def listar_todos(self):
        if not self.conexao:
            return []
                
        try:
            cursor = self.conexao.cursor()
            query = "SELECT cpf, nome, telefone, tipo_pessoa, inscricao_estadual, nome_fazenda, crmv FROM pessoas"
            
            cursor.execute(query) 
            linhas = cursor.fetchall()
            pessoas = []
            
            for linha in linhas:
                obj = PessoaFactory.criar_pessoa(
                    tipo_pessoa=linha[3],
                    cpf=linha[0], 
                    nome=linha[1], 
                    telefone=linha[2],
                    inscricao_estadual=linha[4],
                    nome_fazenda=linha[5],
                    crmv=linha[6]
                )
                pessoas.append(obj)
            
            return pessoas

        except Exception as e:
            print(f"Erro ao buscar pessoas: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()

    def buscar_por_cpf(self, cpf):
        if not self.conexao:
            return None
                
        try:
            cursor = self.conexao.cursor()
            query = "SELECT cpf, nome, telefone, tipo_pessoa, inscricao_estadual, nome_fazenda, crmv FROM pessoas WHERE cpf = %s"
            
            cursor.execute(query, (cpf,))
            linha = cursor.fetchone() 
            
            if linha:
                pessoa_encontrada = PessoaFactory.criar_pessoa(
                    tipo_pessoa=linha[3],
                    cpf=linha[0], 
                    nome=linha[1], 
                    telefone=linha[2],
                    inscricao_estadual=linha[4],
                    nome_fazenda=linha[5],
                    crmv=linha[6]
                )
                return pessoa_encontrada
            else:
                return None

        except Exception as e:
            print(f"Erro ao buscar pessoa por CPF no BD: {e}")
            return None
        
        finally:
            if cursor:
                cursor.close()