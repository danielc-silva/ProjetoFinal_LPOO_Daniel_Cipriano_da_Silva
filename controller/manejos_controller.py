from model.manejo import Manejo
from dao.manejos_dao import ManejosDAO
from dao.animal_dao import AnimalDAO

class ManejoController:
    def __init__(self):
        self.manejo_dao = ManejosDAO()
        self.animal_dao = AnimalDAO()

    def _atualizar_estado_matriz(self, brinco: int, evento: str, diagnostico: str):
        animal = self.animal_dao.buscar_por_brinco(brinco)
        
        if not animal or animal.__class__.__name__ != "Femea":
            return

        novo_estado = None
        
        if evento == "Inseminação":
            novo_estado = "Inseminada"
        elif evento == "Diagnóstico":
            if diagnostico == "Positivo":
                novo_estado = "Prenha"
            elif diagnostico == "Negativo":
                novo_estado = "Vazia"
        elif evento in ["Parto", "Aborto"]:
            novo_estado = "Vazia"

        if novo_estado and getattr(animal, 'estado_reprodutivo', '') != novo_estado:
            animal.estado_reprodutivo = novo_estado
            self.animal_dao.atualizar(animal)

    def salvar_manejo(self, brinco_int: int, cpf_str: str, data_str: str, tipo_resp: str, evento_str: str, diag_str: str, obs_str: str):
        if not brinco_int or not cpf_str or not data_str or not evento_str:
            return False, "Os campos Brinco, CPF, Data e Tipo de Evento são obrigatórios!"

        animal = self.animal_dao.buscar_por_brinco(brinco_int)
        if not animal:
            return False, "Animal não encontrado no banco de dados."
            
        if animal.__class__.__name__ == "Femea":
            estado_atual = getattr(animal, 'estado_reprodutivo', '')
            
            if evento_str == "Inseminação" and estado_atual in ["Inseminada", "Prenha"]:
                return False, f"Ação bloqueada: Esta matriz já consta como '{estado_atual}'."
                
            if evento_str == "Diagnóstico" and estado_atual == "Vazia":
                return False, "Ação bloqueada: Não é possível diagnosticar uma matriz 'Vazia' sem inseminação prévia."

        if tipo_resp == "Proprietario" or evento_str != "Diagnóstico":
            diag_str = None
        elif diag_str == "":
            diag_str = None

        try:
            novo_manejo = Manejo(
                id_manejo=None, 
                brinco_animal=brinco_int,
                cpf_responsavel=cpf_str,
                data_evento=data_str,
                tipo_evento=evento_str,
                resultado_diagnostico=diag_str,
                observacao=obs_str
            )

            sucesso, msg = self.manejo_dao.salvar(novo_manejo)
            
            if sucesso:
                self._atualizar_estado_matriz(brinco_int, evento_str, diag_str)
                
            return sucesso, msg

        except Exception as e:
            return False, f"Falha ao processar salvamento do manejo: {e}"

    def atualizar_manejo(self, id_manejo: int, brinco_int: int, cpf_str: str, data_str: str, tipo_resp: str, evento_str: str, diag_str: str, obs_str: str):
        if not id_manejo:
            return False, "ID do manejo não identificado para atualização!"
            
        if not brinco_int or not cpf_str or not data_str or not evento_str:
            return False, "Os campos Brinco, CPF, Data e Tipo de Evento são obrigatórios!"

        if tipo_resp == "Proprietario" or evento_str != "Diagnóstico":
            diag_str = None
        elif diag_str == "":
            diag_str = None

        try:
            manejo_editado = Manejo(
                id_manejo=id_manejo, 
                brinco_animal=brinco_int,
                cpf_responsavel=cpf_str,
                data_evento=data_str,
                tipo_evento=evento_str,
                resultado_diagnostico=diag_str,
                observacao=obs_str
            )

            sucesso, msg = self.manejo_dao.atualizar(manejo_editado)
            
            if sucesso:
                self._atualizar_estado_matriz(brinco_int, evento_str, diag_str)
                
            return sucesso, msg

        except Exception as e:
            return False, f"Falha ao processar atualização do manejo: {e}"

    def listar_manejos(self):
        try:
            return self.manejo_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar manejos: {e}")
            return []

    def remover_manejo(self, id_manejo: int):
        if not id_manejo:
            return False, "ID do manejo não informado."
        try:
            return self.manejo_dao.remover(id_manejo)
        except Exception as e:
            return False, f"Erro ao remover manejo: {e}"