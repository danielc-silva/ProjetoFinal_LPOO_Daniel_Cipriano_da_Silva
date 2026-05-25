from abc import ABC, abstractmethod
from datetime import date, datetime
from model.raca import Raca

class Animal(ABC):
    def __init__(self, brinco, raca, data_nascimento, peso, lote=None):
        self.brinco = brinco
        self.raca = raca
        self.data_nascimento = data_nascimento
        self.peso = peso
        self.lote = lote

    @property
    def brinco(self):
        return self.__brinco
    
    @brinco.setter
    def brinco(self, valor):
        if valor > 0:
            self.__brinco = valor
        else:
            raise ValueError("O brinco deve ser um valor positivo.")
    
    @property
    def raca(self):
        return self.__raca
    
    @raca.setter
    def raca(self, valor):
        if isinstance(valor, Raca):
            self.__raca = valor
        else:
            raise ValueError("Raça inválida. Escolha uma opção válida do sistema.")
        
    @property
    def data_nascimento(self):
        return self.__data_nascimento
    
    @data_nascimento.setter
    def data_nascimento(self, data_recebida):
        data_convertida = self.valida_data(data_recebida)
        
        if data_convertida:
            if data_convertida > date.today():
                raise ValueError("A data de nascimento não pode ser futura.")
            self.__data_nascimento = data_convertida
        else:
            self.__data_nascimento = None

    @property
    def peso(self):
        return self.__peso
    
    @peso.setter
    def peso(self, valor):
        if valor > 0:
            self.__peso = valor
        else:
            raise ValueError("O peso deve ser um valor positivo.")

    def transferir_lote(self, novo_lote):
        self.lote = novo_lote
        
    def atualizar_peso(self, novo_peso):
        self.peso = novo_peso

    def valida_data(self, data_recebida):
        if data_recebida is None:
            return None
        if isinstance(data_recebida, date):
            return data_recebida
        try:
            temporario = datetime.strptime(data_recebida, "%d-%m-%Y")
            return temporario.date()
        except ValueError:
            raise ValueError(f"ERRO: Data '{data_recebida}' em formato inválido. Use DD-MM-YYYY.")


class Macho(Animal):
    def __init__(self, brinco, raca, data_nascimento, peso, lote=None, castrado=False):
        super().__init__(brinco, raca, data_nascimento, peso, lote)
        self.castrado = castrado


class Femea(Animal):
    def __init__(self, brinco, raca, data_nascimento, peso, lote=None):
        super().__init__(brinco, raca, data_nascimento, peso, lote)
        self.estado_reprodutivo = "Vazia" 
        self.data_ultima_inseminacao = None

    def inseminar(self, data):
        pass
        
    def confirmar_prenhez(self):
        pass