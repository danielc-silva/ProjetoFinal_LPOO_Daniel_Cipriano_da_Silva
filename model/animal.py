from abc import ABC, abstractmethod
from datetime import date, datetime
from model.raca import Raca

class Animal(ABC):
    def __init__(self, brinco, raca, data_nascimento):
        self.brinco = brinco
        self.raca = raca
        self.data_nascimento = data_nascimento

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

    def valida_data(self, data_recebida):
        if data_recebida is None:
            return None
        if isinstance(data_recebida, date):
            return data_recebida
        try:
            data_limpa = data_recebida.replace('/', '-')
            temporario = datetime.strptime(data_limpa, "%d-%m-%Y")
            return temporario.date()
        except ValueError:
            raise ValueError(f"ERRO: Data '{data_recebida}' inválida. Use DD/MM/YYYY.")