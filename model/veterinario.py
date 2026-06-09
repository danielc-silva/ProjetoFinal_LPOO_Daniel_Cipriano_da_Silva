from model.pessoa import Pessoa

class Veterinario(Pessoa):
    def __init__(self, cpf, nome, telefone, crmv, especialidade):
        super().__init__(cpf, nome, telefone)
        self.crmv = crmv
        self.especialidade = especialidade

    @property
    def crmv(self):
        return self.__crmv
    
    @crmv.setter
    def crmv(self, valor):
        if isinstance(valor, str) and valor.strip():
            self.__crmv = valor.strip()
        else:
            raise ValueError("O CRMV deve ser um valor válido.")

    def obter_identificacao_profissional(self):
        return f"Veterinário(a) {self.nome} - CRMV: {self.crmv} ({self.especialidade})"
    
    def exibir_informacoes(self):
        info = f"CPF: {self.cpf}\n"
        info += f"Nome: {self.nome}\n"
        info += f"Telefone: {self.telefone}\n"
        info += f"CRMV: {self.crmv}\n"
        info += f"Especialidade: {self.especialidade}"
        return info