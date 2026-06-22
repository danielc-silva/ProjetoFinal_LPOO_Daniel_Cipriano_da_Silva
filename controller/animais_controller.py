import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.animal_factory import AnimalFactory
from dao.animal_dao import AnimalDAO
from model.raca import Raca

class AnimalController:
    def __init__(self):
        self.animal_dao = AnimalDAO()

    def salvar_animal(self, brinco_str: str, raca_str: str, nasc_str: str, tipo_str: str, estado_str: str, castrado_str: str):
        if not brinco_str or not raca_str or not nasc_str:
            return False, "Os campos Brinco, Raça e Nascimento são obrigatórios!"

        try:
            brinco_int = int(brinco_str)
        except ValueError:
            return False, "O campo Brinco deve ser um número inteiro!"

        try:
            raca_enum = Raca(raca_str.lower())

            if tipo_str == "Femea":
                novo_animal = AnimalFactory.criar_animal(
                    tipo_animal="Femea", 
                    brinco=brinco_int,
                    raca=raca_enum,
                    data_nascimento=nasc_str,
                    estado_reprodutivo=estado_str
                )
            elif tipo_str == "Macho":
                is_castrado_bool = True if castrado_str == "Sim" else False
                
                novo_animal = AnimalFactory.criar_animal(
                    tipo_animal="Macho", 
                    brinco=brinco_int,
                    raca=raca_enum,
                    data_nascimento=nasc_str, 
                    is_castrado=is_castrado_bool
                )
            else:
                return False, "Erro: O tipo de animal selecionado é inválido!"

            self.animal_dao.salvar(novo_animal)
            return True, f"Animal salvo com sucesso!"

        except ValueError as e:
            return False, str(e) 
        except Exception as e:
            return False, f"Falha ao salvar no banco de dados: {e}"

    def atualizar_animal(self, brinco_str: str, raca_str: str, nasc_str: str, tipo_str: str, estado_str: str, castrado_str: str):
        if not brinco_str or not raca_str or not nasc_str:
            return False, "Os campos Brinco, Raça e Nascimento são obrigatórios!"

        if tipo_str == "Femea" and not estado_str:
            return False, "Para Fêmeas, o Estado Reprodutivo é obrigatório!"
        
        if tipo_str == "Macho" and not castrado_str:
            return False, "Para Machos, informar se é Castrado é obrigatório!"

        try:
            brinco_int = int(brinco_str)
        except ValueError:
            return False, "O campo Brinco deve ser um número inteiro!"

        try:
            raca_enum = Raca(raca_str.lower())

            if tipo_str == "Femea":
                animal_editado = AnimalFactory.criar_animal(
                    tipo_animal="Femea", 
                    brinco=brinco_int, 
                    raca=raca_enum,
                    data_nascimento=nasc_str,
                    estado_reprodutivo=estado_str
                )
            elif tipo_str == "Macho":
                is_castrado_bool = True if castrado_str == "Sim" else False
                
                animal_editado = AnimalFactory.criar_animal(
                    tipo_animal="Macho", 
                    brinco=brinco_int, 
                    raca=raca_enum,
                    data_nascimento=nasc_str, 
                    is_castrado=is_castrado_bool
                )
            else:
                return False, "Erro: Selecione se o animal é Macho ou Fêmea!"

            sucesso, msg = self.animal_dao.atualizar(animal_editado)
            return sucesso, msg

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Falha ao processar atualização: {e}"
        

    def listar_animais(self):
        try:
            return self.animal_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar animais: {e}")
            return []
            
    def remover_animal(self, brinco_str: str):
        if not brinco_str:
            return False, "Brinco não informado para remoção."
        try:
            brinco_int = int(brinco_str.strip())
            sucesso, msg = self.animal_dao.remover(brinco_int)
            return sucesso, msg
            
        except ValueError:
            return False, "Formato do Brinco inválido para remoção."
        except Exception as e:
            return False, f"Erro ao remover: {e}"