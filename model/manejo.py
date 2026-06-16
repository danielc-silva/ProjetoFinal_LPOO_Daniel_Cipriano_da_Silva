from datetime import date, datetime

from model.macho import Macho
from model.femea import Femea
from model.proprietario import Proprietario
from model.veterinario import Veterinario

class Manejo:
    def __init__(self, brinco_animal, cpf_responsavel, data_evento, tipo_evento, resultado_diagnostico=None, observacao=None, id_manejo=None):
        self.id_manejo = id_manejo
        self.brinco_animal = brinco_animal
        self.cpf_responsavel = cpf_responsavel
        self.data_evento = data_evento
        self.tipo_evento = tipo_evento
        self.resultado_diagnostico = resultado_diagnostico
        self.observacao = observacao

    @property
    def data_evento(self):
        return self.__data_evento
    
    @data_evento.setter
    def data_evento(self, data_recebida):
        data_convertida = self.valida_data(data_recebida)
        if data_convertida:
            if data_convertida > date.today():
                raise ValueError("A data do manejo não pode ser uma data futura.")
            self.__data_evento = data_convertida
        else:
            raise ValueError("Data do evento é obrigatória.")

    @property
    def tipo_evento(self):
        return self.__tipo_evento
    
    @tipo_evento.setter
    def tipo_evento(self, valor):
        eventos_validos = ['Inseminação', 'Diagnóstico', 'Parto', 'Aborto']
        if valor in eventos_validos:
            self.__tipo_evento = valor
        else:
            raise ValueError(f"Tipo de evento inválido. Escolha entre: {', '.join(eventos_validos)}")

    @property
    def resultado_diagnostico(self):
        return self.__resultado_diagnostico

    @resultado_diagnostico.setter
    def resultado_diagnostico(self, valor):
        if valor in [None, "", "N/A"]:
            self.__resultado_diagnostico = None
            
        elif valor not in ["Positivo", "Negativo"]:
            raise ValueError("O resultado do diagnóstico deve ser 'Positivo' ou 'Negativo'!")
            
        else:
            self.__resultado_diagnostico = valor

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

    def exibir_informacoes(self):
        info = f"Manejo [{self.tipo_evento}] - Data: {self.data_evento}\n"
        info += f"Animal (Brinco): {self.brinco_animal} | Responsável (CPF): {self.cpf_responsavel}\n"
        if self.resultado_diagnostico:
            info += f"Resultado: {self.resultado_diagnostico}\n"
        if self.observacao:
            info += f"Obs: {self.observacao}"
        return info