import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.manejo import Manejo
from dao.db_config import DatabaseConfig

class ManejosDAO:
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def salvar(self, obj_manejo):
        if not self.conexao:
            return False, "Sem conexão com o Banco de Dados"
        
        try:
            cursor = self.conexao.cursor()

            query = """
                INSERT INTO tb_manejos (brinco_animal, cpf_responsavel, data_evento, tipo_evento, resultado_diagnostico, observacao)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (
                obj_manejo.brinco_animal, 
                obj_manejo.cpf_responsavel, 
                obj_manejo.data_evento, 
                obj_manejo.tipo_evento, 
                obj_manejo.resultado_diagnostico, 
                obj_manejo.observacao
            )
            
            cursor.execute(query, valores)
            self.conexao.commit()
            return True, "Manejo registrado com sucesso!"
            
        except Exception as e:
            self.conexao.rollback()

            if "foreign key constraint" in str(e).lower() or "violates foreign key" in str(e).lower():
                return False, "Erro: O CPF do responsável ou o Brinco do animal não estão cadastrados no sistema."
            
            return False, f"Erro ao salvar manejo no banco: {e}"
            
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, obj_manejo):
        if not self.conexao:
            return False, "Sem conexão com o Banco de Dados"
        
        try:
            cursor = self.conexao.cursor()
            query = """
                UPDATE tb_manejos
                SET brinco_animal = %s, 
                    cpf_responsavel = %s, 
                    data_evento = %s, 
                    tipo_evento = %s, 
                    resultado_diagnostico = %s, 
                    observacao = %s
                WHERE id_manejo = %s
            """
            valores = (
                obj_manejo.brinco_animal,
                obj_manejo.cpf_responsavel,
                obj_manejo.data_evento,
                obj_manejo.tipo_evento,
                obj_manejo.resultado_diagnostico,
                obj_manejo.observacao,
                obj_manejo.id_manejo
            )
            cursor.execute(query, valores)
            self.conexao.commit()
            
            if cursor.rowcount > 0:
                return True, f"Manejo atualizado com sucesso!"
            else:
                return False, "Manejo não encontrado no banco de dados para atualização."
                
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar manejo: {e}"
            
        finally:
            if cursor:
                cursor.close()

    def remover(self, id_manejo):
        if not self.conexao:
            return False, "Sem conexão com o banco."
            
        try:
            cursor = self.conexao.cursor()
            # fazemos o delete utilizando a chave primaria gerada automaticamente pelo BD
            query = "DELETE FROM tb_manejos WHERE id_manejo = %s"
            
            cursor.execute(query, (id_manejo,))
            self.conexao.commit()
            
            if cursor.rowcount > 0:
                return True, "Manejo removido com sucesso!"
            else:
                return False, "Manejo não encontrado no banco de dados."
                
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover manejo: {e}"
            
        finally:
            if cursor:
                cursor.close()

    def listar_todos(self):
        if not self.conexao:
            return []
                
        try:
            cursor = self.conexao.cursor()
            query = "SELECT id_manejo, brinco_animal, cpf_responsavel, data_evento, tipo_evento, resultado_diagnostico, observacao FROM tb_manejos"
            
            cursor.execute(query) 
            linhas = cursor.fetchall()
            manejos = []
            
            for linha in linhas:
                obj = Manejo(
                    id_manejo=linha[0],
                    brinco_animal=linha[1],
                    cpf_responsavel=linha[2],
                    data_evento=linha[3],
                    tipo_evento=linha[4],
                    resultado_diagnostico=linha[5],
                    observacao=linha[6]
                )
                manejos.append(obj)
                
            return manejos
            
        except Exception as e:
            print(f"Erro ao buscar manejos: {e}")
            return []
            
        finally:
            if cursor:
                cursor.close()