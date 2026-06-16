import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.femea import Femea
from model.macho import Macho
from model.animal_factory import AnimalFactory
from dao.db_config import DatabaseConfig
from model.raca import Raca

class AnimalDAO:
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def salvar(self, obj_animal):
        if not self.conexao:
            raise Exception("Sem conexão com o Banco de Dados")
        
        try:
            cursor = self.conexao.cursor()
            
            tipo_animal = obj_animal.__class__.__name__
            
            if isinstance(obj_animal, Femea):
                is_castrado = None
                estado_reprodutivo = obj_animal.estado_reprodutivo
            elif isinstance(obj_animal, Macho):
                is_castrado = obj_animal.castrado
                estado_reprodutivo = None
            else:
                raise ValueError("Tipo de animal desconhecido.")

            query = """
                INSERT INTO tb_animais (brinco, raca, data_nascimento, tipo_animal, is_castrado, estado_reprodutivo) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """            
            valores = (
                obj_animal.brinco, 
                obj_animal.raca.value, 
                obj_animal.data_nascimento, 
                tipo_animal, 
                is_castrado, 
                estado_reprodutivo
            )
            
            cursor.execute(query, valores)            
            self.conexao.commit()
            return True, "Animal cadastrado com sucesso"

        except Exception as e:
            print(f"Erro ao inserir animal com brinco ({obj_animal.brinco}): {e}")
            self.conexao.rollback()
            return False, str(e)
        
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, obj_animal):
        if not self.conexao:
            return False, "Sem conexão com o Banco de Dados"
        
        try:
            cursor = self.conexao.cursor()
            
            tipo_animal = obj_animal.__class__.__name__
            
            if isinstance(obj_animal, Femea):
                is_castrado = None
                estado_reprodutivo = obj_animal.estado_reprodutivo
            elif isinstance(obj_animal, Macho):
                is_castrado = obj_animal.castrado
                estado_reprodutivo = None
            else:
                raise ValueError("Tipo de animal desconhecido.")

            query = """
                UPDATE tb_animais
                SET raca = %s, 
                    data_nascimento = %s,
                    tipo_animal = %s, 
                    is_castrado = %s,
                    estado_reprodutivo = %s
                WHERE brinco = %s
            """
            
            valores = (
                obj_animal.raca.value,
                obj_animal.data_nascimento,
                tipo_animal, 
                is_castrado,
                estado_reprodutivo,
                obj_animal.brinco 
            )
            
            cursor.execute(query, valores)
            self.conexao.commit()
            
            if cursor.rowcount > 0:
                return True, f"Animal de brinco {obj_animal.brinco} atualizado com sucesso!"
            else:
                return False, "Animal não encontrado no banco de dados para atualização."

        except Exception as e:
            print(f"Erro ao atualizar animal de brinco ({obj_animal.brinco}): {e}")
            self.conexao.rollback()
            return False, f"Erro ao atualizar: {e}"
        
        finally:
            if cursor:
                cursor.close()

    def remover(self, brinco):
        if not self.conexao:
            return False, "Sem conexão com o banco."
            
        try:
            cursor = self.conexao.cursor()
            query = "DELETE FROM tb_animais WHERE brinco = %s"
            
            cursor.execute(query, (brinco,))
            self.conexao.commit()
            
            if cursor.rowcount > 0:
                return True, f"Animal com brinco {brinco} removido com sucesso!"
            else:
                return False, "Animal não encontrado no banco de dados."

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
            query = "SELECT brinco, raca, data_nascimento, tipo_animal, is_castrado, estado_reprodutivo FROM tb_animais"
            
            cursor.execute(query) 
            linhas = cursor.fetchall()
            animais = []
            
            for linha in linhas:
                try:
                    raca_enum = Raca(linha[1])
                except ValueError:
                    raca_enum = Raca[linha[1].upper()]

                brinco_banco = int(linha[0])

                obj = AnimalFactory.criar_animal(
                    brinco=brinco_banco,
                    raca=raca_enum,
                    data_nascimento=linha[2],
                    tipo_animal=linha[3],
                    is_castrado=linha[4], 
                    estado_reprodutivo=linha[5]
                )
                animais.append(obj)
            
            return animais

        except Exception as e:
            print(f"Erro ao buscar animais: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()

    def buscar_por_brinco(self, brinco):
        if not self.conexao:
            return None
                
        try:
            cursor = self.conexao.cursor()
            query = "SELECT brinco, raca, data_nascimento, tipo_animal, is_castrado, estado_reprodutivo FROM tb_animais WHERE brinco = %s"
            
            cursor.execute(query, (brinco,))
            linha = cursor.fetchone() 
            
            if linha:
                try:
                    raca_enum = Raca(linha[1])
                except ValueError:
                    raca_enum = Raca[linha[1].upper()]

                animal_encontrado = AnimalFactory.criar_animal(
                    tipo_animal=linha[3],
                    brinco=int(linha[0]),
                    raca=raca_enum, 
                    data_nascimento=linha[2],
                    is_castrado=linha[4],
                    estado_reprodutivo=linha[5]
                )
                
                return animal_encontrado
            else:
                return None

        except Exception as e:
            print(f"Erro ao buscar animal por brinco no BD: {e}")
            return None
        
        finally:
            if cursor:
                cursor.close()