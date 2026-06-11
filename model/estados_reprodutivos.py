from abc import ABC, abstractmethod

# class abstrar, as regrass gerais
class EstadoReprodutivo(ABC):
    @property
    @abstractmethod
    # obrigo todos os estados a ter um nome, só pra nao usar o __class__.___name__
    def nome(self):
        pass

    def registrar_inseminacao(self, femea):
        raise Exception(f"Operação inválida: Não é possível inseminar uma matriz que está {self.nome}.")

    def registrar_diagnostico(self, femea, positivo):
        raise Exception(f"Operação inválida: Diagnóstico de gestação não aplicável para matriz {self.nome}.")

    def registrar_parto(self, femea):
        raise Exception(f"Operação inválida: Não é possível registrar parto para matriz {self.nome}.")

    def registrar_aborto(self, femea):
        raise Exception(f"Operação inválida: Não é possível registrar aborto para matriz {self.nome}.")



class EstadoVazia(EstadoReprodutivo):
    @property
    def nome(self):
        return "Vazia"

    def registrar_inseminacao(self, femea):
        # Muda o estado da fêmea para Inseminada
        femea.mudar_estado(EstadoInseminada())
        return "Inseminação registrada. A matriz agora está Inseminada."

class EstadoInseminada(EstadoReprodutivo):
    @property
    def nome(self):
        return "Inseminada"

    def registrar_diagnostico(self, femea, positivo):
        if positivo:
            femea.mudar_estado(EstadoPrenha())
            return "Diagnóstico Positivo! A matriz agora está Prenha."
        else:
            femea.mudar_estado(EstadoVazia())
            return "Diagnóstico Negativo. A matriz retornou para o estado Vazia."

class EstadoPrenha(EstadoReprodutivo):
    @property
    def nome(self):
        return "Prenha"

    def registrar_parto(self, femea):
        femea.mudar_estado(EstadoVazia())
        return "Parto registrado com sucesso. A matriz retornou para o estado Vazia."

    def registrar_aborto(self, femea):
        femea.mudar_estado(EstadoVazia())
        return "Aborto registrado. A matriz retornou para o estado Vazia."