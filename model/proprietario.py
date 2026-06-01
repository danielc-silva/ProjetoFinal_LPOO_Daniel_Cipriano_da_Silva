from pessoa import Pessoa

class Proprietario(Pessoa):
    def __init__(self, cpf, nome, telefone, inscricao_estadual, nome_fazenda):
        super().__init__(cpf, nome, telefone)
        self.inscricao_estadual = inscricao_estadual
        self.nome_fazenda = nome_fazenda

    @property
    def inscricao_estadual(self):
        return self.__inscricao_estadual
    
    @inscricao_estadual.setter
    def inscricao_estadual(self, valor):
        if isinstance(valor, str) and valor.strip():
            self.__inscricao_estadual = valor.strip()
        else:
            raise ValueError("A inscrição estadual não pode estar vazia.")

    @property
    def nome_fazenda(self):
        return self.__nome_fazenda
    
    @nome_fazenda.setter
    def nome_fazenda(self, valor):
        if isinstance(valor, str) and valor.strip():
            self.__nome_fazenda = valor.strip()
        else:
            raise ValueError("O nome da fazenda não pode estar vazio.")

    def obter_identificacao_profissional(self):
        return f"Proprietário(a) {self.nome} - Fazenda: {self.nome_fazenda} (IE: {self.inscricao_estadual})"

    def exibir_informacoes(self):
        info = f"CPF: {self.cpf}\n"
        info += f"Nome: {self.nome}\n"
        info += f"Telefone: {self.telefone}\n"
        info += f"Inscrição Estadual: {self.inscricao_estadual}\n"
        info += f"Nome da Fazenda: {self.nome_fazenda}"
        return info