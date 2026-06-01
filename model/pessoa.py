from abc import ABC, abstractmethod

class Pessoa(ABC):
    def __init__(self, cpf, nome, telefone):
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone

    @property
    def cpf(self):
        return self.__cpf
    
    @cpf.setter
    def cpf(self, valor):
        if self.validar_cpf(valor):
            self.__cpf = valor
        else:
            raise ValueError("O CPF informado é inválido.")
        
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, valor):
        if isinstance(valor, str) and valor.strip():
            self.__nome = valor.strip()
        else:
            raise ValueError("O nome não pode estar vazio.")

    @property
    def telefone(self):
        return self.__telefone
    
    @telefone.setter
    def telefone(self, valor):
        digitos = ''.join(filter(str.isdigit, str(valor)))
        if len(digitos) >= 11:
            self.__telefone = valor
        else:
            raise ValueError("O telefone deve conter ao menos 11 dígitos numéricos incluindo o DDD.")

    @staticmethod
    def validar_cpf(cpf):
        cpf_numeros = ''.join(filter(str.isdigit, str(cpf)))
        
        if len(cpf_numeros) != 11 or len(set(cpf_numeros)) == 1:
            return False
            
        for i in range(9, 11):
            soma = sum(int(cpf_numeros[num]) * ((i + 1) - num) for num in range(0, i))
            digito = (soma * 10 % 11) % 10
            if digito != int(cpf_numeros[i]):
                return False
        return True
    
    # método para tornar a class pessoa abstrat
    @abstractmethod
    def obter_identificacao_profissional(self):
        pass

    @abstractmethod
    def exibir_informacoes(self):
        pass
